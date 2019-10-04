from odoo import fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # TODO move to POS Settings

    # TODO check valid path
    pos_fp_file_path = fields.Char(
        config_parameter='point_of_sale.fiscal_printer.file_path',
        string=_("File path"),
    )
    # payments TODO
    # TODO vat
    # TODO pos_fp_additional_product_text = fields.(
    #     config_parameter='point_of_sale.fiscal_printer.additional_product_text',
    #     string=_(''),
    # )
    # TODO pos_fp_additional_text = fields.(
    #     config_parameter='point_of_sale.fiscal_printer.additional_text',
    #     string=_(''),
    # )
    pos_fp_additional_text_plain = fields.Char(
        config_parameter='point_of_sale.fiscal_printer.additional_text_plain',
        string=_('Additional Text Plain'),
    )
    pos_fp_cutter_receipt_paper = fields.Boolean(
        config_parameter='point_of_sale.fiscal_printer.cutter_receipt_paper',
        string=_('Cutter Receipt Paper'),
    )
    pos_fp_open_cash_drawer = fields.Boolean(
        config_parameter='point_of_sale.fiscal_printer.open_cash_drawer',
        string=_('Open Cash Drawe'),
    )
