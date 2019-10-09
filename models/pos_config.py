from odoo import fields, models, _


class POSConfigFiscalPrinterJournalCode(models.Model):
    _name = 'pos.config.fiscal_printer.journal_code'
    _description = '''Relation between account.journal and the printer code.'''

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
    _description = '''Relation between tax and printer code.'''

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
        config_parameter='point_of_sale.fiscal_printer.file_path',  # TODO REM
        string=_("File path"),
    )
    fp_tax_ids = fields.Many2many(
        comodel_name='pos.config.fiscal_printer.tax_code',  # TODO REM
        string=_('Taxes Codes'),
    )
    fp_cutter_receipt_paper = fields.Boolean(
        config_parameter='point_of_sale.fiscal_printer.cutter_receipt_paper',  # TODO REM
        string=_('Cutter Receipt Paper'),
    )
    fp_open_cash_drawer = fields.Boolean(
        config_parameter='point_of_sale.fiscal_printer.open_cash_drawer',  # TODO REM
        string=_('Open Cash Drawer'),
    )
    fp_order_suffix = fields.Char(
        string=_('Order suffix'),
    )
