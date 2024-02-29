{
    'name': "School Mangement Module",
    'version': '16.0.0',
    'depends': ['base'],
    'author': "Djamel Hemch",
    'category': 'Management',
    'description': """This module will add a record to store students details
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/menu.xml',
        'views/students_view.xml'
    ],
    # data files containing optionally loaded demonstration data
    'demo': [],
    'installable' : True,
    'auto_install' : False,
    'license': 'AGPL-3',
}