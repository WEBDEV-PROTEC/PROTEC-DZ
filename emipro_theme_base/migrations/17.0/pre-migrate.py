# -*- coding: utf-8 -*-
from odoo import api, SUPERUSER_ID
import logging
_logger = logging.getLogger(__name__)


def migrate(cr, version):

    from odoo import api, SUPERUSER_ID

    """Migration script for emipro_theme_base and theme_clarico_vega for v14 to v17."""
    _logger.info("---------------- Migration script execution start ----------------")
    cr.execute("""    
        ALTER TABLE IF EXISTS product_brand_ept RENAME TO product_brand;
        UPDATE ir_model SET model='product.brand' where model='product.brand.ept';
        UPDATE ir_model_fields SET model='product.brand' where model='product.brand.ept';
        UPDATE ir_model_fields SET relation='product.brand' where relation='product.brand.ept';
        UPDATE ir_model_fields SET name='product_brand_id' where name='product_brand_ept_id';
        ALTER TABLE product_template RENAME COLUMN product_brand_ept_id TO product_brand_id;

        DELETE from ir_ui_view where name in ('product.attribute.quick.filter.form','slider_auto_play','product.template.product.website.form.inherit', 'product_brand_container', 'product.template.brand.add.form', 'dynamic_category_mega_menu', 'products_ept');
        UPDATE ir_module_module SET state = 'uninstalled' WHERE name IN ('emipro_theme_banner_video','emipro_theme_brand','emipro_theme_category_listing', 'emipro_theme_landing_page', 'emipro_theme_lazy_load', 'emipro_theme_load_more', 'emipro_theme_product_carousel','emipro_theme_product_label', 'emipro_theme_product_label_extended', 'emipro_theme_product_tabs','emipro_theme_product_timer','emipro_theme_quick_filter','pwa_ept');
        DELETE from theme_ir_ui_view where name in ('dynamic_category_mega_menu');
        ALTER TABLE website DROP COLUMN banner_video_url, DROP COLUMN number_of_product_line, DROP COLUMN website_company_info,DROP COLUMN website_footer_extra_links,DROP COLUMN website_header_offer_ept,DROP COLUMN footer_style_1_content_ept,DROP COLUMN footer_style_3_content_ept,DROP COLUMN footer_style_4_content_ept,DROP COLUMN footer_style_5_content_ept,DROP COLUMN footer_style_6_content_ept,DROP COLUMN footer_style_7_content_ept,DROP COLUMN website_header_extra_links,DROP COLUMN website_vertical_menu_ept,DROP COLUMN is_auto_play,DROP COLUMN is_price_range_filter,DROP COLUMN b2b_hide_details,DROP COLUMN allow_reorder,DROP COLUMN b2b_checkout;
        ALTER TABLE product_attribute DROP COLUMN IF EXISTS is_quick_filter, DROP COLUMN IF EXISTS allow_search;
        ALTER TABLE product_brand DROP COLUMN IF EXISTS is_brand_page, DROP COLUMN IF EXISTS brand_page, DROP COLUMN IF EXISTS is_featured_brand;
        ALTER TABLE product_label_line DROP COLUMN IF EXISTS website_id, DROP COLUMN IF EXISTS label;
        ALTER TABLE website_menu DROP COLUMN menu_label_text, DROP COLUMN menu_label_text_color;
        DELETE from ir_asset where name LIKE 'emipro_%';
        DELETE from ir_model where model in ('slider.filter', 'slider.styles');
        DROP TABLE IF EXISTS slider_filter, slider_styles;
    """)
    _logger.info("---------------- Migration script execution done ----------------")

    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        # Replace 'your_module.view_id' with your view's XML ID
        view = env.ref('your_module.view_id', raise_if_not_found=False)
        if view:
            view.active = False
            env.cr.commit()  # Ensure the change is saved before the upgrade
            _logger.info("View %s has been archieved",view.name)
        else:
            _logger.info("View not found.")
