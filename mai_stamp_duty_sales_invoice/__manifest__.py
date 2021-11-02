{
    'name': 'Stamp Duty on Cash payment in sale and Invoice || Stamp Duty on Cash Payment',
    'version': '14.1.1.1',
    'category': 'Sales',
    'sequence': 1,
    'summary': 'Moroccan Stamp Duty on Cash payment in sale and Invoice',
    'currency': 'EUR',
    'description': 
     """ 
        Moroccan Stamp Duty on Cash payment in sale and Invoice
     """,
    "author" : "MAISOLUTIONSLLC",
    "email": 'apps@maisolutionsllc.com',
    "website":'http://maisolutionsllc.com/',
    'license': 'OPL-1',
    'price': 45,
    'depends': [
        "account",
        "sale_management"],
    'data': [
        'security/ir.model.access.csv',
        'views/stamp_duty_config_view.xml',
        'views/account_view.xml',
        'views/sale_order_view.xml',
        'views/invoice_report.xml',
    ],
    'demo': [],
    "live_test_url" : "https://youtu.be/zPPqfQS6bWw",
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'auto_install': False,
    'application': False,
}

