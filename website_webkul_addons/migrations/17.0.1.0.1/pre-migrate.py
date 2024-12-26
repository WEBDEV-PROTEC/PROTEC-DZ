# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)
from odoo import SUPERUSER_ID, api


modules = ['abs_so_minimum_quantity', 'al_web_price_hide', 'amount_in_letters', 'auto_generate_product_code_app', 'batch_payment_pdf',  'contact_protec', 'custom_login', 'custom_pricelist_report', 'customer_sale_history', 'droggol_mass_mailing_themes', 'emipro_theme_banner_video', 'emipro_theme_base', 'emipro_theme_brand', 'emipro_theme_category_listing', 'emipro_theme_landing_page', 'emipro_theme_lazy_load', 'emipro_theme_load_more', 'emipro_theme_product_carousel', 'emipro_theme_product_label', 'emipro_theme_product_label_extended', 'emipro_theme_product_tabs', 'emipro_theme_product_timer', 'emipro_theme_quick_filter', 'fl_so_po_multi_products', 'images_order',  'l10n_dz_elosys', 'multi_warehouse_sale_order', 'payment_cash_on_delivery', 'printnode_base', 'product_banner_a6', 'product_catalogue', 'product_price_slots', 'protec_optional_products', 'protec_partners', 'pwa_ept', 'sales_credit_limit', 'sh_call_for_price', 'sh_shop_qty', 'sh_website_category_page', 'signupavinet', 'stock_filter', 'stock_notifier', 'tags', 'tags_product', 'theme_clarico_vega', 'timbre_fiscal', 'video_player', 'webdescription', 'website_product_pack', 'website_stock', 'website_stock_notifiy', 'wk_product_pack']
def migrate(cr, version):
    _logger.info(f'Starting migration from version {version}.')
    env = api.Environment(cr, SUPERUSER_ID,{})
    # openupgrade.rename_tables(cr, brand_table_renames)
    # openupgrade.rename_models(cr, brand_model_renames)
#     cr.execute("""INSERT INTO product_brand
# select * from product_brand_ept;
# """)
    model = env['ir.module.module']
    module_ids = model.search(
        [('name', 'in', modules)])
    _logger.info('uninstall module %s' % modules)
    _logger.info('ids for module: %s' % module_ids)
    for module in module_ids:
        try:
            module.button_uninstall()
        except Exception as e:
            _logger.info("======****============%r",e)
    _logger.info('module uninstalled')
    cr.execute("""
                delete from ir_model_data where module in ('abs_so_minimum_quantity', 'al_web_price_hide', 'amount_in_letters', 'auto_generate_product_code_app', 'batch_payment_pdf',  'contact_protec', 'custom_login', 'custom_pricelist_report', 'customer_sale_history', 'droggol_mass_mailing_themes', 'emipro_theme_banner_video', 'emipro_theme_base', 'emipro_theme_brand', 'emipro_theme_category_listing', 'emipro_theme_landing_page', 'emipro_theme_lazy_load', 'emipro_theme_load_more', 'emipro_theme_product_carousel', 'emipro_theme_product_label', 'emipro_theme_product_label_extended', 'emipro_theme_product_tabs', 'emipro_theme_product_timer', 'emipro_theme_quick_filter', 'fl_so_po_multi_products', 'images_order',  'l10n_dz_elosys', 'multi_warehouse_sale_order', 'payment_cash_on_delivery', 'printnode_base', 'product_banner_a6', 'product_catalogue', 'product_price_slots', 'protec_optional_products', 'protec_partners', 'pwa_ept', 'sales_credit_limit', 'sh_call_for_price', 'sh_shop_qty', 'sh_website_category_page', 'signupavinet', 'stock_filter', 'stock_notifier', 'tags', 'tags_product', 'theme_clarico_vega', 'timbre_fiscal', 'video_player', 'webdescription', 'website_product_pack', 'website_stock', 'website_stock_notifiy', 'wk_product_pack'); 
               """)
    cr.execute("""delete from ir_asset;
                delete from ir_cron where id=35;
                delete from ir_cron where id=44;
                delete from ir_cron where id=61;
               delete from ir_cron where id=59;
               delete from ir_cron where id=60;
               delete from ir_model_fields where name in ('show_category','printnode_enabled', 'product_brand_ept_id','sale_product_count','rc','exclude_website_ids','is_display_timer','equation_montant','use_timbre','printnode_printed','is_dynamic_menu','due_amount','autoprint_paperformat_id');
                delete from ir_model where model='website.stock.config.settings';
                delete from  website_notifiy_config_settings;
                delete from mail_template where model='website.stock.notify';
                delete from ir_model where model='config.timbre';
                delete from ir_model where model='product.brand.ept';
                delete from ir_model where model='approval.signup';
                delete from ir_model where model='sale.call.for.price';
                delete from ir_model where model='website.stock.notify';
                delete from ir_model where model='printnode.report.policy';
                delete from ir_model where model='printnode.printer';
                delete from ir_model where model='printnode.action.button';
                delete from ir_model where model='printnode.scenario';
                delete from ir_model where model='printnode.rule';
                delete from ir_model where model='shipping.label';
                delete from ir_model where model='printnode.printjob';
                delete from ir_model where model='printnode.release';
                delete from ir_model where model='printnode.account';
                delete from ir_model where model='printnode.computer';
                delete from ir_model where model='printnode.scales';
                delete from ir_model where model='printnode.paper';
                delete from ir_model where model='printnode.action.method';
                delete from ir_model where model='printnode.map.action.server';
                delete from ir_model_fields where model='config.timbre';
                delete from ir_model_fields where model='product.brand.ept';
                delete from ir_model_fields where model='approval.signup';
                delete from ir_model_fields where model='sale.call.for.price';
                delete from ir_model_fields where model='website.stock.notify';
                delete from ir_model_fields where model='printnode.report.policy';
                delete from ir_model_fields where model='printnode.printer';
                delete from ir_model_fields where model='printnode.action.button';
                delete from ir_model_fields where model='printnode.scenario';
                delete from ir_model_fields where model='printnode.rule';
                delete from ir_model_fields where model='shipping.label';
                delete from ir_model_fields where model='printnode.printjob';
                delete from ir_model_fields where model=' printnode.release';
                delete from ir_model_fields where model='printnode.account';
                delete from ir_model_fields where model='printnode.computer';
                delete from ir_model_fields where model='printnode.printer';
                delete from ir_model_fields where model='printnode.scales';
                delete from ir_model_fields where model='printnode.paper';
                delete from ir_model_fields where model='printnode.action.method';
               delete from ir_model_fields where model='printnode.map.action.server';
               """)
    _logger.info('**********Delete******** generate_combination')
   
    _logger.info('**********Deleted******** generate_combination')
    
    _logger.info("============installe commession")
    _logger.info('Migration completed.')

    _logger.info("============module migrate")
    
