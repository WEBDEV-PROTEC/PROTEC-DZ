# -*- coding: utf-8 -*-

# Copyright © 2021 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# @author: Iryna Razumovska (<support@garazd.biz>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

{
    'name': 'Facebook Domain Verification',
    'version': '14.0.1.0.0',
    'category': 'Website',
    'author': 'Garazd Creation',
    'website': 'https://garazd.biz',
    'license': 'LGPL-3',
    'summary': 'Facebook Domain Verification by meta-tag',
    'images': ['static/description/banner.png'],
    'live_test_url': 'https://garazd.biz/r/dW5',
    'description': """
The module allows completing the verification of an odoo website domain by meta-tag to configure Facebook Web Events.

    """,
    'depends': [
        'website',
    ],
    'data': [
        'views/website_views.xml',
        'views/website_templates.xml',
    ],
    'external_dependencies': {
    },
    'support': 'support@garazd.biz',
    'application': False,
    'installable': True,
    'auto_install': False,
}
