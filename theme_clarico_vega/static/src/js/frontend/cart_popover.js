/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";
import { _lt, _t } from "@web/core/l10n/translation";
var registry = publicWidget.registry;

publicWidget.registry.websiteSaleCartLinkEpt = publicWidget.Widget.extend({
    selector: '.o_wsale_my_cart a',
    events: {
        'click': '_cartPopupData',
    },
    _cartPopupData: async function(ev) {
        ev.preventDefault();
        let self = this;
        self = await $.get('/shop/cart_popover').then(function (data) {
            $("#cartoffcanvasWithBackdrop .offcanvas-body").html(data);
            $(".te_clear_cart_popover").on('click', function(ev) {
                jsonrpc('/shop/clear_cart', {}).then((data) => {
                    location.reload();
                    $(".my_cart_quantity").html('0');
                });
            });
        });
    },
});

$(document).mouseup(function (ev) {
    if ($(ev.target).closest(".mycart-popover").length === 0) {
         $(".mycart-popover").removeClass("te_open");
        $("#wrapwrap").removeClass("te_overlay");
        $('.mycart-popover').removeClass('show');
        $('.mycart-popover').remove();
        $('header#top').css({'z-index': ''});
    }
});

$(document).on('click', '.te_cross', function() {
    $(".mycart-popover").removeClass("te_open");
    $("#wrapwrap").removeClass("te_overlay");
    $('.mycart-popover').removeClass('show');
    $('.mycart-popover').remove();
    $('header#top').css({'z-index': ''});
    if ($(window).width() <= 768) {
        $('.mycart-popover').remove();
    }
});
/*==== clear cart ========*/
registry.clear_cart = publicWidget.Widget.extend({
    selector: '#wrapwrap , .mycart-popover',
    read_events: {
        'click .te_clear_cart': '_onClickClearCart',
    },
    _onClickClearCart: function (ev) {
        ev.preventDefault();
        jsonrpc('/shop/clear_cart', {}).then(function(data){
            location.reload();
        });
    },
});

publicWidget.registry.product_pager = publicWidget.Widget.extend({
    selector: ".next_prev_btn_main",
    events: {
        'mouseenter .product_next_btn, .product_prev_btn': 'getProductInfo',
        'mouseleave .product_next_btn, .product_prev_btn': 'removeProductInfo',
    },
    getProductInfo: function(ev) {
        const windowWidth = $(window).width();
        if (windowWidth > 992) {
            var product_id = $(ev.currentTarget).attr('product-id') || false;
            var params = {'product_id': product_id};
            jsonrpc('/get_product_info', params).then(function (data) {
                $(ev.currentTarget).find('.main_product_container_append').html(data);
            });
        }
    },
    removeProductInfo: function(ev) {
        const windowWidth = $(window).width();
        if (windowWidth > 992) {
            $(ev.currentTarget).find('.main_product_container_append').html('');
        }
    },
});
