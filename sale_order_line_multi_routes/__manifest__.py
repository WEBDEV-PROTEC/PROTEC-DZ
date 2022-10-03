{
    'name': "Multi Warehouse Auto Split Sale Order Line",
    'version': "1.0",
    'summary': "Sale Order Split line from multi-warehouse inventory",
    'sequence': 0,
    'category': "Sales/Sales",
    'description': "Split Sale Order Line",
    'website': 'https://www.vperfectcs.com',
    'author': "VperfectCS",
    'maintainer': 'VperfectCS',
    'depends': ["base_automation","sale_stock","stock"],
    'data': [
        "views/sale_order.xml",
        "data/sale_order_automated_action.xml",
         ],
    'demo': [],
    'qweb': [],
    "installable":True,
    "application":True,
    "auto_install":False,
    'price': 39,
    'currency': 'EUR'
}
