from odoo import api, models

CHUNK_SIZE = 24


def commafile(value):
    '''Return numbers with comma instead of decimal point.'''
    return str(value).replace('.', ',')


def to_chunks(string: str, width: int):
    '''Split a string in chunks of size width.'''
    return [string[y-width:y] for y in range(width, len(string)+width, width)]


class FiscalPrinter(models.TransientModel):
    _name = 'fiscal.printer'
    _description = '''Assistant model to make the files for fiscal printer.'''

    @api.model
    def print_file(self, rows, payment_lines):
        '''Generate text file with the fiscal printer commands based on POS'''
        ProductProduct = self.env['product.product']
        pos_config = self.env['pos.config'].search([], limit=1)  # TODO IMP multiple stores
        for row in rows:
            row['name'] = ProductProduct.browse(row['id']).product_name_pos

        # OPEN FISCAL RECEIPT
        content = '1020;1\n'
        # ROW PRODUCT SALE
        discount_amount = 0
        surcharge = 0
        subtotal_discount = ''
        for row in rows:
            product = ProductProduct.browse(row['id'])
            if pos_config.discount_product_id and pos_config.discount_product_id == product:
                discount = abs(row['price'])
                subtotal_discount = '1025;2;1;Discount {discount};{discount}\n'.format(discount=commafile(discount))
                continue
            # TODO IMP check , instead of .
            vat_id = product.taxes_id[0]  # TODO IMP multiple taxes
            vat_code = pos_config.fp_tax_ids.search([('tax_id', '=', vat_id.id)]).code
            if row['qty'] == 1:  # Ignore qty if is == 1
                content += '1021;1;;{vat};;;{name};{price}\n'.format(vat=vat_code, name=row['name'], price=commafile(row['price']))
            else:
                content += '1021;1;;{vat};;;{name};{price};{qty}\n'.format(vat=vat_code, name=row['name'], price=commafile(row['price']), qty=commafile(row['qty']))
            # ADDITIONAL PRODUCT TEXT
            additional_text = ''
            for field in pos_config.fp_product_additional_text_ids:
                additional_text += product[field.name].name
            for chunk in to_chunks(additional_text, CHUNK_SIZE):
                content += '112;{};0;1;3\n'.format(chunk)
            # PRODUCT DISCOUNT
            if row.get('discount'):
                discount_amount = row['price'] * row['qty'] * row['discount'] / 100
                content += '1025;2;1;Discount {discount}%;{discount_amount}\n'.format(discount=commafile(row['discount']), discount_amount=commafile(discount_amount))
            # PRODUCT SURCHARGE
            surcharge = 0  # TODO IMP
            if surcharge:
                surcharge_text = ''  # TODO IMP
                content += '1025;4;1;{surcharge_text};{surcharge}\n'.format(surcharge_text=surcharge_text, surcharge=surcharge)
        # SUBTOTAL
        if subtotal_discount:
            content += '1028\n'
        # SUBTOTAL DISCOUNT
        if subtotal_discount:
            content += commafile(subtotal_discount)
        # TODO IMP SUBTOTAL SURCHARGE
        # PAYMENT METHOD
        # TODO IMP multiple methods
        for payment_line in payment_lines:
            payment_code = pos_config.fp_payment_method_code_ids.search([('method_id', '=', payment_line['method_id'])]).code
            cash = payment_line['amount'] or ''
            content += '1030;{payment_code};1;;{cash}\n'.format(payment_code=payment_code, cash=commafile(cash))
        # ADDITIONAL TEXT
        additional_text = pos_config.fp_additional_text or ''
        for chunk in to_chunks(additional_text, CHUNK_SIZE):
            content += '112;{};0;1;3\n'.format(chunk)
        # CUTTER RECEIPT PAPER
        cutter_receipt_paper = pos_config.fp_cutter_receipt_paper
        if cutter_receipt_paper:
            content += '115\n'
        # OPEN CASH DRAWER
        open_cash_drawer = pos_config.fp_open_cash_drawer
        if open_cash_drawer:
            content += '1029;1\n'
        file_path = pos_config.fp_file_path
        with open(file_path, 'w', newline='\r\n') as file_output:
            file_output.write(content)
        print(content)
        return content

    @api.model
    def set_prefix(self, pos_reference):
        '''Add prefix into pos.order'''
        order = self.env['pos.order'].search([('pos_reference', '=', pos_reference)], limit=1)
        pos_config = self.env['pos.config'].search([], limit=1)  # TODO IMP multiple stores
        order.pos_reference = pos_config.fp_order_suffix + pos_reference

    @api.model
    def get_prefix(self):
        '''Return the prefix for pos.order'''
        return self.env['pos.config'].search([], limit=1).fp_order_suffix  # TODO IMP multiple stores
