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
                // console.log(document.querySelectorAll('.next.highlight'));
                if (self.order_is_valid('confirm')) {
                    var order = self.fiscal_print();
                    self.get_prefix().then(function (prefix) {
                        order.name = prefix + order.get_name();
                        self.validate_order();
                        order.finalize();
                    });
                }
            });
        },
        fiscal_print: function () {
            var order = this.pos.get_order();
            var rows = [];
            for (const line of order.get_orderlines()) {
                rows.push({
                    id: line.product.id,
                    qty: line.quantity,
                    price: line.price,
                    discount: line.discount,
                })
            }
            var payment_lines = []
            for (const line of order.paymentlines.models) {
                payment_lines.push({
                    journal_id: line.cashregister.journal.id,
                    amount: line.amount,
                })
            }
            rpc.query({
                model: 'fiscal.printer',
                method: 'print_file',
                args: [rows, payment_lines],
                kwargs: {
                    context: session.user_context
                },
            });
            return order;
        },
        get_prefix: function() {
            return rpc.query({
                model: 'fiscal.printer',
                method: 'get_prefix',
                args: [],
                kwargs: {
                    context: session.user_context
                },
            });
        }
    });

    screens.ReceiptScreenWidget.include({
        renderElement: function () {
            var self = this;
            this._super();
            this.$('.js_fiscal_print2').click(function () {
                // console.log(document.querySelectorAll('.next.highlight'));
                var order = self.fiscal_print();
                self.set_prefix(order.name).then(function (prefix) {
                    order.finalize();
                });
            });
        },
        fiscal_print: function () {
            var order = this.pos.get_order();
            var rows = [];
            for (const line of order.get_orderlines()) {
                rows.push({
                    id: line.product.id,
                    qty: line.quantity,
                    price: line.price,
                    discount: line.discount,
                })
            }
            var payment_lines = []
            for (const line of order.paymentlines.models) {
                payment_lines.push({
                    journal_id: line.cashregister.journal.id,
                    amount: line.amount,
                })
            }
            rpc.query({
                model: 'fiscal.printer',
                method: 'print_file',
                args: [rows, payment_lines],
                kwargs: {
                    context: session.user_context
                },
            });
            return order;
        },
        set_prefix: function (pos_reference) {
            return rpc.query({
                model: 'fiscal.printer',
                method: 'set_prefix',
                args: [pos_reference],
                kwargs: {
                    context: session.user_context
                },
            });
        }
    });
});
