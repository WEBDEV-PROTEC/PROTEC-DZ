# -*- coding: utf-8 -*-
from odoo import api, SUPERUSER_ID
import logging
_logger = logging.getLogger(__name__)


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        # Replace 'your_module.view_id' with your view's XML ID
        view = env.ref('your_module.view_id', raise_if_not_found=False)
        if view:
            view.active = True
            env.cr.commit()  # Ensure the change is saved after the upgrade
            _logger.info("View %s has been reactivated.",view.name)
        else:
            _logger.info("View not found.")