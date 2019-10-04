from odoo import api, fields, models, _

class POSConfigFiscalPrinterJournalCode(models.Model):
    _name = 'pos.config.fiscal_printer.journal_code'

    name = fields.Char(
        related='journal_id.name',
    )
    journal_id = fields.Many2one(
        comodel_name='account.journal',
        required=True,
        string='Journal',
    )
    code = fields.Integer(
        required=True,
    )

    # TODO constraints

class POSConfig(models.Model):
    _inherit = 'pos.config'

    fp_journal_ids = fields.Many2many(
        comodel_name='pos.config.fiscal_printer.journal_code',
        string='Journal Codes',
    )
