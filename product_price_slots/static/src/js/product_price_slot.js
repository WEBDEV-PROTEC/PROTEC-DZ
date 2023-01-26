/* Copyright (c) 2019-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : https://store.webkul.com/license.html/ */

odoo.define('product_price_slots.product_price_slot', function (require) {
    "use strict";

    var ajax = require('web.ajax');

    $(document).ready(function () {
        localStorage.removeItem("product_id");
        $("#product_details .js_product").on('change',"input.product_id",function(){
            var product_id = parseInt($(this).val(),10);
            load_product_offers(product_id);
        });
    });
    
    $(document).on('click', '.wk_add_to_cart_slot', function (ev) {
        ev.preventDefault();
        $(".wk_product_offer_slot").find(".wk_price_slot_qty").attr('name', 'add_qty')
        $(this).closest('form').submit();
    });

    function load_product_offers(product_id) {
        var p_id = parseInt(localStorage.getItem('product_id'));
        if (product_id != p_id || p_id==NaN){
            localStorage.setItem('product_id', product_id);
            $('.wk_product_slot_loading').removeClass("d-none");
            $('.wk_product_offer_slot').hide();
            ajax.jsonRpc("/product/price/slot/"+product_id, 'call', {}).then(function (data){
                $('.wk_product_slot_loading').addClass("d-none");
                $('.wk_product_offer_slot').html(data);
                $('.wk_product_offer_slot').find(".no-offer").removeClass("d-none");
                $('.wk_product_offer_slot').show();
            });
        }
    }

});