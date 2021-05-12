# -*- coding: utf-8 -*-
{
    'name': "Report XLSX - Invoice",
    'summary': """
        Export data to file excel""",
    'description': """
        General report Excel/CSV
                """,
    'author': "SeaTek",
    'website': "http://www.seatek.vn",
    'category': 'Seacorp',
    'version': '12.0.0.1',
    'depends': ['report_xlsx',
                'account',
    ],
    'data': [
        'reports/report_invoice_xls.xml',
    ],
    'installable': True,
    'auto_install': False,
}
