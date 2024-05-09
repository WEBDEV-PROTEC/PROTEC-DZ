import logging
from odoo import http
from odoo.http import request
import requests

_logger = logging.getLogger(__name__)

class YalidineAPIController(http.Controller):

    @http.route('/shop/payment', type='http', auth='public', website=True)
    def index(self, **kwargs):
        _logger.info("Yalidine API : Starting payment process")

        # Retrieve the order ID from the session
        order_id = request.session.get('sale_order_id')
        if not order_id:
            _logger.warning("Order ID not found in session")
            return "Order ID not found in session"

        _logger.info("Retrieving order with ID: %s", order_id)
        # Retrieve the order
        order = request.env['sale.order'].sudo().browse(order_id)

        # Retrieve customer information from the order
        customer_name = order.partner_id.name or ''
        customer_phone = order.partner_id.phone or ''
        customer_address = order.partner_id.street or ''
        customer_city = order.partner_id.city or ''

        _logger.info("Calculating values and fetching product names from cart")
        # Calculate total amount, total weight, and product names
        items_value, total_weight, product_names, shipping_cost, total_amount = self.calculate_total_amount_weight_and_shipping_cost(order_id, customer_city)

        # Split name into first name and family name
        name_parts = customer_name.split(maxsplit=1)
        first_name = name_parts[0] if name_parts else ''
        family_name = name_parts[1] if len(name_parts) > 1 else ''

        _logger.info("Retrieved stored address information from order: %s", order)

        # Perform API call to YALIDINE API to create the parcel with the retrieved address information
        url = "https://api.yalidine.app/v1/parcels/"
        api_id = '30766545130987580386'
        api_token = 'ImVbOQcUYtikAM6i8e3qM754wJ5lSuBzTFzaldoFOAvhHWcPf2DYugk1S6xDXXsP'
        headers = {
            "Content-Type": "application/json",
            "X-API-ID": api_id,
            "X-API-TOKEN": api_token
        }

        payload = {
            "order_id": order_id,
            "from_wilaya_name": "Oran",  # Replace with appropriate value
            "firstname": first_name,
            "familyname": family_name,
            "contact_phone": customer_phone,
            "address": customer_address,
            "to_commune_name": "",  # Fill this with appropriate data
            "to_wilaya_name": customer_city,
            "product_list": product_names,
            "price": total_amount,
            "do_insurance": False,
            "declared_value": items_value,
            "height": 0,
            "width": 0,
            "length": 0,
            "weight": total_weight,
            "freeshipping": False,
            "is_stopdesk": True,
            "has_exchange": 0,
            "product_to_collect": str(total_amount) + "dzd"
        }
        _logger.info("Created yalidine payload: %s", payload)
        try:
            _logger.info("Making API call to create parcel")
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            _logger.info("Parcel created successfully: %s", response.json())
            return "Parcel created successfully"
        except requests.RequestException as e:
            _logger.error("Error creating parcel: %s", e)
            return "Error creating parcel: %s" % e

    def calculate_total_amount_weight_and_shipping_cost(self, order_id, city):
        _logger.info("Calculating total amount, weight, and shipping cost")
        order = request.env['sale.order'].sudo().browse(order_id)
        items_value = sum(order.order_line.mapped('price_total'))
        total_weight = sum(order.order_line.mapped('product_id.weight'))
        product_names = [line.product_id.name for line in order.order_line]

        _logger.info("Items value: %s, Total weight: %s, Product names: %s", items_value, total_weight, product_names)
        # Here you can calculate shipping cost and total amount based on your business logic
        shipping_cost = self.calculate_shipping_cost(city)  # Replace with actual shipping cost calculation
        total_amount = shipping_cost + items_value

        return items_value, total_weight, product_names, shipping_cost, total_amount

    def calculate_shipping_cost(self, city):
        _logger.info("Calculating shipping cost for city: %s", city)
        city_id = self.get_city_id(city)
        if city_id == 0:
            _logger.warning("City ID not found for city: %s", city)
            return 0  # City not found, shipping cost is 0

        _logger.info("Fetching shipping cost from Yalidine API for city ID: %s", city_id)
        # Make API call to get shipping cost
        api_url = f'https://api.yalidine.app/v1/deliveryfees/?wilaya_id={city_id}'
        api_id = '30766545130987580386'
        api_token = 'ImVbOQcUYtikAM6i8e3qM754wJ5lSuBzTFzaldoFOAvhHWcPf2DYugk1S6xDXXsP'
        headers = {
            'X-API-ID': api_id,
            'X-API-TOKEN': api_token
        }

        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            data = response.json().get('data', [])
            for item in data:
                if item.get('wilaya_id') == city_id:
                    home_fee = item.get('home_fee', 0)
                    shipping_cost = home_fee
                    _logger.info("Shipping cost retrieved successfully: %s", shipping_cost)
                    return shipping_cost
        else:
            _logger.error("Failed to retrieve shipping cost from API")
            shipping_cost = 0  # Default to 0 if API call fails

        return shipping_cost
