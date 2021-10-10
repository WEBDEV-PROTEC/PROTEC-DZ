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
import datetime
import base64

_logger = logging.getLogger(__name__)


class AuthSignupHome(Home):

    @http.route('/request_sent', type='http', auth='public', website=True,
                sitemap=False, csrf=False)
    def req_sent(self, **kwargs):
        com_values1 = {}
        if kwargs.get('exp_agrem') != '':
            com_values1['exp_agrem'] = datetime.datetime.strptime(
                kwargs.get('exp_agrem'), "%Y-%m-%d").date()

        city_id = request.env['res.city'].search(
            [('name', '=', kwargs.get('ville'))]).id
        # file = request.httprequest.files.getlist('scan')[0].read()

        files = request.httprequest.files.getlist('scan')
        for i in range(len(files)):
            print(i)
            if i >= 5:
                raise UserError(
                    _("Passwords do not match; please retype them."))

            com_values1['scan' + str(i + 1)] = base64.b64encode(files[i].read())

        com_values2 = {
            'name': kwargs.get('company_name'),
            'company_statut': kwargs.get('company_type'),
            'email': kwargs.get('login'),
            'vat': kwargs.get('vat'),
            'num_rc': kwargs.get('num_rc'),
            'art': kwargs.get('art'),
            'agrem': kwargs.get('agrem'),

            'fname': kwargs.get('first_name'),
            'lname': kwargs.get('last_name'),
            'mobile': kwargs.get('mobile'),
            'phone': kwargs.get('phone'),
            'city_id': city_id,
            'street': kwargs.get('adresse'),
            'password': kwargs.get('password'),

        }
        com_values = {**com_values1, **com_values2}
        company = request.env['approval.signup'].sudo().create(com_values)
        response = request.render('signupavinet.signup_done')
        return response

    @http.route('/web/signup', type='http', auth='public', website=True,
                sitemap=False, csrf=False)
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
                        User._get_login_domain(qcontext.get('login')),
                        order=User._get_login_order(), limit=1
                    )
                    template = request.env.ref(
                        'auth_signup.mail_template_user_signup_account_created',
                        raise_if_not_found=False)
                    if user_sudo and template:
                        template.sudo().with_context(
                            lang=user_sudo.lang,
                            auth_login=werkzeug.url_encode(
                                {'auth_login': user_sudo.email}),
                        ).send_mail(user_sudo.id, force_send=True)
                return self.web_login(*args, **kw)
            except UserError as e:
                qcontext['error'] = e.name or e.value
            except (SignupError, AssertionError) as e:
                if request.env["res.users"].sudo().search(
                        [("login", "=", qcontext.get("login"))]):
                    qcontext["error"] = _(
                        "Another user is already registered using this email address.")
                else:
                    _logger.error("%s", e)
                    qcontext['error'] = _("Could not create a new account.")

        test = request.env['ir.config_parameter'].sudo().get_param(
            'web.base.url')
        invite = request.website.name
        ville = request.env['res.country.state'].sudo().search(
            [('country_id', '=', request.env.ref('base.dz').id)])
        city = request.env['res.city'].sudo().search([])
        qcontext.update({'villes': ville, 'city': city})
        if invite == "PROTEC IT Network & Security":
            response = request.render('signupavinet.signup', qcontext)
            response.headers['X-Frame-Options'] = 'DENY'
            return response
        else:
            qcontext['url'] = ""
            response = request.render('auth_signup.signup', qcontext)
            response.headers['X-Frame-Options'] = 'DENY'
            return response

    def do_signup(self, qcontext):
        if not qcontext.get(
                'token'):  # our custom function should not be called if user go for reset password. So, we have added this statement
            """ Shared helper that creates a res.partner out of a token """
            values = {key: qcontext.get(key) for key in ('login', 'password')}
            if not values:
                raise UserError(_("The form was not properly filled in."))

            # get all user and check if the email already exist or not
            user = request.env["res.users"].sudo().search([])

            if values.get('password') != qcontext.get('confirm_password'):
                raise UserError(
                    _("Passwords do not match; please retype them."))

            supported_langs = [lang['code'] for lang in
                               request.env['res.lang'].sudo().search_read([], [
                                   'code'])]
            if request.lang in supported_langs:
                values['lang'] = request.lang

            elif request.env["res.users"].sudo().search(
                    [("login", "=", qcontext.get("email"))]):
                raise UserError(
                    _("Another user is already registered with same Email."))
            try:
                values['name'] = qcontext.get(
                    'first_name') + " " + qcontext.get('last_name')
            except:
                pass

            com_values44 = {
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
            exp_agrem = datetime.datetime.strptime(qcontext.get('exp_agrem'),
                                                   "%Y-%m-%d").date()
            city_id = request.env['res.city'].search(
                [('name', '=', qcontext.get('ville'))]).id
            com_values = {
                'name': "qcontext.get('company_name')",

                'company_statut': qcontext.get('company_type'),
                'email': qcontext.get('login'),
                'vat': qcontext.get('vat'),
                'num_rc': qcontext.get('num_rc'),
                'art': qcontext.get('art'),
                'agrem': qcontext.get('agrem'),
                'exp_agrem': exp_agrem,
                'mobile': qcontext.get('mobile'),
                'phone': qcontext.get('phone'),
                'city_id': city_id,
                'street': qcontext.get('adresse'),

            }
            test = request.env['ir.config_parameter'].sudo().get_param(
                'web.base.url')
            invite = request.website.name
            if invite != "PROTEC IT Network & Security":

                our_values = {
                    'name': qcontext.get('company_name'),
                    'type': 'contact',
                    'company_type': 'person',
                }
                print(our_values)

            else:
                our_values = com_values
            login = {
                'name': qcontext.get('company_name'),
                'login': qcontext.get('login'),
                'password': qcontext.get('password'),
            }
            try:
                company = request.env['res.partner'].sudo().create(com_values)
            except odoo.exceptions.ValidationError:
                raise UserError(_("Vat is not valid"))

            login['partner_id'] = company.id
            values['partner_id'] = company.id
            values['phone'] = qcontext.get('phone')
            values['mobile'] = qcontext.get('mobile')
            invite = request.website.name
            if invite == "PROTEC IT Network & Security":
                company = request.env['approval.signup'].sudo().create(
                    com_values)
                response = request.render('signupavinet.signup_done')
                return response
            else:
                self._signup_with_values(qcontext.get('token'), values)
                request.env.cr.commit()
        else:
            res = super(AuthSignupHome, self).do_signup(qcontext)

    @http.route('/get/city', type='json', auth='public', website=True,
                sitemap=False, csrf=False)
    def search_city(self, domain):
        cities = request.env['res.city'].sudo().search([
            ('state_id.id', '=', domain)
        ])
        city = []
        for rec in cities:
            city.append([rec.name, rec.id])
        return city


class Home(http.Controller):

    def _login_redirect(self, uid, redirect=None):
        return redirect if redirect else '/web'

    @http.route('/invite', type='http', auth='public')
    def web_invite(self, redirect=None, **kw):
        token = kw.get('token')
        logFile = os.path.expanduser(
            '/home/cybrosys/odoo-14.0/user/signupavinet/settings.conf')

        with open(logFile, 'r') as file:
            test_t = file.read()

        f = Fernet(bytes(test_t, 'utf-8'))

        decrpt = f.decrypt(bytes(token, 'utf-8'))
        account = decrpt.decode('utf-8').split('/')
        uid = request.session.authenticate("protecdz-copie-3087959", account[0],
                                           account[1])
        request.params['login_success'] = True
        return http.redirect_with_hash(
            self._login_redirect(uid, redirect=redirect))

    # @http.route('/testing', type='http', auth='public')
    # def web_te(self, redirect=None, **kw):

    @http.route('/getbaseurl', type='http', auth='public', website=True,
                sitemap=False, csrf=False)
    def get_base_url(self, redirect=None, **kw):
        test = request.env['ir.config_parameter'].sudo().get_param(
            'web.base.url')
        invite = request.website.name
        # if test == "https://avndgx-copy-3025130.dev.odoo.com":
        if invite != "PROTEC IT Network & Security":
            response = request.render('signupavinet.signup')
            return response
        else:

            response = request.render('auth_signup.signup')
            return response
