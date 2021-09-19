# -*- coding: utf-8 -*-
{
    'name': 'Account Update Data',
    'summary': 'Customer Portal',
    'sequence': '',
    'category': '',
    'description': """""",
    'depends': ['mail', 'base'],
    'data': [
        'security/ir.model.access.csv',
        'data/update_ac_mail.xml',
        'wizard/update_acc_menu.xml'
    ],
    'qweb': [
    ],
}
