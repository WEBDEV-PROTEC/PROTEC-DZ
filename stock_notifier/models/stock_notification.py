import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)

class StockNotificationCron(models.AbstractModel):
    _name = 'stock.notification.cron'
    _description = 'Stock Notification Cron'

    @api.model
    def _send_stock_notifications(self):
        _logger.info("Starting stock notification cron job.")

        locations = {
            'MAGASIN': {
                'channel_name': 'Alerte Stock MAG/MAGASIN',
                'user_name': 'Stock Manager'
            },
            'DEPOT': {
                'channel_name': 'Alerte Stock DEP/DEPOT',
                'user_name': 'DEPOT (PROTEC)'
            },
        }

        # Testing purposes: Limit the total number of products to 10
        test_limit = 10

        # Process products for each location
        for location_name, data in locations.items():
            location = self.env['stock.location'].search([('complete_name', 'like', location_name)], limit=1)
            user = self.env['res.users'].search([('name', '=', data['user_name'])], limit=1)

            if not location:
                _logger.warning(f"Location '{location_name}' not found.")
                continue

            if not user:
                _logger.warning(f"User '{data['user_name']}' not found.")
                continue

            products_to_notify = []

            # Fetch products using stock.quant based on location and quantity below threshold
            quants_below_threshold = self.env['stock.quant'].search([
                ('location_id', '=', location.id),
                ('quantity', '<=', 2),
                ('quantity', '>', 0)  # Only products with a quantity greater than zero
            ], limit=test_limit)

            # Process the products fetched for this location
            self._process_batch(quants_below_threshold, products_to_notify)

            _logger.info(f"Processing products for {location_name}: {products_to_notify}")

            if products_to_notify:
                try:
                    self._notify_user(products_to_notify, data['channel_name'], user)
                    _logger.info(f'Notifications sent for {location_name}')
                except Exception as e:
                    _logger.error(f"Error sending notifications for {location_name}: {e}")

    @api.model
    def _process_batch(self, quants_below_threshold, products_to_notify):
        for quant in quants_below_threshold:
            products_to_notify.append({
                'name': quant.product_id.name,
                'qty_available': quant.quantity,
                'status': 'red' if quant.quantity < 2 else 'orange',
            })

    @api.model
    def _notify_user(self, products_to_notify, channel_name, user):
        _logger.info(f"Notifying {user.name} about products that need restocking via channel '{channel_name}'.")

        # Create or find the channel
        channel = self.env['mail.channel'].search([('name', '=', channel_name), ('public', '=', 'private')], limit=1)

        if not channel:
            channel = self.env['mail.channel'].create({
                'name': channel_name,
                'public': 'public',
            })

            # Add the user to the channel
            all_users = self.env['res.users'].search([])
            channel.write({'channel_partner_ids': [(4, user.partner_id.id) for user in all_users]})

        # Notify users in the channel
        for product_info in products_to_notify:
            if product_info['qty_available'] <= 2:
                message = (
                    f"<div style='border: 1px solid #ccc; padding: 10px; background-color: #f9f9f9; border-radius: 8px;'>"
                    f"<h3 style='color: #d9534f; margin-bottom: 10px;'>⚠️ Restock Alert</h3>"
                    f"<p style='font-size: 14px; color: #333;'>"
                    f"<span style='color: #ff9800; font-weight: bold;'>Produit:</span> "
                    f"<span style='color: #4caf50; text-decoration: none; font-weight: bold;'>{product_info['name']}</span><br>"
                    f"<span style='color: #ff9800; font-weight: bold;'>Quantité Restante:</span> "
                    f"<span style='color: #d9534f;'>{product_info['qty_available']}</span>"
                    f"</p>"
                    f"<p style='font-size: 12px; color: #888; margin-top: 10px;'>Veuillez réapprovisionner dès que possible.</p>"
                    f"</div>"
                )
                # Create a mail.message to associate with the channel
                channel.message_post(body=message, message_type='comment', subtype_xmlid='mail.mt_comment', author_id=self.env.user.partner_id.id)

        _logger.info(f"Users in the channel '{channel_name}' notified about products that need restocking.")

