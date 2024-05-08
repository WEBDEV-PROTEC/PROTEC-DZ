{
    'name': 'YALIDINE Odoo Integration Module',
    'version': '14.0.1.0.0',
    'summary': 'Integrate Odoo with YALIDINE for delivery tracking.',
    'author': 'Djamel Hemch (Protec DZ)',
    'category': 'Uncategorized',
    'depends': ['base', 'web'],
    'data': [
        'views/delivery_history_template.xml',
        'views/history_assets.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'auto_install': False,
}
