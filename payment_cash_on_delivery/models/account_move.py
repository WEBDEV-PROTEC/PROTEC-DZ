
from odoo import api, models
import logging
_logger = logging.getLogger(__name__)

class CodAccountMove(models.Model):
    _inherit = "account.move"

    def action_invoice_paid(self):
        # Loop through each invoice in self to handle multiple invoices safely
        for record in self:
            if record.payment_state == "paid":
                try:
                    # Search for pending transactions for cash on delivery
                    payment_transactions = self.env["payment.transaction"].search([
                        ("state", "=", "pending"),
                        ("provider", "=", "cash_on_delivery"),
                        ("invoice_ids", "in", record.id)  # Ensure the transaction is related to the current invoice
                    ])
                    if payment_transactions:
                        # Assuming only one transaction per invoice, but if multiple, consider handling or logging
                        for txn in payment_transactions:
                            txn.state = "done"
                except Exception as e:
                    _logger.info("\n\n\n[COD]: EXCEPTION in auto done payment transaction....%r\n\n\n", str(e))
