from odoo import api, fields, models, _
from datetime import datetime, timedelta

class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def _default_select_warehouse_id(self):
        return self.env["stock.warehouse"].search([])

    multi_warehouse_ids = fields.Many2many(
        comodel_name="stock.warehouse",
        string="Multi Warehouse",
        default=_default_select_warehouse_id,
        check_company=True,
    )

    def get_warehouse_ids(self):
        existing_w_l = []
        for line in self.order_line:
            total_qty = line.product_uom_qty
            if (len(self.multi_warehouse_ids) >= 1 and total_qty != 0 and line.splitted == False):
                for wr_id in self.multi_warehouse_ids:
                    if total_qty == 0:
                        continue
                    warehouse_available_qty = wr_id.lot_stock_id.quant_ids.filtered(lambda x: x.product_id == line.product_id).available_quantity
                    if warehouse_available_qty == 0:
                        continue
                    if (total_qty > warehouse_available_qty):
                        if wr_id.id not in existing_w_l:
                            existing_w_l.append(wr_id.id)
                        #creating New Line with available qty
                        vals = {
                            "product_id": line.product_id.id,
                            "name": line.name,
                            "product_uom_qty": warehouse_available_qty,
                            "price_unit": line.price_unit,
                            "warehouse_id": wr_id.id,
                            "splitted": True,
                        }
                        self.write({"order_line": [(0, 0, vals)]})
                        #Now calculating remaning qty for existing line update
                        total_qty -= warehouse_available_qty
                        vals = {
                            "product_uom_qty": total_qty,
                            "warehouse_id": wr_id.id,
                            "splitted": False,
                        }
                        #Updating Existing line with ref of existing warehouse
                        line.write(vals)
                    elif(total_qty == warehouse_available_qty):
                        if wr_id.id not in existing_w_l:
                            existing_w_l.append(wr_id.id)
                        vals = {
                            "product_uom_qty": warehouse_available_qty,
                            "warehouse_id": wr_id.id,
                            "splitted": True,
                        }
                        #making same line with warehouse update without spliting
                        line.write(vals)
                        total_qty = 0
                    else:
                        if wr_id.id not in existing_w_l:
                            existing_w_l.append(wr_id.id)
                        vals = {
                            "product_uom_qty": total_qty,
                            "warehouse_id": wr_id.id,
                            "splitted": True,
                        }
                        #warehouse_available_qty is greater then total_qty then need to pass wareshouse ref
                        line.write(vals)
                        total_qty = 0
        if existing_w_l:
            existing_w_l = list(set(self.multi_warehouse_ids.ids) & set(existing_w_l))
            to_del_w_ids = self.multi_warehouse_ids.filtered(lambda x: x.id not in existing_w_l)
            if to_del_w_ids:
                for l in to_del_w_ids.ids:
                    self.write({'multi_warehouse_ids': [(3, l)]})


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    warehouse_id = fields.Many2one("stock.warehouse", related=False)
    splitted = fields.Boolean()

    def _prepare_procurement_values(self, group_id=False):
        """Prepare specific key for moves or other components that will be created from a stock rule
        comming from a sale order line. This method could be override in order to add other custom key that could
        be used in move/po creation.
        """
        values = super(SaleOrderLine, self)._prepare_procurement_values(group_id)
        self.ensure_one()
        # Use the delivery date if there is else use date_order and lead time
        date_deadline = self.order_id.commitment_date or (
            self.order_id.date_order + timedelta(days=self.customer_lead or 0.0)
        )
        date_planned = date_deadline - timedelta(
            days=self.order_id.company_id.security_lead
        )
        values.update(
            {
                "group_id": group_id,
                "sale_line_id": self.id,
                "date_planned": date_planned,
                "date_deadline": date_deadline,
                "route_ids": self.route_id,
                "warehouse_id": self.warehouse_id or False,
                "partner_id": self.order_id.partner_shipping_id.id,
                "product_description_variants": self._get_sale_order_line_multiline_description_variants(),
                "company_id": self.order_id.company_id,
            }
        )
        return values
