# -*- coding: utf-8 -*-
#################################################################################
#
# Copyright (c) 2019-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# See LICENSE file for full copyright and licensing details.
#################################################################################

from odoo import http
from odoo.http import request
from odoo import fields
from odoo.addons.website_sale.controllers.main import WebsiteSale
import logging
_logger = logging.getLogger(__name__)


class ProductPriceSlot(WebsiteSale):
    @http.route(["/product/price/slot/<model('product.product'):product_id>"], type='json', auth="public", website=True)
    def load_product_price_slot(self, product_id, **kwargs):
        # Firstly we find the current pricelist on current website
        pricelist = self._get_pricelist_context()[1]
        # Then we filter all the pricelist items which is applicable on given product_id
        applicable_offers = pricelist.item_ids.filtered(lambda item: self.filter_pricelist_item(item,product_id))
        # Then Again check that applicable offers contains any formula and pricelist based offers.
        formula_base_offers = applicable_offers.filtered(lambda item: item.base=='pricelist' and item.compute_price =='formula')
        # Then seperate the non formula based offers from all applicable offer 
        # because we have to process the formula base offers separately.
        qty_base_offers = applicable_offers - formula_base_offers
        # At this stage we process the (formula and pricelist) based offer to get qty_base_offers from them,
        # because formula is based on "other pricelist" so we have to search offer in other pricelist,  
        # and then append that offer to qty_base_offers
        qty_base_form_formula_base = self.get_pricelist_base_item(product_id,formula_base_offers or [])
        if qty_base_form_formula_base:
            qty_base_offers = qty_base_offers + qty_base_form_formula_base if qty_base_offers else qty_base_form_formula_base
        # Then we sort the qty_base_offers on the base of min_quantity field, 
        # And Pick one offer which has minimum quantity,
        relevent_offers = qty_base_offers and qty_base_offers.sorted(lambda item:item.min_quantity)[0] 
        
        # here we find the price of request product for minimum quantity,
        min_qty = relevent_offers and relevent_offers.min_quantity or 2
        price = pricelist.get_product_price(product=product_id,quantity=min_qty, partner=request.env.user.partner_id)

        # Then last step: in this step we will check that any other offer is still there 
        # which give differ price then above calculated price 
        # if yes then append that offer to show on website. 
        for item in qty_base_offers.sorted(lambda item:item.min_quantity):
            current_price = pricelist.get_product_price(product=product_id,quantity=item.min_quantity,partner=request.env.user.partner_id) 
            if price == current_price or min_qty == item.min_quantity:
                continue
            else: 
                price = current_price
                relevent_offers += item

        return request.env.ref("product_price_slots.product_price_offer_template")._render({"product_id":product_id,'relevent_offers':relevent_offers,"pricelist":pricelist,}, engine='ir.qweb')

    def filter_pricelist_item(self, item, product_id):
        product_tmpl_id = product_id.product_tmpl_id
        if item.applied_on == '3_global':
            state = True
        elif item.applied_on == '2_product_category' and (item.categ_id.id in self.get_all_child_category(product_tmpl_id)):
            state = True
        elif item.applied_on == '1_product' and (item.product_tmpl_id == product_tmpl_id):
            state = True
        elif item.applied_on == '0_product_variant' and (item.product_id == product_id):
            state = True
        else:
            state = False
        return state and self.is_valid_pli_item(item)
               
    def is_valid_pli_item(self, pricelist_item):
        # this function simply check that is offer is vallid or not on the base of date. 
        start_date = fields.Date.from_string(pricelist_item.date_start) if pricelist_item.date_start else False
        end_date = fields.Date.from_string(pricelist_item.date_end) if pricelist_item.date_end else False
        today_date = fields.Date.from_string(fields.Date.today())
        if start_date and end_date and start_date <= today_date <= end_date:
           status = True 
        elif not start_date and not end_date:
           status = True 
        elif start_date and not end_date and start_date <= today_date:
           status = True 
        elif not start_date and end_date and today_date <= end_date :
           status = True 
        else:
           status = False
        return (pricelist_item.min_quantity>1 or (pricelist_item.base=='pricelist' and pricelist_item.compute_price =='formula')) and status 


    def get_all_child_category(self, product):
        categ_ids = {}
        if product:
            categ = product.categ_id
            while categ:
                categ_ids[categ.id] = True
                categ = categ.parent_id
        categ_ids = list(categ_ids)
        return categ_ids

    def get_pricelist_base_item(self, product_id,formula_base_offers):
        applicable_offers = False
        for fb_item in formula_base_offers:
            all_offers = fb_item.base_pricelist_id.item_ids
            applied_offer = all_offers.filtered(lambda item: self.filter_pricelist_item(item,product_id))
            fb_offers = applied_offer.filtered(lambda item: item.base=='pricelist' and item.compute_price =='formula')  
            if fb_offers:
                pricelist_base_item = self.get_pricelist_base_item(product_id,fb_offers)
                if pricelist_base_item:
                    applicable_offers = applicable_offers + pricelist_base_item  if applicable_offers else pricelist_base_item
            else:
                applicable_offers = applicable_offers + applied_offer-fb_offers if applicable_offers else applied_offer-fb_offers

        return applicable_offers
    
    def offer_update_cart(self):
        sale_order = request.website.sale_get_order()
        if sale_order:
            for line in sale_order.website_order_line:
                sale_order._cart_update(line_id=line.id, product_id=line.product_id.id)

    @http.route()
    def cart(self, **post):
        res = super(ProductPriceSlot,self).cart(**post)
        self.offer_update_cart()
        return res
        
    @http.route()
    def payment(self, **post):
        res = super(ProductPriceSlot,self).payment(**post)
        self.offer_update_cart()
        return res
