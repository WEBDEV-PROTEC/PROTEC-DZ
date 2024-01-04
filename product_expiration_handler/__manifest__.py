# -*- coding: utf-8 -*-
{
    'name': "product_expiration",
    'summary': """Handles product expirations time""",
    'author': "Djamel Hemch",
    'category': 'Uncategorized',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['purchase', 
        'stock'],
    # always loaded
    'data': [
        'views/purchase_order_view.xml',
        'views/product_normal_view.xml'
    ],
}