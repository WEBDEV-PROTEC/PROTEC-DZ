
{
    'name': 'Customer Credit Management App',
    'author': 'Edge Technologies',
    'version': '14.0.1.0',
    'live_test_url':'https://youtu.be/0FcTkaU_WQw',
    "images":['static/description/main_screenshot.png'],
    'summary': 'Customer credit limit on customer payment limit partner credit limit on partner payment limit customer credit balance customer credit management customer credit payment limit vendor credit customer credit hold customer overdue limit customer due limit',
    'description': "Odoo credit management app",
    "license" : "OPL-1",
    'depends': [
        'base',
        'sale',
        'sale_management',
        'stock'
    ],
    'data': [
    	'security/security.xml',
    	'views/inherited_res_partner_view.xml',
        'views/inherited_sale_order_view.xml',
        
    ],
    'qweb' : [],
    'demo': [],
    'css': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 48,
    'currency': "EUR",
    'category': 'Sales',
}
