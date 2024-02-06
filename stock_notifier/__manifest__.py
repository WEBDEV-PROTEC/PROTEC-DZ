# __manifest__.py

{
    'name': 'Stock Notification Tracker',
    'version': '1.0',
    'author': 'Djamel Hemch',
    'summary': 'Notify users about low stock products',
    'description': """
        This module sends notifications to users when products are below the specified stock threshold.
    """,
    'images': ['static/description/icon.png'],
    'depends': ['base', 'mail', 'product'],
    'data': [
        'views/stock_notification_cron.xml',
        'data/stock_notification_cron_data.xml',
    ],
    'installable': True,
    'application': True,
}
