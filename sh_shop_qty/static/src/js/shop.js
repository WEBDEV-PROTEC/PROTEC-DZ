/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import wSaleUtils from "@website_sale/js/website_sale_utils";
// import { OptionalProductsModal } from "@website_sale_product_configurator/js/sale_product_configurator_modal";
import "@website_sale/js/website_sale";
import { _t } from "@web/core/l10n/translation";
// import { WebsiteSale } from "@website_sale/js/website_sale";



    publicWidget.registry.WebsiteSale.include({

        _onClickAddCartJSON: function(ev) {        
            ev.preventDefault();
            var $link = $(ev.currentTarget);

            var $input = $link.closest(".input-group").find("input");

            // var module_name = $input.attr('data-module_name') || false;
            // if (module_name != 'sh_shop_qty'){
            //     this._super.apply(this, arguments);
            //     return false;
            // }

            var min = parseFloat($input.data("min") || 0);
            var setqty = parseFloat($input.data("setqty") || 1);
            var max = parseFloat($input.data("max") || Infinity);
            var quantity = ($link.has(".fa-minus").length ? -setqty : setqty) + parseFloat($input.val() || 0, 10);
            var newQty = quantity > min ? (quantity < max ? quantity : max) : min;
  
            $input.val(newQty).trigger("change");
            return false;
        },
        _onChangeAddQuantity: function(ev) {
            /// this._super.apply(this, arguments);

            ev.preventDefault();
            var $input = $(ev.currentTarget);
            var module_name = $input.attr('data-module_name') || false;
            // if (module_name != 'sh_shop_qty'){
            //     this._super.apply(this, arguments);
            //     return false;
            // }

            var data = $input.val();
            var default_value = $input.data("setqty");
        
            data = parseInt(data) || 0;
            default_value = parseInt(default_value) || 0;
        
            if (data < default_value) {
                var set_data = default_value;
                $input.val(set_data);
            } else {
                var divided_value = Math.ceil(data / default_value);
                var set_data = divided_value * default_value;
                $input.val(set_data);
            }
        
            this._super.apply(this, arguments);
            return false;
        },
        
        /**
         * @private override
         */
        _changeCartQuantity: function($input, value, $dom_optional, line_id, productIDs) {
            this._super.apply(this, arguments);
            if (value != 0) {
                var data = parseInt(value) || 0;
                var default_value = parseInt($input.data("setqty")) || 0;
            
                if (data < default_value) {
                    var set_data = default_value;
                    $input.val(set_data);
                } else {
                    var divided_value = Math.ceil(data / default_value);
                    var set_data = divided_value * default_value;
                    $input.val(set_data);
                }
            }
        }
        
    });
