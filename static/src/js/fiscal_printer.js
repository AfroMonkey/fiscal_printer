odoo.define('POS.pos', function (require) {
    'use strict';

    var screens = require('point_of_sale.screens');
    var Widget = require('web.Widget');
    var rpc = require('web.rpc');
    var session = require('web.session');


    screens.PaymentScreenWidget.include({
        renderElement: function () {
            var self = this;
            this._super();
            this.$('.js_fiscal_print').click(function () {
                self.fiscal_print();
            });
        },
        fiscal_print: function () {
            var order = this.pos.get_order();
            // TODO send POS id
            var rows = [];
            for (const line of order.get_orderlines()) {
                rows.push({
                    id: line.product.id,
                    qty: line.quantity,
                    price: line.price,
                    discount: line.discount,
                    // vat_button:, TODO
                })
            }
            var payment_lines = []
            for (const line of order.paymentlines.models) {
                payment_lines.push({
                    journal_id: line.cashregister.journal.id,
                    amount: line.amount,
                })
            }
            return rpc.query({
                model: 'fiscal.printer',
                method: 'print_file',
                args: [rows, payment_lines],
                kwargs: {
                    context: session.user_context
                },
            });
        }
    });
});
