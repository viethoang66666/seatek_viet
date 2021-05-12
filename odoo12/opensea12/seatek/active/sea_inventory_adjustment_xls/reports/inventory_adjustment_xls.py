import base64
import pytz, io, base64, datetime
from pytz import timezone
from datetime import timedelta
import logging
from odoo import models, api
from odoo.tools.translate import _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

_logger = logging.getLogger(__name__)


class InventoryAdjustmentXLS(models.AbstractModel):
    _name = 'report.sea_inventory_adjustment_xls.inventory_adjustment_xls'
    _inherit = 'report.report_xlsx.abstract'

    @api.model
    def conver_timezone(self, var):
        user = self.env["res.users"].browse(self._uid)
        tz = timezone(user.tz)
        c_time = datetime.datetime.now(tz)
        hour_tz = int(str(c_time)[-5:][:2])
        min_tz = int(str(c_time)[-5:][3:])
        sign = str(c_time)[-6][:1]
        if sign == '+':
            var_time = datetime.datetime.strptime(str(var), DEFAULT_SERVER_DATETIME_FORMAT) + timedelta(hours=hour_tz,
                                                                                                        minutes=min_tz)
        else:
            var_time = datetime.datetime.strptime(str(var), DEFAULT_SERVER_DATETIME_FORMAT) - timedelta(hours=hour_tz,
                                                                                                        minutes=min_tz)
        return str(var_time)


    def generate_xlsx_report(self, workbook, data, objects):
        workbook.set_properties({'comments': 'Created with Python and XlsxWriter from Odoo 11.0'})
        worksheet1 = workbook.add_worksheet('Inventory Adjustment')
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
        f6 = workbook.add_format({'bold': 1, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True,  'bg_color': '#FFFFCC'})
        f7 = workbook.add_format({'bottom': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
        f8 = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
        f9 = workbook.add_format({'bold': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
        f10 = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'italic': True})
        f11 = workbook.add_format({'border': 1, 'valign': 'vcenter', 'text_wrap': True})
        f12 = workbook.add_format(
            {'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'num_format': '0.000'})
        money = workbook.add_format({'border': 1, 'align': 'center', 'valign': 'vcenter', 'num_format': '#,##0'})
        percent = workbook.add_format({'border': 1, 'num_format': 9, 'align': 'center', 'valign': 'vcenter', })
        row_no = 2
        col_no = 0

        # Report header
        worksheet1.set_column(0, 0, 15)
        worksheet1.set_column(1, 1, 50)
        worksheet1.set_column(2, 2, 13)
        worksheet1.set_column(3, 3, 13)
        worksheet1.set_column(4, 4, 13)
        worksheet1.set_column(5, 5, 18)
        worksheet1.set_column(6, 6, 13)
        worksheet1.set_column(7, 7, 18)
        worksheet1.set_column(8, 8, 15)
        worksheet1.set_column(9, 9, 18)

        worksheet1.insert_image(0, 2, "company_logo.png",
                                {'image_data': company_logo, 'x_scale': 0.22, 'y_scale': 0.20})
        worksheet1.merge_range(row_no - 1, 2, row_no, 9, company_name, f1)
        row_no += 1
        worksheet1.merge_range(row_no, 2, row_no, 9, _('Địa chỉ: ') + company_street + _(', ') + str(company_street2) + _(', ') + str(company_city) + _(', ') + str(company_country), f2)
        row_no += 1
        worksheet1.merge_range(row_no, 2, row_no, 9, _('Điện thoại: ') + str(company_phone) + _('     Email: ') + company_mail, f2)
        row_no += 1
        worksheet1.merge_range(row_no, 2, row_no, 9, website, f2)
        row_no += 3
        worksheet1.merge_range(row_no, 0, row_no + 1, 0, _('Date'), f6)
        worksheet1.merge_range(row_no, 1, row_no, 3, _('Product Information'), f6)
        worksheet1.merge_range(row_no, 4, row_no, 5, _('Theoretical'), f6)
        worksheet1.merge_range(row_no, 6, row_no, 7, _('Real'), f6)
        worksheet1.merge_range(row_no, 8, row_no, 9, _('Difference'), f6)
        row_no += 1
        col_no += 1

        worksheet1.write(row_no, col_no, _('Product Name'), f4)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Lot/Serial No.'), f4)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Unit Price'), f4)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Quantity'), f4)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Inventory Cost'), f4)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Quantity'), f4)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Inventory Cost'), f4)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Quantity Difference'), f4)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Amount Difference'), f4)
        row_no += 1

        for o in objects:
            sheet_row = row_no
            worksheet1.merge_range(7, 0, 7, 9, o.name, f3)
            for ch in o.line_ids:
                worksheet1.write(sheet_row, 0, self.conver_timezone(o.date)[0:10], f11)
                worksheet1.write(sheet_row, 1, ch.product_id.display_name, f11)
                worksheet1.write(sheet_row, 2, ch.prod_lot_id.name or '', f11)
                worksheet1.write(sheet_row, 3, ch.product_id.standard_price, money)
                worksheet1.write(sheet_row, 4, ch.theoretical_qty, f11)
                worksheet1.write(sheet_row, 5, abs(ch.product_id.standard_price*ch.theoretical_qty), money)
                if o.state == 'done':
                    worksheet1.write(sheet_row, 6, ch.product_qty, f11)
                else:
                    worksheet1.write(sheet_row, 6, '', f11)
                if o.state == 'done':
                    worksheet1.write(sheet_row, 7, abs(ch.product_id.standard_price*ch.product_qty), money)
                else:
                    worksheet1.write(sheet_row, 7, '', f11)
                if o.state == 'done':
                    worksheet1.write(sheet_row, 8, abs(ch.theoretical_qty - ch.product_qty), f11)
                else:
                    worksheet1.write(sheet_row, 8, '', f11)
                if o.state == 'done':
                    worksheet1.write(sheet_row, 9, abs((ch.theoretical_qty - ch.product_qty)*ch.product_id.standard_price), money)
                else:
                    worksheet1.write(sheet_row, 9, '', f11)
                sheet_row += 1
        worksheet1.merge_range(sheet_row + 2, 0, sheet_row + 2, 4, _('____, ____/____/20___'), f8)
        worksheet1.merge_range(sheet_row + 2, 5, sheet_row + 2, 9, _('____, ____/____/20___'), f8)
        worksheet1.merge_range(sheet_row + 3, 0, sheet_row + 3, 4, _('Trưởng phòng'), f9)
        worksheet1.merge_range(sheet_row + 3, 5, sheet_row + 3, 9, 'Người lập', f9)
        worksheet1.merge_range(sheet_row + 4, 0, sheet_row + 4, 4, '(Ký, họ tên)', f10)
        worksheet1.merge_range(sheet_row + 4, 5, sheet_row + 4, 9, '(Ký, họ tên)', f10)