# -*- coding: utf-8 -*-
import pytz, io, base64, datetime
from pytz import timezone
from datetime import timedelta
from base64 import b64decode
from logging import getLogger
from PIL import Image
from io import StringIO
from odoo import models, fields, api, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class InventoryAdjustmentXLS(models.AbstractModel):
    _name = 'report.sea_inventory_adjustment_pdf.inventory_adjustment_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data):
        worksheet1 = workbook.add_worksheet(_('BÁO CÁO CHUYỂN KHO THEO NGÀY'))
        company_name = self.env.user.company_id.display_name
        company_street = self.env.user.company_id.street
        company_street2 = self.env.user.company_id.street2
        company_city = self.env.user.company_id.city
        company_country = self.env.user.company_id.country_id.name
        company_phone = self.env.user.company_id.phone
        company_mail = self.env.user.company_id.catchall
        company_logo = io.BytesIO(base64.b64decode(self.env.user.company_id.logo))
        website = self.env.user.company_id.website

        f1 = workbook.add_format(
            {'bold': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 24})
        f2 = workbook.add_format(
            {'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 10, 'italic': True})
        f3 = workbook.add_format(
            {'bold': 1, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 18})
        f4 = workbook.add_format({'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
        f5 = workbook.add_format(
            {'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 9, 'italic': True})
        f6 = workbook.add_format({'bold': 1, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
        f7 = workbook.add_format({'bottom': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
        f8 = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
        f9 = workbook.add_format({'bold': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
        f10 = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'italic': True})
        f11 = workbook.add_format({'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
        money = workbook.add_format({'border': 1, 'align': 'center', 'valign': 'vcenter', 'num_format': '#,##0'})
        percent = workbook.add_format({'border': 1, 'align': 'center', 'valign': 'vcenter', 'num_format': 9})
        row_no = 2
        col_no = 0

# Report Header
        worksheet1.set_column(0, 0, 20)
        worksheet1.set_column(1, 1, 30)
        worksheet1.set_column(2, 2, 15)
        worksheet1.set_column(3, 3, 13)
        worksheet1.set_column(4, 4, 10)
        worksheet1.set_column(5, 5, 18)
        worksheet1.set_column(6, 6, 10)
        worksheet1.set_column(7, 7, 18)
        worksheet1.set_column(8, 8, 10)
        worksheet1.set_column(9, 9, 18)

        worksheet1.insert_image(0, 2, "company_logo.png", {'image_data': company_logo, 'x_scale': 0.22, 'y_scale': 0.20})
        worksheet1.merge_range(row_no - 1, 2, row_no, 9, company_name, f1)
        row_no += 1
        worksheet1.merge_range(row_no, 2, row_no, 9, _('Địa chỉ: ') + company_street + _(', ') + str(company_street2) + _(', ') + str(company_city) + _(', ') + str(company_country), f2)
        row_no += 1
        worksheet1.merge_range(row_no, 2, row_no, 9, _('Điện thoại: ') + str(company_phone) + _('     Email: ') + company_mail, f2)
        row_no += 1
        worksheet1.merge_range(row_no, 2, row_no, 9, website, f2)
        row_no += 2
        worksheet1.merge_range(row_no, 2, row_no, 9, _('NAME'), f3)
        row_no += 2

# Header Data
        worksheet1.merge_range(row_no, 0, row_no + 1, 0, _('Date'), f6)