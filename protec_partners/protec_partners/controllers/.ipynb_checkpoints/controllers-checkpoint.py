# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import datetime
import werkzeug.urls

from collections import OrderedDict
from werkzeug.exceptions import NotFound

from odoo import fields
from odoo import http
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import slug, unslug
from odoo.addons.website.models.ir_http import sitemap_qs2dom
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.website_partner.controllers.main import WebsitePartnerPage
from odoo.addons.website_crm_partner_assign.controllers.main import WebsiteCrmPartnerAssign


from odoo.tools.translate import _



class ProtecPartners(WebsiteCrmPartnerAssign):
    _references_per_page = 40

    def sitemap_partners(env, rule, qs):
        if not qs or qs.lower() in '/partners':
            yield {'loc': '/partners'}

        Grade = env['res.partner.grade']
        dom = [('website_published', '=', True)]
        dom += sitemap_qs2dom(qs=qs, route='/partners/grade/', field=Grade._rec_name)
        for grade in env['res.partner.grade'].search(dom):
            loc = '/partners/grade/%s' % slug(grade)
            if not qs or qs.lower() in loc:
                yield {'loc': loc}

        partners_dom = [('is_company', '=', True), ('grade_id', '!=', False), ('website_published', '=', True),
                        ('grade_id.website_published', '=', True), ('state_id', '!=', False)]
        dom += sitemap_qs2dom(qs=qs, route='/partners/wilaya/')
        countries = env['res.partner'].sudo().read_group(partners_dom, fields=['id', 'state_id'], groupby='state_id')
        for country in countries:
            loc = '/partners/wilaya/%s' % slug(country['state_id'])
            if not qs or qs.lower() in loc:
                yield {'loc': loc}

    @http.route([
        '/partners',
        '/partners/page/<int:page>',

        '/partners/grade/<model("res.partner.grade"):grade>',
        '/partners/grade/<model("res.partner.grade"):grade>/page/<int:page>',

        '/partners/wilaya/<model("res.country.state"):country>',
        '/partners/wilaya/<model("res.country.state"):country>/page/<int:page>',

        '/partners/grade/<model("res.partner.grade"):grade>/wilaya/<model("res.country.state"):country>',
        '/partners/grade/<model("res.partner.grade"):grade>/wilaya/<model("res.country.state"):country>/page/<int:page>',
    ], type='http', auth="public", website=True, sitemap=sitemap_partners)
    def partners(self, country=None, grade=None, page=0, **post):
        country_all = post.pop('country_all', False)
        partner_obj = request.env['res.partner']
        country_obj = request.env['res.country']
        search = post.get('search', '')

        base_partner_domain = [('is_company', '=', True), ('grade_id', '!=', False), ('website_published', '=', True)]
        if not request.env['res.users'].has_group('website.group_website_publisher'):
            base_partner_domain += [('grade_id.website_published', '=', True)]
        if search:
            base_partner_domain += ['|', ('name', 'ilike', search), ('website_description', 'ilike', search)]

        # group by grade
        grade_domain = list(base_partner_domain)
        if not country and not country_all:
            country_code = request.session['geoip'].get('country_code')
            if country_code:
                country = country_obj.search([('code', '=', country_code)], limit=1)
        if country:
            grade_domain += [('state_id', '=', country.id)]
        grades = partner_obj.sudo().read_group(
            grade_domain, ["id", "grade_id"],
            groupby="grade_id")
        grades_partners = partner_obj.sudo().search_count(grade_domain)
        # flag active grade
        for grade_dict in grades:
            grade_dict['active'] = grade and grade_dict['grade_id'][0] == grade.id
        grades.insert(0, {
            'grade_id_count': grades_partners,
            'grade_id': (0, _("All Categories")),
            'active': bool(grade is None),
        })

        # group by country
        country_domain = list(base_partner_domain)
        if grade:
            country_domain += [('grade_id', '=', grade.id)]
        countries = partner_obj.sudo().read_group(
            country_domain, ["id", "state_id"],
            groupby="state_id", orderby="state_id")
        countries_partners = partner_obj.sudo().search_count(country_domain)
        # flag active country
        for country_dict in countries:
            country_dict['active'] = country and country_dict['state_id'] and country_dict['state_id'][0] == country.id
        countries.insert(0, {
            'state_id_count': countries_partners,
            'state_id': (0, _("All Wilayas")),
            'active': bool(country is None),
        })

        # current search
        if grade:
            base_partner_domain += [('grade_id', '=', grade.id)]
        if country:
            base_partner_domain += [('state_id', '=', country.id)]

        # format pager
        if grade and not country:
            url = '/partners/grade/' + slug(grade)
        elif country and not grade:
            url = '/partners/wilaya/lol' 
        elif country and grade:
            url = '/partners/grade/' + slug(grade) + '/wilaya/' + slug(country)
        else:
            url = '/partners'
        url_args = {}
        if search:
            url_args['search'] = search
        if country_all:
            url_args['country_all'] = True

        partner_count = partner_obj.sudo().search_count(base_partner_domain)
        pager = request.website.pager(
            url=url, total=partner_count, page=page, step=self._references_per_page, scope=7,
            url_args=url_args)

        # search partners matching current search parameters
        partner_ids = partner_obj.sudo().search(
            base_partner_domain, order="grade_sequence ASC, implemented_count DESC, display_name ASC, id ASC",
            offset=pager['offset'], limit=self._references_per_page)
        partners = partner_ids.sudo()

        google_map_partner_ids = ','.join(str(p.id) for p in partners)
        google_maps_api_key = request.website.google_maps_api_key

        # rech = request.env['res.partner'].search([('is_company', '=', True), ('grade_id', '!=', False), ('website_published', '=', True)])
        
        # states = [a.state_id for a in rech]
        
        countries2 = countries

        

        values = {
            'countries': countries,
            'country_all': country_all,
            'current_country': country,
            'grades': grades,
            'current_grade': grade,
            'partners': partners,
            'google_map_partner_ids': google_map_partner_ids,
            'pager': pager,
            'searches': post,
            'search_path': "%s" % werkzeug.urls.url_encode(post),
            'google_maps_api_key': google_maps_api_key,
        }
        return request.render("website_crm_partner_assign.index", values, status=partners and 200 or 404)


    # Do not use semantic controller due to sudo()
#     @http.route(['/partners/<partner_id>'], type='http', auth="public", website=True)
#     def partners_detail(self, partner_id, **post):
#         _, partner_id = unslug(partner_id)
#         current_grade, current_country = None, None
#         grade_id = post.get('grade_id')
#         country_id = post.get('country_id')
#         if grade_id:
#             current_grade = request.env['res.partner.grade'].browse(int(grade_id)).exists()
#         if country_id:
#             current_country = request.env['res.country'].browse(int(country_id)).exists()
#         if partner_id:
#             partner = request.env['res.partner'].sudo().browse(partner_id)
#             is_website_publisher = request.env['res.users'].has_group('website.group_website_publisher')
#             if partner.exists() and (partner.website_published or is_website_publisher):
#                 values = {
#                     'main_object': partner,
#                     'partner': partner,
#                     'current_grade': current_grade,
#                     'current_country': current_country
#                 }
#                 return request.render("website_crm_partner_assign.partner", values)
#         return self.partners(**post)
