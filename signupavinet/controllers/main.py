import logging
from odoo.http import request
from odoo.addons.web.controllers.main import ensure_db, Home
from odoo.exceptions import UserError
from odoo import _
import odoo
from odoo import http
import os
from odoo.service import db, security
import pdb
import werkzeug
from odoo.addons.auth_signup.models.res_users import SignupError
from cryptography.fernet import Fernet


_logger = logging.getLogger(__name__)


class AuthSignupHome(Home):

    @http.route('/request_sent', type='http', auth='public', website=True, sitemap=False, csrf=False)
    def req_sent(self, **kwargs):
        com_values = {
           'name':kwargs.get('company_name'),
           'company_type':kwargs.get('company_type'),
           'email':kwargs.get('login'),
           'vat':kwargs.get('vat'),
           'country_id':kwargs.get('country_id'),
           'password':kwargs.get('password'),
        }
        company = request.env['approval.signup'].sudo().create(com_values)
        response = request.render('signupavinet.signup_done')
        return response

    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False, csrf=False)
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()

        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                self.do_signup(qcontext)
                # Send an account creation confirmation email
                if qcontext.get('token'):
                    User = request.env['res.users']
                    user_sudo = User.sudo().search(
                        User._get_login_domain(qcontext.get('login')), order=User._get_login_order(), limit=1
                    )
                    template = request.env.ref('auth_signup.mail_template_user_signup_account_created',
                                               raise_if_not_found=False)
                    if user_sudo and template:
                        template.sudo().with_context(
                            lang=user_sudo.lang,
                            auth_login=werkzeug.url_encode({'auth_login': user_sudo.email}),
                        ).send_mail(user_sudo.id, force_send=True)
                return self.web_login(*args, **kw)
            except UserError as e:
                qcontext['error'] = e.name or e.value
            except (SignupError, AssertionError) as e:
                if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                    qcontext["error"] = _("Another user is already registered using this email address.")
                else:
                    _logger.error("%s", e)
                    qcontext['error'] = _("Could not create a new account.")

        test = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        invite = request.website.name
        if invite == "DIGIMEX":
            response = request.render('signupavinet.signup', qcontext)
            response.headers['X-Frame-Options'] = 'DENY'
            return response
        else:
            qcontext['url'] = ""
            response = request.render('auth_signup.signup', qcontext)
            response.headers['X-Frame-Options'] = 'DENY'
            return response

    def do_signup(self, qcontext):
        if not qcontext.get('token'):  # our custom function should not be called if user go for reset password. So, we have added this statement
            """ Shared helper that creates a res.partner out of a token """
            values = {key: qcontext.get(key) for key in ('login', 'password')}
            if not values:
                raise UserError(_("The form was not properly filled in."))

            # get all user and check if the email already exist or not
            user = request.env["res.users"].sudo().search([])

            if values.get('password') != qcontext.get('confirm_password'):
                raise UserError(_("Passwords do not match; please retype them."))

            supported_langs = [lang['code'] for lang in request.env['res.lang'].sudo().search_read([], ['code'])]
            if request.lang in supported_langs:
                values['lang'] = request.lang

            elif request.env["res.users"].sudo().search([("login", "=", qcontext.get("email"))]):
                raise UserError(_("Another user is already registered with same Email."))
            try:
                values['name'] = qcontext.get('first_name') + " " + qcontext.get('last_name')
            except:
                pass

            com_values = {
                'company_type': 'company',
                'type': 'contact',
                # 'street': qcontext.get('street'),
                # 'street2': qcontext.get('street2'),
                # 'city': qcontext.get('city'),
                # 'zip': qcontext.get('zip'),
                'country_id': int(qcontext.get('country_id', '0')),
                'name': qcontext.get('company_name'),
                'web_company_type': qcontext.get('company_type'),
                'email': qcontext.get('login'),
                'vat': qcontext.get('vat'),
                # 'comment': qcontext.get('comment'),
            }
            test = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            invite = request.website.name
            if invite != "DIGIMEX":
        
                our_values = {
                    'name': qcontext.get('name'),
                    'type': 'contact',
                    'company_type': 'person',
                }
                print(our_values)

            else:
                our_values = com_values
            login = {
                'name': qcontext.get('name'),
                'login': qcontext.get('login'),
                'password': qcontext.get('password'),
            }
            try:
                company = request.env['res.partner'].sudo().create(our_values)
            except odoo.exceptions.ValidationError:
                raise UserError(_("Vat is not valid"))


            login['partner_id'] = company.id
            values['partner_id'] = company.id
            values['phone'] = qcontext.get('phone')
            values['mobile'] = qcontext.get('mobile')
            invite = request.website.name
            if invite == "DIGIMEX":
                self._signup_with_values(qcontext.get('token'), login)
                request.env.cr.commit()
            else:
                self._signup_with_values(qcontext.get('token'), values)
                request.env.cr.commit()
        else:
            res = super(AuthSignupHome, self).do_signup(qcontext)


class Home(http.Controller):

    def _login_redirect(self, uid, redirect=None):
        return redirect if redirect else '/web'

    @http.route('/invite', type='http', auth='public')
    def web_invite(self, redirect=None, **kw):
        token= kw.get('token')
        logFile = os.path.expanduser('/home/odoo/src/user/signupavinet/settings.conf')

        with open(logFile, 'r') as file:
            test_t = file.read()


        f = Fernet(bytes(test_t, 'utf-8'))

        decrpt = f.decrypt(bytes(token, 'utf-8'))
        account =  decrpt.decode('utf-8').split('/')
        uid = request.session.authenticate("avndgx-main-1897478", account[0], account[1])
        request.params['login_success'] = True
        return http.redirect_with_hash(self._login_redirect(uid, redirect=redirect))

    # @http.route('/testing', type='http', auth='public')
    # def web_te(self, redirect=None, **kw):


    @http.route('/getbaseurl', type='http', auth='public', website=True, sitemap=False, csrf=False)
    def get_base_url(self, redirect=None, **kw):
        test = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        invite = request.website.name
        #if test == "https://avndgx-copy-3025130.dev.odoo.com":
        if invite == "DIGIMEX":
            response = request.render('signupavinet.signup')
            return response
        else:
            
            response = request.render('auth_signup.signup')
            return response
