odoo.define("website_request_quote_order.sale", function (require) {
    var ajax = require("web.ajax");

    $(document).ready(function () {
        $("#product_call_for_price_modal").on("shown.bs.modal", function () {
            $('input[name="input_firstname"]').focus();
        });

        $("#frm_register").submit(function (e) {
            e.preventDefault();

            var ret = ajax
                .jsonRpc("/sale/product_call_for_price", "call", {
                    product_id: $(".product_id").val(),
                    first_name: $('input[name="input_firstname"]').val(),
                    last_name: $('input[name="input_lastname"]').val(),
                    email: $('input[name="input_email"]').val(),
                    contact_no: $('input[name="input_contactno"]').val(),
                    quantity: $('input[name="input_quantity"]').val(),
                    message: $('textarea[name="input_message"]').val(),
                })
                .then(function (data) {
                    if (data == 1) {
                        $("#product_call_for_price_modal .closemodel_btn").click();
                        $("#bttn_reset").click();
                        $("#alertmsg").html('<div class="alert alert-success"><strong>Thank you for information, we will get back to you asap.</strong></div>');
                    } else {
                        $("#product_call_for_price_modal .closemodel_btn").click();
                        $("#alertmsg").html('<div class="alert alert-danger"><strong>Failure in product call for price.</strong></div>');
                    }
                });
            return false;
        });
    });
});
