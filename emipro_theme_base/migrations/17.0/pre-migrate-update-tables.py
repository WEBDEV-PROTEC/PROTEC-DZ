# -*- coding: utf-8 -*-

import logging
_logger = logging.getLogger('Emipro:')


def migrate(cr, version):
    _logger.info("-------------Migration | Theme Clarico Vega | script Started---------------")
    cr.execute("""
    	ALTER TABLE product_template DROP COLUMN label_line_ids;
    """)
    _logger.info("-------------Migration | Theme Clarico Vega | script Ended ---------------")
