# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
{
    'name': "Droit de timbre - Algérie",
    'summary': """Gestion des droits de timbre pour les paiements en liquide sur les factures client""",

    'version': '14.0.1.0',
    'category': 'Accounting/Accounting',


    "contributors": [
        "1 <Djamel Eddine YAGOUB>",
        "2 <Nassim REFES>",
        "3 <Kamel BENCHEHIDA>",
        "4 <Yamina ZOUATINE>",
        "5 <Fatima MESSADI>",
    ],
    
    
    
    'company'     : 'Elosys',
    'author'      : 'Elosys',
    'maintainer'  : 'Elosys',

    'website': 'http://www.elosys.net',
    'support' : "support@elosys.net",

    #'live_test_url' : "https://www.elosys.net/shop",    


    "license": "OPL-1",
    "price": 105,
    "currency": 'EUR',


    'depends': [
        'base',
        'account'
    ],

    "sequence":1,

    'data': [
        'views/configuration_timbre.xml',
        'views/account_move.xml',
        'views/account_move_report.xml',
        'views/account_payment.xml',
        
        'security/ir.model.access.csv',

        'data/paymment_mode.xml',
    ],



    'images': ['images/baneer.gif'],



    'installable': True,
    'auto_install': False,
    'application': False,
    'post_init_hook': "post_init_hook",
}
