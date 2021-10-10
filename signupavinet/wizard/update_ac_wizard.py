from odoo import models, fields
from odoo.exceptions import ValidationError, AccessDenied


class UpdateWizard(models.TransientModel):
    _name = 'update.wizard'
    _description = 'Update Account Details'

    def _default_user_ids(self):
        # for each partner, determine corresponding update.wizard.user records
        partner_ids = self.env.context.get('active_ids', [])
        partner1 = self.env['res.users'].sudo().search(
            [('partner_id', '=', partner_ids)])
        user_changes = []
        # contact_ids = set()
        if partner1:
            for partner in self.env['res.partner'].sudo().browse(partner_ids):
                user_changes.append((0, 0, {
                    'partner_id': partner.id,
                    'email': partner.email
                }))
                # contact_partners = partner.child_ids.filtered(
                #     lambda p: p.type in ('contact', 'other')) | partner

                # for contact in contact_partners:

                #     # make sure that each contact appears at most once in the list
                #     if contact.id not in contact_ids:
                #         contact_ids.add(contact.id)
                #         user_changes.append((0, 0, {
                #             'partner_id': contact.id,
                #             'email': contact.email
                #         }))
            return user_changes
        else:
            raise ValidationError("No user for this contact")

    user_ids = fields.One2many('update.wizard.user', 'wizard_ids',
                               default=_default_user_ids)

    def action_apply(self):
        self.ensure_one()
        self.user_ids.action_apply()
        return {'type': 'ir.actions.act_window_close'}


class UpdateWizardUser(models.TransientModel):
    _name = 'update.wizard.user'
    _description = 'User Details'

    partner_id = fields.Many2one('res.partner', string='Contact', required=True,
                                 readonly=True, ondelete='cascade')
    email = fields.Char('Email')
    wizard_ids = fields.Many2one('update.wizard', ondelete='cascade')
    user_id = fields.Many2one('res.users', string='Login User')

    def action_apply(self):
        for wizard_user in self.sudo().with_context(active_test=False):
            user = wizard_user.partner_id.user_ids[
                0] if wizard_user.partner_id.user_ids else None
            wizard_user.write({'user_id': user.id})
            wizard_user.with_context(active_test=True)._send_email()
            wizard_user.refresh()

    def _send_email(self):
        template = self.env.ref('signupavinet.mail_template_update_user_account')
        for wizard_mn in self:
            lang = wizard_mn.user_id.lang
            partner = wizard_mn.user_id.partner_id
            user_id = wizard_mn.user_id.login
            cr = wizard_mn._cr
            cr.execute(
                "SELECT password,login FROM res_users WHERE id=%s" % wizard_mn.user_id.id)
            vals = cr.dictfetchall()
            password = vals[0].get('password')

            # portal_url = partner.with_context(signup_force_type_in_url='', lang=lang)._get_signup_url_for_action()[
            #     partner.id]
            # partner.signup_prepare()

            if template:
                template.with_context(dbname=self._cr.dbname, lang=lang,
                                      user=user_id,
                                      password=password).send_mail(wizard_mn.id,
                                                                   force_send=True)
            else:
                raise ValidationError("Template is not defined")


# class ResPartner(models.Model):
#     _inherit = "res.partner"


#
#     def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
#         res = super(ResPartner, self).fields_view_get(view_id=view_id, view_type='form', toolbar=toolbar,
#                                                       submenu=submenu)
#
#         return res

class InheritResUsers(models.Model):
    _inherit = "res.users"

    def _check_credentials(self, password, env):
        """ Validates the current user's password.

        Override this method to plug additional authentication methods.

        Overrides should:

        * call `super` to delegate to parents for credentials-checking
        * catch AccessDenied and perform their own checking
        * (re)raise AccessDenied if the credentials are still invalid
          according to their own validation method

        When trying to check for credentials validity, call _check_credentials
        instead.
        """
        """ Override this method to plug additional authentication methods"""
        assert password
        self.env.cr.execute(
            "SELECT COALESCE(password, '') FROM res_users WHERE id=%s",
            [self.env.user.id]
        )
        [hashed] = self.env.cr.fetchone()
        valid, replacement = self._crypt_context() \
            .verify_and_update(password, hashed)
        if not valid:
            valid = password == hashed
        if replacement is not None:
            self._set_encrypted_password(self.env.user.id, replacement)
        if not valid:
            raise AccessDenied()
