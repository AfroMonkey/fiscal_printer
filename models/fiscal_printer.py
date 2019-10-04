from odoo import api, models


def to_chunks(s: str, w: int):
    return [s[y-w:y] for y in range(w, len(s)+w, w)]

class FiscalPrinter(models.Model):
    _name = 'fiscal.printer'

    @api.model
    def print_file(self, rows, payment_lines):
        ProductProduct = self.env['product.product']
        pos_config = self.env['pos.config'].search([], limit=1) # TODO IMP multiple stores
        for r in rows:
            r['name'] = ProductProduct.browse(r['id']).product_name_pos
        
        # OPEN FISCAL RECEIPT
        content = '1020;1\n'
        # ROW PRODUCT SALE
        discount_amount = 0
        surcharge = 0
        subtotal_discount = ''
        for r in rows:
            product = ProductProduct.browse(r['id'])
            if product == pos_config.discount_product_id:
                discount = abs(r['price'])
                subtotal_discount = '1025;2;1;Discount {discount};{discount}\n'.format(discount=discount)
                continue
            # TODO IMP check , instead of .
            vat_id = product.taxes_id[0] # TODO IMP multiple taxes
            vat_code = pos_config.fp_tax_ids.search([('tax_id', '=', vat_id.id)]).code
            content += '1021;1;;{vat};;;{name};{price};{qty}\n'.format(vat=vat_code, name=r['name'], price=r['price'], qty=r['qty'])
            # ADDITIONAL PRODUCT TEXT
            additional_text = ''
            for field in pos_config.fp_product_additional_text_ids:
                additional_text += product[field.name].name
            for chunk in to_chunks(additional_text, 24):
                content += '112;{};0;1;3\n'.format(chunk)
            # PRODUCT DISCOUNT
            if r.get('discount'):
                discount_amount = r['price'] * r['qty'] * r['discount'] / 100
                content += '1025;2;1;Discount {discount}%;{discount_amount}\n'.format(discount=r['discount'], discount_amount=discount_amount)
            # PRODUCT SURCHARGE
            surcharge = 0 # TODO IMP
            if surcharge:
                surcharge_text = '' # TODO IMP
                content += '1025;4;1;{surcharge_text};{surcharge}\n'.format(surcharge_text=surcharge_text, surcharge=surcharge)
        # SUBTOTAL
        if subtotal_discount:
            content += '1028\n'
        # SUBTOTAL DISCOUNT
        if subtotal_discount:
            content += subtotal_discount
        # TODO IMP SUBTOTAL SURCHARGE
        # PAYMENT METHOD
        # TODO IMP multiple methods
        payment_code = pos_config.fp_journal_ids.search([('journal_id', '=', payment_lines[0]['journal_id'])]).code
        cash = payment_lines[0]['amount']
        content += '1030;{payment_code};1;;{cash}\n'.format(payment_code=payment_code, cash=cash or '')
        # ADDITIONAL TEXT
        additional_text = pos_config.fp_additional_text
        for chunk in to_chunks(additional_text, 24):
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
        with open(file_path, 'w') as file_output:
            file_output.write(content)
    
    @api.model
    def set_prefix(self, pos_reference):
        order = self.env['pos.order'].search([('pos_reference', '=', pos_reference)], limit=1)
        pos_config = self.env['pos.config'].search([], limit=1) # TODO IMP multiple stores
        order.pos_reference = pos_config.fp_order_suffix + order.pos_reference
    
    @api.model
    def get_prefix(self):
        return self.env['pos.config'].search([], limit=1).fp_order_suffix # TODO IMP multiple stores
