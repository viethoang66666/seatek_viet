# -*- coding: utf-8 -*-
import pytz, datetime
from pytz import timezone
from datetime import timedelta
from odoo import models, fields, api, exceptions, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import ValidationError


class WizardInvoiceReport(models.TransientModel):
    _name = 'sea_report_xls.invoice_report.wizard'

    # @api.onchange('location_ids')
    # def _default_picking_type(self):
    #     self.picking_type_ids = [(5, 0, 0)]
    #     if self.location_ids:
    #         domain_ids = []
    #         location_src = self.env['stock.picking.type'].search(
    #             [('default_location_src_id', 'in', self.location_ids.ids)])
    #         domain_ids += location_src.ids
    #         location_dest = self.env['stock.picking.type'].search(
    #             [('default_location_dest_id', 'in', self.location_ids.ids)])
    #         domain_ids += location_dest.ids
    #         return {'domain': {'picking_type_ids': [('id', 'in', domain_ids)]}}
    #     else:
    #         return {'domain': {'picking_type_ids': []}}

    @api.constrains('date_from', 'date_to')
    def _constrain_dates(self):
        for rec in self:
            if rec.date_from > rec.date_to:
                raise ValidationError(_('Date From must be greater than date To!'))

    date_from = fields.Date(string='Date From', default=fields.Date.today() - timedelta(days=1))
    date_to = fields.Date(string='Date To', default=fields.Date.today())

    invoice_ids = fields.Many2many('account.invoice', 'report_account_invoice_xls_invoice_rel', 'wizard_id',
                                           'invoice_id', 'Account Invoice')
    # account_invoice_line_ids = fields.Many2many('account.invoice.line', 'report_account_invoice_line_xls_invoice_rel', 'wizard_id',
    #                                             'account_invoice_line_id', 'Account Invoice Line')
    # account_invoice_line_tax_ids = fields.Many2many('account.invoice.line.tax', 'report_account_invoice_line_tax_xls_invoice_rel', 'wizard_id',
    #                                        'account_invoice_line_tax_id', 'Account Invoice Line Tax')
    # account_tax_ids = fields.Many2many('account.tax', 'report_account_tax_xls_invoice_rel', 'wizard_id',
    #                                                 'account_tax_id', 'Account Tax')
    # product_template_ids = fields.Many2many('product.template', 'report_product_template_xls_product_rel', 'wizard_id',
    #                                         'product_template_id', 'Product Template')
    # res_currency_ids = fields.Many2many('res.currency', 'report_res_currency_xls_product_rel', 'wizard_id',
    #                                         'res_currency_id', 'Res Currency')
    # res_partner_ids = fields.Many2many('res.partner', 'report_res_partner_xls_product_rel', 'wizard_id',
    #                                     'res_partner_id', 'Res Partner')
    # uom_uom_ids = fields.Many2many('res.partner', 'report_uom_uom_xls_product_rel', 'wizard_id',
    #                                    'uom_uom_id', 'Uom Uom')

    # location_ids = fields.Many2many('stock.location', 'report_stock_move_xls_location_rel', 'wizard_id', 'warehouse_id',
    #                                 'Location', domain=[('usage', 'in', ('internal', 'transit'))])
    # picking_type_ids = fields.Many2many('stock.picking.type', 'report_stock_move_xls_picking_type_rel', 'wizard_id',
    #                                     'warehouse_id', 'Picking Type')
    # warehouse_ids = fields.Many2many('stock.warehouse', 'report_stock_move_xls_warehosue_rel', 'wizard_id',
    #                                  'warehouse_id', 'Warehouse')

    @api.model
    def conver_timezone(self, var):
        user = self.env["res.users"].browse(self._uid)
        tz = timezone(user.tz)
        c_time = datetime.datetime.now(tz)
        hour_tz = int(str(c_time)[-5:][:2])
        min_tz = int(str(c_time)[-5:][3:])
        sign = str(c_time)[-6][:1]
        if sign == '+':
            var_time = datetime.datetime.strptime(str(var), DEFAULT_SERVER_DATETIME_FORMAT) - timedelta(hours=hour_tz,
                                                                                                        minutes=min_tz)
        else:
            var_time = datetime.datetime.strptime(str(var), DEFAULT_SERVER_DATETIME_FORMAT) + timedelta(hours=hour_tz,
                                                                                                        minutes=min_tz)
        return str(var_time)

    @api.multi
    def find_objs(self):
        date_from = datetime.datetime(year=self.date_from.year, month=self.date_from.month, day=self.date_from.day,
                                      hour=0, minute=0, second=0)
        date_to = datetime.datetime(year=self.date_to.year, month=self.date_to.month, day=self.date_to.day, hour=23,
                                    minute=59, second=59)
        search_obj = [('date', '>=', self.conver_timezone(date_from)), ('date', '<=', self.conver_timezone(date_to)),
                       ('state', '=', 'done')]
        search_invoice = ('invoice_id.id', 'in', self.account_invoice_ids.ids)

        if self.invoice_ids:
            search_obj.append(search_invoice)
            obj_search = self.env['account.invoice'].search(search_obj + search_invoice)
        else:
            obj_search = self.env['account.invoice'].search(search_obj)
        if not obj_search:
            raise ValidationError(_('The period choose has no data to report! Please select a different time period.'))
        else:
            return obj_search

    @api.multi
    def view_report(self):
        self.ensure_one()
        if not self.env.user.tz:
            raise ValidationError(_('Please contact Administrator to configure your time zone!!!'))
        else:
            data = self.read()[0]
            obis_invoice = self.find_objs()
            dataset = {
                'ids': obis_invoice.ids,
                'model': 'account.invoice',
                'form': data,
                'account_invoice': self.account_invoice_ids,
            }
            return self.env['ir.actions.report'].search(
                [('report_name', '=', 'sea_report_xls.invoice_report_xls'),
                 ('report_type', '=', 'xlsx')],
                limit=1).report_action(self, data=dataset)
