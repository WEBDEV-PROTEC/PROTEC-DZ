import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

class StockNotificationCron(models.AbstractModel):
    _name = 'stock.notification.cron'
    _description = 'Stock Notification Cron'

    @api.model
    def _send_stock_notifications(self):
        _logger.info("Starting stock notification cron job.")

        location = self.env['stock.location'].search([('name', '=', 'MAG/Stock')], limit=1)
        products_to_notify = []

        # Set the batch size for processing
        batch_size = 100
        offset = 0

        # Continue processing batches until all products are covered
        while True:
            # Fetch products in batches using LIMIT and OFFSET
            products_below_threshold = self.env['product.template'].search([
                ('qty_available', '<=', 2),
                ('location_id', '=', location.id),
                ('qty_available', '>', 0),  # Only add products with quantity greater than zero
            ], limit=batch_size, offset=offset)

            # Break the loop if no more products are found
            if not products_below_threshold:
                break

            # Process the current batch of products
            self._process_batch(products_below_threshold, products_to_notify)

            # Increment the offset for the next batch
            offset += batch_size

        _logger.info(f"Processing all products: {products_to_notify}")

        try:
            self._notify_users(products_to_notify)
            _logger.info('Notifications sent')
        except Exception as e:
            _logger.error(f"Error sending notifications: {e}")

    @api.model
    def _process_batch(self, products_below_threshold, products_to_notify):
        # Process the current batch of products
        for product in products_below_threshold:
            products_to_notify.append({
                'name': product.name,
                'qty_available': product.qty_available,
                'status': 'red' if product.qty_available < 2 else 'orange',
            })
    @api.model
    def _notify_users(self, products_to_notify):
        _logger.info("Notifying users in Odoo about products that need restocking.")

        # Search for the existing channel named "stock_warning"
        channel = self.env['mail.channel'].search([('name', '=', 'Stock Notif'), ('public', '=', 'private')], limit=1)

        # If the channel doesn't exist, create it and add all users
        if not channel:
            channel = self.env['mail.channel'].create({
                'name': 'Stock Notif',
                'public': 'public',
            })

            # Add all users to the "stock_warning" channel
            all_users = self.env['res.users'].search([])
            channel.write({'channel_partner_ids': [(4, user.partner_id.id) for user in all_users]})

        # Notify users in the "stock_warning" channel
        for product_info in products_to_notify:
            if product_info['qty_available'] <= 2:
                message = (
                    f"<span style='color: orange;'>RESTOCK NECESSAIRE POUR</span> "
                    f"<span style='color: green; text-decoration: none; font-weight: bold;'>{product_info['name']}</span> "
                    f"<span style='color: red;'>QUANTITE RESTANTE: {product_info['qty_available']}</span>"
                )
                # Create a mail.message to associate with the channel
                channel.message_post(body=message, message_type='comment', subtype_xmlid='mail.mt_comment', author_id=self.env.user.partner_id.id)
                
       
        
        _logger.info("Users in the Stock Notif channel notified about products that need restocking.")
        
    @api.model
    def _get_channel_icon(self):
        # Get the path to the assets folder
        assets_folder = os.path.join(os.path.dirname(__file__), '..', 'assets')

        # Load your custom icon image and encode it in base64
        icon_path = os.path.join(assets_folder, 'icon.png')

        with open(icon_path, 'rb') as image_file:
            icon_binary = image_file.read()

        return base64.b64encode(icon_binary)