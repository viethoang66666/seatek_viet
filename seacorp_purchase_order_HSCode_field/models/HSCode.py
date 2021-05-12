from odoo import models, fields, api

class PurchaseOrderHSCodeLine(models.Model):
    _inherit = 'purchase.order.line'

    HSCode = fields.Text(string='HS Code', store=True, default="")
