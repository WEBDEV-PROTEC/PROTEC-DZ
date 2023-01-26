# -*- coding: utf-8 -*-
#################################################################################
#
# Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# See LICENSE file for full copyright and licensing details.
#################################################################################

from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)

class Website(models.Model):
    _inherit = 'website'

    @api.model
    def check_partner_country_eligiblity_for_pricelist(self, partner, pricelist):
        partner = partner or self.env.user.partner_id
        partner_country = partner.country_id
        if pricelist and pricelist.country_group_ids and partner_country:
            for country_group in pricelist.country_group_ids:
                return partner_country.id in country_group.country_ids.ids
        return True 

    def check_offer_expired_or_not(self, offer):
        date_end = offer.date_end
        date_now = fields.Datetime.now()
        if date_end and date_now > date_end:
            return True
        else:
            return False

   