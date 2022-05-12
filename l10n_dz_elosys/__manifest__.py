# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{
    'name': "Comptabilité - Algérie",
    'category': 'Accounting/Localizations/Account Charts',
    'summary': """ Factures et plan comptable aux normes algériennes. """,
    'category': 'Accounting/Localizations/Account Charts',
    "contributors": [
        "1 <Djamel Eddine YAGOUB>",
        "2 <Nassim REFES>",
        "3 <Kamel BENCHEHIDA>",
        "4 <Mohamed Ould Miloud>",
        "5 <Chenafa Yassamine>",
        "6 <Fatima MESSADI>",
        "7 <Yamina ZOUATINE>",
    ],
    'sequence': 1,
    'version': '14.0.2.3',
    "license": "LGPL-3",
    'author': 'Elosys',
    'website': 'https://www.elosys.net',
    "price": 50,
    "currency": 'EUR',
    'live_test_url':"https://www.elosys.net/shop/comptabilite-et-factures-algerie-2?category=6#attr=4",
    'depends': [
        'base',
        'account',
        'sale',
    ],
    'data': [
        'data/l10n_dz_base_chart_data.xml',
        'data/account_group.xml',
        'data/account_account_template_data.xml',
        'data/account_chart_template_data.xml',
        'data/account_data.xml',
        'data/account_tax_data.xml',
        'data/account_fiscal_position_template_data.xml',
        'data/account_chart_template_configure_data.xml',


        "views/forme_juridique.xml",
        "views/res_company.xml",
        "views/res_partner.xml",
        "views/account_journal.xml",
        "views/account_move.xml",

        'reports/sale_invoice_report.xml',
        'reports/account_invoice_report.xml',
        'reports/inherit_header_footer.xml',
        'reports/inherit_header_footer_boxed.xml',
        'reports/inherit_header_footer_bold.xml',
        'reports/inherit_header_footer_striped.xml',


        'security/ir.model.access.csv',
    ],
    'images': ['images/banner.gif'],

    'post_init_hook': '_preserve_tag_on_taxes',

    'installable': True,
    'auto_install': False,
    'application':False,
}
