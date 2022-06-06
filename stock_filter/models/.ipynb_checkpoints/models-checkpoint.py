# -*- coding: utf-8 -*-

import hashlib
import json
from odoo import models, fields, api

from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale_wishlist.controllers.main import WebsiteSaleWishlist
from odoo.osv import expression

def _get_search_domain(self, search, category, attrib_values, search_in_description=True, search_in_brand=True):
        domains = super(ThemePrimeWebsiteSale, self)._get_search_domain(search, category, attrib_values, search_in_description)

        # In Stock
        in_stock = request.httprequest.args.get('in_stock')
        
        if in_stock=="1":

            domains = expression.AND([domains, [('qty_available', '>', 0)]])

            return domain