
from odoo import api, models
import logging
_logger = logging.getLogger(__name__)

class CodAccountMove(models.Model):
    _inherit = "account.move"

    def action_invoice_paid(self):
        if self and self.payment_state == "paid":
            try:
                payment_transections = self.env["payment.transaction"].search([("state",'=','pending'),("provider", "=", "cash_on_delivery")])
                cod_transection = payment_transections and payment_transections.filtered(lambda txn: self.id in txn.invoice_ids.ids)
                txn = cod_transection and cod_transection[0]
                if txn:
                    txn.state = "done"
            except Exception as e:
                _logger.info("\n\n\n[COD]: EXCEPTION in auto done payment transection....%r\n\n\n",str(e))