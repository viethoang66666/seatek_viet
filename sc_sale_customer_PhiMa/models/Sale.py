from odoo import models, fields, api


class STKCustomer(models.Model):
    _inherit = ['sale.order']

    CustomerInquiryNo = fields.Char(string='Customer Inquiry No', store=True, default="")

    CustomerInquiryDate = fields.Date(string='Customer InquiryDate', store=True)

    CustomerPONo = fields.Char(string='CustomerPO No', store=True, default="")

    CustomerOrderDate = fields.Date(string='Order Date', store=True)



