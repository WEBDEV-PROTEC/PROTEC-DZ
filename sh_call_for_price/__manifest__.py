# Part of Softhealer Technologies.
{
    "name": "Call For Price",

    "author": "Softhealer Technologies",

    "website": "https://www.softhealer.com",

    "support": "support@softhealer.com",

    "version": "14.0.1",

    "category": "eCommerce",
    
    "license": "OPL-1",

    "summary": "Manage Product Price Module,  Hide  Product Price App, Remove Goods Price Module, Temporary Invisible Product Price , Price Manage, Manage Product Price Odoo",
    "description": """Merchants occasionally have products and services where prices should be hidden for many reasons. These items might free, out of stock or their prices change frequently and need to be verified by phone, email and etc. The product prices will become a consensus between merchants and their customers. Call For Price is a tool with a flexible option, you can effectively manage all the product price status by deciding which are display, which must be contacted to know the price.The product that enables a call for the price will hide the price and “Add to cart” button, then add a button “Call for price”. The customer clicks the button to send price requests to the merchant.  """,

    "depends": ['website_sale'],

    "data": [
        'security/ir.model.access.csv',
        'views/sale_call_for_price.xml',
        'views/website_sale_template_call_price.xml',
    ],

    "images": ["static/description/background.png", ],

    "installable": True,
    "auto_install": False,
    "application": True,
    "price": "35",
    "currency": "EUR"
}
