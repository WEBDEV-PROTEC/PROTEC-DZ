import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

class YalidineAPIController(http.Controller):

    @http.route('/shop/delivery', type='http', auth='public', website=True)
    def index(self):
        # Get the current order ID from the session
        order_id = request.session.get('sale_order_id')
        name = request.session.get('name')
        delivery_address = request.session.get('delivery_address')
        delivery_history = [
            {'date': '2024-04-30', 'event': 'Package picked up'},
            {'date': '2024-05-02', 'event': 'In transit'},
            {'date': '2024-05-05', 'event': 'Out for delivery'},
            {'date': '2024-05-06', 'event': 'Delivered'}
        ]

        _logger.info("Received request to display delivery information for order ID: %s", order_id)
        # Log the delivery address information
        _logger.info("Delivery address requested from session variable: %s", delivery_address)

        return request.render('yalidine_odoo_cod.delivery_histories', {
            'delivery_history': delivery_history
        })
        
    @http.route('/shop/confirmation', type='http', auth='public', website=True)
    def process_payment(self, **kwargs):
        # Retrieve the order ID
        order_id = request.session.get('sale_order_id')
        if not order_id:
            _logger.warning("Order ID not found in session")
            return "Order ID not found in session"
        _logger.info("Starting controller process payment")
        order = request.env['sale.order'].sudo().browse(order_id)

        # Retrieve customer information from the order
        customer_name = order.partner_id.name or ''
        customer_phone = order.partner_id.phone or ''
        customer_address = order.partner_id.street or ''
        customer_city = order.partner_id.city or ''
        _logger.info("Calculating values and fetching products names from cart")
        # Calculate total amount, total weight, and product names
        items_value, total_amount, total_weight, product_names, shipping_cost = calculate_total_amount_weight_and_shipping_cost(order_id, customer_city)

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
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            _logger.info("Parcel created successfully: %s", response.json())
            return "Parcel created successfully"
        except requests.RequestException as e:
            _logger.error("Error creating parcel: %s", e)
            return "Error creating parcel: %s" % e
            
    def calculate_total_amount_weight_and_shipping_cost(order_id, city):
        order = self.env['sale.order'].sudo().browse(order_id)
        items_value = sum(order.order_line.mapped('price_total'))
        total_weight = sum(order.order_line.mapped('product_id.weight'))
        product_names = [line.product_id.name for line in order.order_line]
        _logger.info("Calculating total amount and weight")
        # Get the city ID (assuming 'city' is the name of the city)
        city_id = get_city_id(city)
    
        # Calculate shipping cost
        shipping_cost = calculate_shipping_cost(city_id)
        total_amount = shipping_cost + items_value
        
        return items_value, total_weight, product_names, shipping_cost, total_amount, product_names 

    def get_city_id(city_name):
        # Dictionary mapping city names to their corresponding ID
        city_ids = {
            'Adrar': 1,
            'Chlef': 2,
            'Laghouat': 3,
            'Oum El Bouaghi': 4,
            'Batna': 5,
            'Bejaïa': 6,
            'Biskra': 7,
            'Béchar': 8,
            'Blida': 9,
            'Bouira': 10,
            'Tamanrasset': 11,
            'Tebessa': 12,
            'Tlemcen': 13,
            'Tiaret': 14,
            'Tizi Ouzou': 15,
            'Alger': 16,
            'Djelfa': 17,
            'Djijel': 18,
            'Sétif': 19,
            'Saïda': 20,
            'Skikda': 21,
            'Sidi Bel Abbès': 22,
            'Annaba': 23,
            'Guelma': 24,
            'Constantine': 25,
            'Médéa': 26,
            'Mostaganem': 27,
            "M'Sila": 28,
            'Mascara': 29,
            'Ouargla': 30,
            'Oran': 31,
            'El Bayadh': 32,
            'Illizi': 33,
            'Bordj Bou Arreridj': 34,
            'Boumerdès': 35,
            'El Tarf': 36,
            'Tindouf': 37,
            'Tissemsilt': 38,
            'El Oued': 39,
            'Khenchela': 40,
            'Souk Ahras': 41,
            'Tipaza': 42,
            'Mila': 43,
            'Aïn Defla': 44,
            'Naâma': 45,
            'Aïn Témouchent': 46,
            'Ghardaia': 47,
            'Relizane': 48
        }
    
        return city_ids.get(city_name, 0)  # Return 0 if city not found
    
    def calculate_shipping_cost(city_id):
        if city_id == 0:
            print('city id is 0')
            return 0  # City not found, shipping cost is 0
        
        _logger.info("Calculating total amount and weight")
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
                    return shipping_cost
            print(f'shipping costs from api {shipping_cost}')
        else:
            print("failed api call")
            shipping_cost = 0  # Default to 0 if API call fails
    
        return shipping_cost
