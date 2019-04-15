# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Equitania Product Translation',
    'license': 'AGPL-3',
    'version': '1.0.1',
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    'depends': ['base_setup', 'product'],
    'category' : 'General Improvements',
    'summary': 'Module for translating product name and description from German to English',

    'data': [
        #"security/ir.model.access.csv"
        'views/eq_product_template.xml',
        "views/templates.xml",

    ],
    'demo': [],
    'css': ['base.css'],
    'installable': True,
    'auto_install': False,
}
