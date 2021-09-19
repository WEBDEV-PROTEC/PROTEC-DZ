# -*- coding: utf-8 -*-
{
    'name': "Signup Avinet",
    'summary': """
        Custom Module for customization for signup etc""",

    'description': """
        Custom Module for customization for signup etc
    """,

    'author': "Dalila Hannouche",
    'website': "https://www.linkedin.com/comm/in/dalila-h-8a6896143",
    'category': 'Account',
    'version': '0.1',
    'sequence': 2,
    "depends": ["web", "website", "auth_signup"],

    # always loaded
    'data': [
        'security/security.xml',
        'security/cron.xml',
        'security/ir.model.access.csv',

        
        'views/assets.xml',
        'views/approval_view.xml',

        'views/templates/assets.xml',
        'views/templates/signup.xml',
        'views/templates/res_users.xml',

    ],
    "installable": True,
    "auto_install": False,
    'application': True,
}
