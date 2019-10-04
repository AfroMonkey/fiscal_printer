from odoo import api, fields, models, _

class POSConfigFiscalPrinterJournalCode(models.Model):
    _name = 'pos.config.fiscal_printer.journal_code'

    name = fields.Char(
        related='journal_id.name',
    )
    journal_id = fields.Many2one(
        comodel_name='account.journal',
        required=True,
        string=_('Journal'),
    )
    code = fields.Integer(
        required=True,
    )

    # TODO IMP constraints

class POSConfigFiscalTaxCode(models.Model):
    _name = 'pos.config.fiscal_printer.tax_code'

    name = fields.Char(
        related='tax_id.name',
    )
    tax_id = fields.Many2one(
        comodel_name='account.tax',
        required=True,
        string=_('Tax'),
    )
    code = fields.Integer(
        required=True,
    )

    # TODO IMP constraints

class POSConfig(models.Model):
    _inherit = 'pos.config'

    fp_journal_ids = fields.Many2many(
        comodel_name='pos.config.fiscal_printer.journal_code',
        string=_('Journals Codes'),
    )    
    fp_product_additional_text_ids = fields.Many2many(
        comodel_name='ir.model.fields',
        string=_('Product Additional Text'),
        domain=[('model', '=', 'product.template')],
    )
    fp_additional_text = fields.Text(
        string=_('Additional Text'),
    )
    # TODO IMP check valid path
    fp_file_path = fields.Char(
        string=_("File path"),
    )
    fp_tax_ids = fields.Many2many(
        string=_('Taxes Codes'),
    )
    fp_cutter_receipt_paper = fields.Boolean(
        string=_('Cutter Receipt Paper'),
    )
    fp_open_cash_drawer = fields.Boolean(
        string=_('Open Cash Drawe'),
    )
    fp_order_suffix = fields.Char(
        string=_('Order suffix'),
    )
