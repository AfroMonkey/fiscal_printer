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
                if (self.order_is_valid('confirm')) {
                    var order = self.pos.get_order()
                    self.fiscal_print(order);
                    self.get_prefix().then(function (prefix) {
                        order.name = prefix + order.get_name();
                        self.validate_order();
                        order.finalize();
                    });
                }
            });
        },
        fiscal_print: function (order) {
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
                    method_id: line.payment_method.id,
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
        get_prefix: function () {
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
            var order = self.pos.get_order();
            this._super();
            this.$('.js_fiscal_print2').click(function () {
                self.fiscal_print(order);
                self.set_prefix(order.name).then(function (prefix) {
                    order.finalize();
                });
            });
        },
        fiscal_print: function (order) {
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
                    method_id: line.payment_method.id,
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
