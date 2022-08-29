# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Multiples of Quantity in shop",
    "author": "Softhealer Technologies",
    "support": "support@softhealer.com",
    "website": "https://www.softhealer.com",
    "category": "Website",
    "summary": """Multiples Of  Quantity In Shop, Set Product Multiples Quantity App, Increase Product Quantity Module, Decrease Quantity By Customer, multiple quantity Odoo""",
    "description": """Are you planning to define the multiples of quantities to the products which you are selling on your store build up with the website? Sometimes in the shop, some products come in a bunch of 6, 12, etc. You can set easily multiples of quantity No using this module. Suppose you want to set multiples of quantity is 5, it will default the value of the product in the shop. If customers put manual quantity (manually = 8)of the product so it will automatically take higher No of quantity(higher = 10). Customers can increase or decrease the quantity of products relative to default quantity(default is 5) in shop or cart. If the customer click button "Add to Cart" in the shop, product quantity automatically sets the default quantity.
 Multiples Of  Quantity In Shop Odoo
 Set A Multiples Quantity In Shop Odoo, Increase / Decrease Product Quantity Module, Add Multiple Products Quantity By Customer Odoo.
 Set Product Multiples Quantity App, Increase Product Quantity Module, Decrease Quantity By Customer Odoo.""",
    "version": "14.0.2",
    "depends": [
        'sale_management',
        'website_sale'
    ],
    "data": [
        'security/ir.model.access.csv',
        'views/sh_product_view.xml',
        'views/res_config_settings.xml',
        'views/assets.xml',
        'views/sh_shop_template.xml',
    ],

    "images": ['static/description/background.png', ],
    "license": "OPL-1",
    "auto_install": False,
    "application": True,
    "installable": True,
    "price": 50,
    "currency": 'EUR'
}
