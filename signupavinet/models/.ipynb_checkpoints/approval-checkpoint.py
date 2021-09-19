from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.addons.auth_signup.models.res_partner import SignupError, now
import logging
import os
from cryptography.fernet import Fernet

from odoo.http import request

_logger = logging.getLogger(__name__)


class ApprovalSignup(models.Model):
    """warranty class"""
    _name = 'approval.signup'
    _description = 'approval.signup'

    name = fields.Char(string="Nom societe")
    company_statut = fields.Selection(
        [('eurl', 'EURL'), ('sarl', 'SARL'), ('snc', 'SNC'), ('spa', 'SPA'),
         ('ets', 'ETS'), ('epe', 'EPE'), ('autre', 'Autre')],
        string='Type Société')
    vat = fields.Char(string="Nif")
    num_rc = fields.Char(string="Numéro RC")
    art = fields.Char(string="ART")
    agrem = fields.Char(string="Agrement")
    street = fields.Char(string="Adresse")
    exp_agrem = fields.Date(string="Date Expiration")
    city_id = fields.Many2one('res.city', domain="[('country_id','=',62)]",
                              string="Ville")
    email = fields.Char(string="Email")
    fname = fields.Char(string="Prenom")
    lname = fields.Char(string="Nom")
    position = fields.Char(string="position")
    phone = fields.Char(string="telephone")
    mobile = fields.Char(string="mobile")
    phone2 = fields.Char(string="telephone")
    mobile2 = fields.Char(string="mobile")
    email2 = fields.Char(string="email")

    scan1 = fields.Binary(string="scan1")
    scan2 = fields.Binary(string="scan2")
    scan3 = fields.Binary(string="scan3")
    scan4 = fields.Binary(string="scan4")
    scan5 = fields.Binary(string="scan5")

    password = fields.Char(string="Password")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
    ], string='Status', readonly=True, store=True, default='draft')

    def action_toapprove(self):
        print("password", self.password)
        print("mail", self.email)
        logFile = os.path.expanduser(
            '/home/odoo/src/user/signupavinet/settings.conf')

        with open(logFile, 'r') as file:
            test_t = file.read()

        print(test_t)
        f = Fernet(bytes(test_t, 'utf-8'))
        token = f.encrypt(bytes(self.email + "/" + self.password, 'utf-8'))
        print(token)
        decrpt = f.decrypt(token)
        print(decrpt)
        contact_name = self.fname + ' ' + self.lname

        com_values = {
            'name': self.name,
            'company_type': 'company',
            'email': self.email,
            'vat': self.vat,
            'company_statut': self.company_statut,
            'num_rc': self.num_rc,
            'art': self.art,
            'agrem': self.agrem,
            'exp_agrem': self.exp_agrem,
            'street': self.street,
            'city_id': self.city_id.id,
            'phone': self.phone,
            'mobile': self.mobile,

        }

        company = self.env['res.partner'].sudo().create(com_values)

        child_values = {
            'parent_id': company.id,
            'name': contact_name,
            'function': self.position,
            'email': self.email2,
            'phone': self.phone2,
            'mobile': self.mobile2,

        }
        self.env['res.partner'].sudo().create(child_values)

        group_id = request.env.ref('base.group_portal').id
        login = {
            'name': self.name,
            'login': self.email,
            'partner_id': company.id,
            'password': self.password,
            'groups_id': [(6, 0, [group_id])],
            'token': token.decode("utf-8")

        }
        user = self.env['res.users'].sudo().create(login)

        # self.env['res.groups'].sudo().write({
        #     'name': group_id,
        #     'users': user
        # })
        print("token", user.token)
        # template_id = self.env.ref('signupavinet.set_password_email').id
        # template = self.env['mail.template'].browse(template_id)
        # template.send_mail(self.id, force_send=True)
        self.state = 'approved'


class ResUsers(models.Model):
    _inherit = 'res.users'

    def action_reset_password(self):
        # print("hi")
        # test = self.env['res.users'].search([('id', '=', self.id)])
        # print(test.name)
        # print(test.password)
        """ create signup token for each user, and send their signup url by email """
        # prepare reset password signup
        create_mode = bool(self.env.context.get('create_user'))

        # no time limit for initial invitation, only for reset password
        expiration = False if create_mode else now(days=+1)

        self.mapped('partner_id').signup_prepare(signup_type="reset",
                                                 expiration=expiration)

        # send email to users with their signup url
        template = False
        if create_mode:
            try:
                template = self.env.ref('signupavinet.set_password_email',
                                        raise_if_not_found=False)
                print("called")
            except ValueError:
                pass
        if not template:
            template = self.env.ref('signupavinet.reset_password_email')
        assert template._name == 'mail.template'

        template_values = {
            'email_to': '${object.email|safe}',
            'email_cc': False,
            'auto_delete': True,
            'partner_to': False,
            'scheduled_date': False,
        }
        template.write(template_values)

        for user in self:
            if not user.email:
                raise UserError(
                    _("Cannot send email: user %s has no email address.") % user.name)
            with self.env.cr.savepoint():
                force_send = not (self.env.context.get('import_file', False))
                template.with_context(lang=user.lang).send_mail(user.id,
                                                                force_send=force_send,
                                                                raise_exception=True)
            _logger.info("Password reset email sent for user <%s> to <%s>",
                         user.login, user.email)
