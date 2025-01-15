# -*- coding: utf-8 -*-
# from odoo import SUPERUSER_ID, api

# import logging
# _logger = logging.getLogger('Emipro:')


# def migrate(cr, version):
#     _logger.info("-------------Migration | Theme Clarico Vega | script Started---------------")
#     cr.execute("""
#     	ALTER TABLE product_template DROP COLUMN label_line_ids;
#     """)
#     _logger.info("-------------Migration | Theme Clarico Vega | script Ended ---------------")


import logging
_logger = logging.getLogger('Emipro:')


def migrate(cr, version):
    _logger.info("-------------Migration | Theme Clarico Vega | Script Started---------------")
    
    # Check if the column exists before dropping it
    cr.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'product_template' AND column_name = 'label_line_ids';
    """)
    column_exists = cr.fetchone()

    if column_exists:
        cr.execute("""
            ALTER TABLE product_template DROP COLUMN label_line_ids;
        """)
        _logger.info("Column 'label_line_ids' dropped successfully.")
    else:
        _logger.info("Column 'label_line_ids' does not exist. Skipping drop operation.")

    _logger.info("-------------Migration | Theme Clarico Vega | Script Ended ---------------")
