class SellerOrder:
    def __init__(self, name, email, address):
        self.__name = name
        self.__email = email
        self.__address = address
        self.__order_products = []

    def set_name(self, name):
        self.__name = name

    def set_email(self, email):
        self.__email =email

    def set_address(self, address):
        self.__address = address

    def set_order_products(self, id, qty):
        self.__order_products.append({'product_id': id, 'quantity': qty})

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_address(self):
        return self.__address

    def get_order_products(self):
        return self.__order_products
