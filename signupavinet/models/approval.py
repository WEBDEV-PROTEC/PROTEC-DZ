from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.addons.auth_signup.models.res_partner import SignupError, now
import logging
import os
from cryptography.fernet import Fernet

_logger = logging.getLogger(__name__)


class ApprovalSignup(models.Model):
    """warranty class"""
    _name = 'approval.signup'
    _description = 'approval.signup'

    name = fields.Char(string="Name")
    email = fields.Char(string="Email")
    vat = fields.Char(String="Vat")
    company_type = fields.Char(string="Company Type")
    country_id = fields.Many2one('res.country', string="Country")
    password = fields.Char(string="Password")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
    ], string='Status', readonly=True, store=True, default='draft')

    def action_toapprove(self):
        print("password", self.password)
        print("mail", self.email)
        logFile = os.path.expanduser('/home/odoo/src/user/signupavinet/settings.conf')


        with open(logFile, 'r') as file:
            test_t = file.read()


        print(test_t)
        f = Fernet(bytes(test_t, 'utf-8'))
        token = f.encrypt(bytes(self.email+"/"+self.password, 'utf-8'))
        print(token)
        decrpt = f.decrypt(token)
        print(decrpt)

        com_values = {
            'name': self.name,
            'company_type': 'company',
            'email': self.email,
            'vat': self.vat,
        }

        company = self.env['res.partner'].sudo().create(com_values)
        login = {
            'name': self.name,
            'login': self.email,
            'partner_id': company.id,
            'sel_groups_1_8_9': 9,
            'password': self.password,
            'token': token.decode("utf-8") ,
        }
        user = self.env['res.users'].sudo().create(login)
        print("token", user.token)
        template_id = self.env.ref('signupavinet.set_password_email').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)
        self.state = 'approved'


    def test_cron_job(self):
        i = 0
        test = self.env['res.users'].search([('share', '=', False)])
        record = self.env['approval.signup'].search([])
        for rec in record:
            if rec.state == 'draft':
                i = 1
        if i ==1:
            for user in  test:
                user.notify_info(message='Pending Approval request')

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

        self.mapped('partner_id').signup_prepare(signup_type="reset", expiration=expiration)

        # send email to users with their signup url
        template = False
        if create_mode:
            try:
                template = self.env.ref('signupavinet.set_password_email', raise_if_not_found=False)
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
                raise UserError(_("Cannot send email: user %s has no email address.") % user.name)
            with self.env.cr.savepoint():
                force_send = not(self.env.context.get('import_file', False))
                template.with_context(lang=user.lang).send_mail(user.id, force_send=force_send, raise_exception=True)
            _logger.info("Password reset email sent for user <%s> to <%s>", user.login, user.email)