/*jshint esversion: 6 */
odoo.define("POS.pos", function(require) {
  "use strict";

  var screens = require("point_of_sale.screens");
  var Widget = require("web.Widget");
  var rpc = require("web.rpc");
  var session = require("web.session");

  screens.PaymentScreenWidget.include({
    renderElement: function() {
      var self = this;
      this._super();
      this.$(".js_fiscal_print").click(function() {
        if (self.order_is_valid("confirm")) {
          var order = self.pos.get_order();
          self.fiscal_print(order);
          self.finalize_validation_return_promise().then(function() {
            self.set_prefix(order.name);
            order.finalize();
          });
        }
      });
    },
    finalize_validation_return_promise: function() {
      var self = this;
      var order = this.pos.get_order();

      if (order.is_paid_with_cash() && this.pos.config.iface_cashdrawer) {
        this.pos.proxy.printer.open_cashbox();
      }

      order.initialize_validation_date();
      order.finalized = true;
      if (order.is_to_invoice()) {
        var invoiced = this.pos.push_and_invoice_order(order);
        this.invoicing = true;

        invoiced.catch(
          this._handleFailedPushForInvoice.bind(this, order, false)
        );

        invoiced.then(function(server_ids) {
          self.invoicing = false;
          var post_push_promise = [];
          post_push_promise = self.post_push_order_resolve(order, server_ids);
          post_push_promise
            .then(function() {
              self.gui.show_screen("receipt");
            })
            .catch(function(error) {
              self.gui.show_screen("receipt");
              if (error) {
                self.gui.show_popup("error", {
                  title: "Error: no internet connection",
                  body: error
                });
              }
            });
        });
        return invoiced;
      } else {
        var ordered = this.pos.push_order(order);
        if (order.wait_for_push_order()) {
          var server_ids = [];
          ordered
            .then(function(ids) {
              server_ids = ids;
            })
            .finally(function() {
              var post_push_promise = [];
              post_push_promise = self.post_push_order_resolve(
                order,
                server_ids
              );
              post_push_promise
                .then(function() {
                  self.gui.show_screen("receipt");
                })
                .catch(function(error) {
                  self.gui.show_screen("receipt");
                  if (error) {
                    self.gui.show_popup("error", {
                      title: "Error: no internet connection",
                      body: error
                    });
                  }
                });
            });
        } else {
          self.gui.show_screen("receipt");
        }
        return ordered;
      }
    },
    fiscal_print: function(order) {
      var rows = [];
      for (const line of order.get_orderlines()) {
        rows.push({
          id: line.product.id,
          qty: line.quantity,
          price: line.price,
          discount: line.discount
        });
      }
      var payment_lines = [];
      for (const line of order.paymentlines.models) {
        payment_lines.push({
          method_id: line.payment_method.id,
          amount: line.amount
        });
      }
      rpc.query({
        model: "fiscal.printer",
        method: "print_file",
        args: [rows, payment_lines],
        kwargs: {
          context: session.user_context
        }
      });
    },
    set_prefix: function(pos_reference) {
      return rpc.query({
        model: "fiscal.printer",
        method: "set_prefix",
        args: [pos_reference],
        kwargs: {
          context: session.user_context
        }
      });
    },
    order_changes: function() {
      var self = this;
      var order = this.pos.get_order();
      if (!order) {
        return;
      } else if (order.is_paid()) {
        self.$(".next").addClass("highlight");
        self.$(".js_fiscal_print").addClass("highlight");
      } else {
        self.$(".next").removeClass("highlight");
        self.$(".js_fiscal_print").removeClass("highlight");
      }
    }
  });

  screens.ReceiptScreenWidget.include({
    renderElement: function() {
      var self = this;
      this._super();
      this.$(".js_fiscal_print_published").click(function() {
        var order = self.pos.get_order();
        self.fiscal_print(order);
        self.set_prefix(order.name);
        order.finalize();
      });
    },
    fiscal_print: function(order) {
      var rows = [];
      for (const line of order.get_orderlines()) {
        rows.push({
          id: line.product.id,
          qty: line.quantity,
          price: line.price,
          discount: line.discount
        });
      }
      var payment_lines = [];
      for (const line of order.paymentlines.models) {
        payment_lines.push({
          method_id: line.payment_method.id,
          amount: line.amount
        });
      }
      return rpc.query({
        model: "fiscal.printer",
        method: "print_file",
        args: [rows, payment_lines],
        kwargs: {
          context: session.user_context
        }
      });
    },
    set_prefix: function(pos_reference) {
      return rpc.query({
        model: "fiscal.printer",
        method: "set_prefix",
        args: [pos_reference],
        kwargs: {
          context: session.user_context
        }
      });
    }
  });
});
