# -*- coding: utf-8 -*-
{
    'name': "Thêm 1 vài field Customer Inquiry vào màn hình Sale Order",

    'summary': """
        Thêm 1 vài field Customer Inquiry vào màn hình Sale Order""",

    'description': """
       Thêm 1 vài field Customer Inquiry vào màn hình Sale Order
    """,

    'author': "Seatek",
    'website': "https://www.seacorp.vn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'sale',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',

        'views/sale_view.xml',
    ],
    # only loaded in demonstration mode
}