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


class InvoiceReportXls(models.AbstractModel):
    _inherit = 'report.report_xlsx.abstract'
    _name = 'report.sea_report_xls.invoice_report_xls'

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

    # def report_ctx(self, invoice, location, picking):
    #     ctx = str()
    #     objs_invoice = self.env['account.invoice'].search([('id', 'in', invoice)])
    #     objs_location = self.env['stock.location'].search([('id', 'in', location)])
    #     name_lc = []
    #     name_invoice = []
    #     if objs_location:
    #         for lc in objs_location:
    #             name_lc.append(lc.display_name)
    #         ctx += ' Từ kho: (' + ', '.join(name_lc) + ')   '
    #     if objs_invoice:
    #         for invoice in objs_invoice:
    #             name_invoice.append(invoice.name)
    #         ctx += ' Sản phẩm: (' + ', '.join(name_invoice) + ')   '
    #     return ctx

    @api.model
    def generate_xlsx_report(self, workbook, data, wizard):
        objs_invoice = self.env['account_invoice', 'product_template', 'account_invoice_line'].search([('id', 'in', data['ids'])]).sorted('account_invoice_id')
        report_name = _('TỔNG HỢP MẶT HÀNG CHUYỂN KHO THEO NGÀY')
        report_ctx = self.report_ctx(data['account_invoice'], data['product_template'], data['account_invoice_line'])
        worksheet1 = workbook.add_worksheet(_('BÁO CÁO CHUYỂN KHO THEO NGÀY'))
        # company_name = self.env.user.company_id.display_name
        # company_street = self.env.user.company_id.street
        # company_street2 = self.env.user.company_id.street2
        # company_city = self.env.user.company_id.city
        # company_country = self.env.user.company_id.country_id.name
        # company_phone = self.env.user.company_id.phone
        # company_mail = self.env.user.company_id.catchall
        # company_logo = io.BytesIO(base64.b64decode(self.env.user.company_id.logo))
        # website = self.env.user.company_id.website

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
        f11 = workbook.add_format({'border': 1, 'valign': 'vcenter', 'text_wrap': True})
        f12 = workbook.add_format(
            {'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'num_format': '0.000'})
        money = workbook.add_format({'border': 1, 'align': 'center', 'valign': 'vcenter', 'num_format': '#,##0'})
        percent = workbook.add_format({'border': 1, 'num_format': 9, 'align': 'center', 'valign': 'vcenter', })
        row_no = 0
        col_no = 0

        # Report header
        worksheet1.set_column(0, 0, 5)
        worksheet1.set_column(1, 2, 13)
        worksheet1.set_column(3, 3, 18)
        worksheet1.set_column(4, 5, 22)
        worksheet1.set_column(6, 6, 8)
        worksheet1.set_column(7, 7, 30)
        worksheet1.set_column(8, 8, 8)
        worksheet1.set_column(9, 9, 12)
        worksheet1.set_column(10, 10, 7)
        worksheet1.set_column(11, 11, 12)
        worksheet1.set_column(12, 12, 15)
        worksheet1.set_column(14, 14, 12)
        worksheet1.set_column(16, 16, 12)
        worksheet1.freeze_panes(10, 2)
        worksheet1.autofilter(9, 0, 9, 14)
        # worksheet1.insert_image(row_no, 1, "company_logo.png",
        #                         {'image_data': company_logo, 'x_scale': 0.19, 'y_scale': 0.17})
        # worksheet1.merge_range(row_no, 2, row_no + 1, 14, company_name, f1)
        # row_no += 2
        # worksheet1.merge_range(row_no, 2, row_no, 16,
        #                        _('Địa chỉ: ') + company_street + _(', ') + str(company_street2) + _(', ') + str(
        #                            company_city) + _(', ') + str(company_country), f2)
        # row_no += 1
        # worksheet1.merge_range(row_no, 2, row_no, 16,
        #                        _('Điện thoại: ') + str(company_phone) + _('     Email: ') + company_mail, f2)
        # row_no += 1
        # worksheet1.merge_range(row_no, 2, row_no, 16, website, f2)
        # row_no += 3
        # worksheet1.merge_range(row_no, 0, row_no, 1, _('Từ ngày: ') + str(wizard.date_from), f5)
        # worksheet1.merge_range(row_no, 2, row_no, 16, report_name, f3)
        # row_no += 1
        worksheet1.merge_range(row_no, 0, row_no, 1, _('Đến ngày: ') + str(wizard.date_to), f5)
        worksheet1.merge_range(row_no, 2, row_no, 16, report_ctx if report_ctx else ' ', f5)
        row_no += 1

        # Report worksheet1
        # Header Of Table Data
        worksheet1.write(row_no, col_no, _('STT'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Số hóa đơn'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Người mua hàng'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Tên đơn vị'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Mã số thuế'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Địa chỉ xuất hóa đơn'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Email'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Số tài khoản'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Nơi mở'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Hình thức thanh toán'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Tiền tệ'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Bán hàng qua điện thoại'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Ghi chú'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Tên hàng hóa'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Đơn vị tính'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Số lượng'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Đơn giá'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Thành tiền'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Thuế xuất'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Tiền thuế'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Tổng tiền'), f6)

        # End Of Header Table Data
        sheet_row = row_no
        quantity = 0
        value = 0
        seq = 0
        quantity_remarks = 0
        quantity_price = 0
        for invoice in objs_invoice:
            for line in invoice:
                sheet_col = 0
                sheet_row += 1
                seq += 1
                worksheet1.write(sheet_row, sheet_col, seq, f4)
                sheet_col += 1
                worksheet1.write(sheet_row, sheet_col, self.conver_timezone(line.date)[0:10], f4)
                sheet_col += 1
                if line.picking_id.date_done:
                    worksheet1.write(sheet_row, sheet_col, self.conver_timezone(line.picking_id.date_done)[0:10], f4)
                else:
                    worksheet1.write(sheet_row, sheet_col, '*', f4)
                sheet_col += 1
                worksheet1.write(sheet_row, sheet_col,
                                 line.picking_id.display_name if line.picking_id.display_name else _('Hao hụt'), f4)
                sheet_col += 1
                worksheet1.write(sheet_row, sheet_col, line.location_id.display_name, f4)
                sheet_col += 1
                worksheet1.write(sheet_row, sheet_col, line.location_dest_id.display_name, f4)
                sheet_col += 1
                worksheet1.write(sheet_row, sheet_col, line.product_id.code, f4)
                sheet_col += 1
                worksheet1.write(sheet_row, sheet_col, line.product_id.name, f11)
                sheet_col += 1
                worksheet1.write(sheet_row, sheet_col, line.product_uom_id.name, f4)
                sheet_col += 1
                worksheet1.write(sheet_row, sheet_col, line.qty_done, f12)
                sheet_col += 1
                worksheet1.write(sheet_row, sheet_col, line.remarks, f12)
                sheet_col += 1
                worksheet1.write(sheet_row, sheet_col, line.product_id.standard_price, money)
                sheet_col += 1
                worksheet1.write(sheet_row, sheet_col, line.qty_done * line.product_id.standard_price or '0', money)
                sheet_col += 1
                worksheet1.write(sheet_row, sheet_col, line.origin or '', f4)
                sheet_col += 1
                if line.lot_id.name != False:
                    worksheet1.write(sheet_row, sheet_col, line.lot_id.name, f12)
                else:
                    worksheet1.write(sheet_row, sheet_col, '', f12)

                sheet_col += 1
                worksheet1.write(sheet_row, sheet_col, line.product_id.lst_price, money)
                sheet_col += 1
                worksheet1.write(sheet_row, sheet_col, line.qty_done * line.product_id.lst_price or '0', money)
                # if str(line.origin).find('PO') != -1:
                #     worksheet1.write(sheet_row, sheet_col, line.product_id.lst_price, money)
                #     sheet_col += 1
                #     worksheet1.write(sheet_row, sheet_col, line.qty_done * line.product_id.lst_price or '0', money)
                # else:
                #     worksheet1.write(sheet_row, sheet_col, '', money)
                #     sheet_col += 1
                #     worksheet1.write(sheet_row, sheet_col, '', money)
                # quantity_price += line.product_id.lst_price
                quantity += line.qty_done
                value += (line.qty_done * line.product_id.standard_price)
        sheet_row += 1
        worksheet1.merge_range(sheet_row, 0, sheet_row, 8, _('TỔNG CỘNG'), f3)
        worksheet1.write(sheet_row, 9, quantity, f4)
        worksheet1.write(sheet_row, 10, '', f4)
        worksheet1.write(sheet_row, 11, '', money)
        worksheet1.write(sheet_row, 12, abs(value), money)
        worksheet1.write(sheet_row, 13, '', f4)
        worksheet1.write(sheet_row, 14, '', f4)
        worksheet1.write(sheet_row, 15, '', f4)
        worksheet1.write(sheet_row, 16, '', f4)
        worksheet1.merge_range(sheet_row + 2, 0, sheet_row + 2, 4, _('____, ____/____/20___'), f8)
        worksheet1.merge_range(sheet_row + 2, 6, sheet_row + 2, 15, _('____, ____/____/20___'), f8)
        worksheet1.merge_range(sheet_row + 3, 0, sheet_row + 3, 4, _('Trưởng phòng'), f9)
        worksheet1.merge_range(sheet_row + 3, 6, sheet_row + 3, 15, 'Người lập', f9)
        worksheet1.merge_range(sheet_row + 4, 0, sheet_row + 4, 4, '(Ký, họ tên)', f10)
        worksheet1.merge_range(sheet_row + 4, 6, sheet_row + 4, 15, '(Ký, họ tên)', f10)