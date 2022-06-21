# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{
    'name'        : "Plan des comptes",
    'summary'     : "Structuration du plan comptable, Lecture des (Débit, Crédit, Solde) plus facile",
    'description' : "Structuration du plan comptable, Lecture des (Débit, Crédit, Solde) plus facile",
    'version'     : "14.0.1.0",
    'category': 'Accounting/Localizations',

    'company'     : 'Elosys',
    'author'      : 'Elosys',
    'maintainer'  : 'Elosys',
    'support' : "support@elosys.net",
    'website'     : "http://www.elosys.net",

    "contributors": [
        "1 <Nassim REFES>",
        "2 <Kamel BENCHEHIDA>",
        "3 <Fatima MESSADI>",
        "4 <Youcef BENCHEHIDA>",
    ],

    'license'      : "OPL-1",
    'price'        : "25",
    'currency'     : 'Eur',
    'live_test_url': "https://www.elosys.net/shop/plan-des-comptes-32?category=6#attr=62",
    'images'       : [
        'images/banner.gif'
        ],

    'depends': [
            'base',
            'eloapps_account_fiscalyear',
            'l10n_dz_elosys',
    ],
    'data': [
        'data/l10n_dz_plan_comptable_report_data.xml',
        'views/report_l10n_dz_plan_comptable.xml',
        'views/l10n_dz_template.xml',
        'views/account_account.xml',
        'views/account_group.xml',
        'security/ir.model.access.csv',
    ],
    'qweb': [
        'static/src/xml/l10n_dz_plan_comptable_report_backend.xml',
    ],

    'installable': True,
    'auto_install': False,
    "application":False,
}
