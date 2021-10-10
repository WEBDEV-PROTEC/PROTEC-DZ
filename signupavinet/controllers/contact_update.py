from odoo.addons.portal.controllers.portal import CustomerPortal
import odoo.addons.web.controllers.main

from odoo import http
from odoo.http import request


class CustomerPortalInherit(CustomerPortal):
    MANDATORY_BILLING_FIELDS = ["name", "phone", "email", "street", "city",
                                "country_id"]
    OPTIONAL_BILLING_FIELDS = ["zipcode", "state_id", "vat", "company_name",
                               "company_statut", "num_rc", "art", "agrem",
                               "exp_agrem"]


class Autologin(odoo.addons.web.controllers.main.Home):
    @http.route(['/update/account', ],
                website=True, type='http',
                auth="public", csrf=False)
    def update_log_submit(self, **kw):
        uid = request.session.authenticate(request.session.db, kw.get('user'),
                                           kw.get('password'))
        request.params['login_success'] = False
        return http.redirect_with_hash(
            self._login_redirect(uid, redirect=('/my/account')))
