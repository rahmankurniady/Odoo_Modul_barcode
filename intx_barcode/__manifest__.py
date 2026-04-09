# -*- coding: utf-8 -*-
{
    'name': "intx_barcode",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "PT Internex Indonesia",
    'website': "https://internex.co.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Internex Modul',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/picking_view.xml',
        'views/picking_scan_wizard_view.xml'
    ],
    'assets': {
    'web.assets_backend': [
        'intx_barcode/static/src/js/barcode_enter.js',
        ],
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}

