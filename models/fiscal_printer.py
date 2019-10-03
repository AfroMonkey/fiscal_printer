from odoo import api, models


class FiscalPrinter(models.Model):
    _name = 'fiscal.printer'

    @api.model
    def print_file(self, rows, payment_lines):
        ProductProduct = self.env['product.product']
        for r in rows:
            r['name'] = ProductProduct.browse(r['id']).product_name_pos
        
        # OPEN FISCAL RECEIPT
        content = '1020;1\n'
        # ROW PRODUCT SALE
        discount_amount = 0
        surcharge = 0
        for r in rows:
            # TODO VAT
            # TODO check , instead of .
            content += '1021;1;;{vat};;;{name};{price};{qty}\n'.format(vat='1', name=r['name'], price=r['price'], qty=r['qty'])
            # ADDITIONAL PRODUCT TEXT
            additional_text = '' # TODO
            if additional_text: # TODO check len
                content += '112;{};0;1;3\n'.format(additional_text)
            # PRODUCT DISCOUNT
            if r.get('discount'):
                discount_amount = r['price'] * r['qty'] * r['discount'] / 100
                content += '1025;2;1;Discount {discount}%;{discount_amount}\n'.format(discount=r['discount'], discount_amount=discount_amount)
            # PRODUCT SURCHARGE
            surcharge = 0 # TODO
            if surcharge:
                surcharge_text = '' # TODO
                content += '1025;4;1;{surcharge_text};{surcharge}\n'.format(surcharge_text=surcharge_text, surcharge=surcharge)
        # SUBTOTAL
        if discount_amount or surcharge:
            content += '1028\n'
        # SUBTOTAL DISCOUNT TODO
        # SUBTOTAL SURCHARGE TODO
        # PAYMENT METHOD
        payments_codes = {
            'Cash (USD)': 1,
            # TODO credit card
        }
        payment_code = payments_codes.get(payment_lines[0]['name'], 1)
        cash = payment_lines[0].get('amount', 0)
        content += '1030;{payment_code};1;;{cash}\n'.format(payment_code=payment_code, cash=cash or '')
        # ADDITIONAL TEXT
        additional_text = ''  # TODO
        if additional_text:  # TODO check len
            content += '112;{};0;1;3\n'.format(additional_text)
        # CUTTER RECEIPT PAPER
        cutter_receipt_paper = False # TODO
        if cutter_receipt_paper:
            content += '115\n'
        # OPEN CASH DRAWER
        open_cash_drawer = False # TODO
        if open_cash_drawer:
            content += '1029;1\n'
