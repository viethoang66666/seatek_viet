import base64
import pytz, io, base64, datetime

from pylint.checkers.typecheck import _

from odoo import models


class InvoiceReportXls(models.AbstractModel):
    _name = 'report.sea_invoice_xls.report_invoice_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):

        sheet = workbook.add_worksheet('Invoice')


        f1 = workbook.add_format(
            {'bold': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})

        row_no = 0
        col_no = 0

        sheet.write(row_no, col_no, 'STT', f1)
        col_no +=1
        sheet.write(row_no, col_no, 'Ho tên người mua hàng', f1)
        col_no += 1
        sheet.write(row_no, col_no, 'Mã số thuế', f1)
        col_no += 1
        sheet.write(row_no, col_no, 'Đia chỉ xuất hóa đơn', f1)
        col_no += 1
        sheet.write(row_no, col_no, 'Email', f1)
        col_no += 1
        sheet.write(row_no, col_no, 'Số tài khoản', f1)
        col_no += 1
        sheet.write(row_no, col_no, 'Nơi mở', f1)
        col_no += 1
        sheet.write(row_no, col_no, 'Hình thức thanh toán', f1)
        col_no += 1
        sheet.write(row_no, col_no, 'Tiền tệ', f1)
        col_no += 1
        sheet.write(row_no, col_no, 'Bán hàng qua điện thoại', f1)
        col_no += 1
        sheet.write(row_no, col_no, 'Ghi chú', f1)