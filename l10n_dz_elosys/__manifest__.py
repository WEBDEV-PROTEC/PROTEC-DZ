# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{
    'name': "Comptabilité - Algérie",
    'summary': """ Plan comptable aux normes algériennes. """,



    'category': 'Accounting/Localizations/Account Charts',
    'version': '17.0',

    "contributors": [
        "1 <Soufyane AMRAOUI>",
        "2 <Chems Eddine SAHININE>",
        "3 <Fatima MESSADI>",
    ],
    'sequence': 1,
    
    
    'author': 'Elosys',
    'website': 'https://www.elosys.net',
    'live_test_url':"https://www.elosys.net/tester_nos_modules",

    "license": "LGPL-3",
    "price": 0.0,
    "currency": 'EUR',
    
    'depends': [
        'base',
        'account',
        'sale',
        'sale_management',
        
    ],

    



    'data': [
        'data/accounting_group.xml',
        # 'data/l10n_dz_base_chart_data.xml',
        'data/account_group.xml',
        'data/account_account_template_data.xml',
        'data/account_chart_template_data.xml',
        'data/account_data.xml',
        'data/account_tax_data.xml',
        'data/account_fiscal_position_template_data.xml',
        'data/account_chart_template_configure_data.xml',
        'data/company_function.xml',
        

        "views/forme_juridique.xml",
        "views/activity_code.xml",
        "views/res_company.xml",
        "views/res_partner.xml",
        "views/configuration_settings.xml",

        


        'security/ir.model.access.csv',
        'security/rules.xml',
    ],

    
    'images': ['images/banner.gif'],

    'post_init_hook': '_preserve_tag_on_taxes',

    'installable': True,
    'auto_install': False,
    'application':False,
}
