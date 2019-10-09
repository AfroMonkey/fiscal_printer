from odoo import fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_name_pos = fields.Char(
        string=_('Product name POS'),
    )
