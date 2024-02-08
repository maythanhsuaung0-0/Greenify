class SellerOrder:
    def __init__(self, name, email, address):
        self.__name = name
        self.__email = email
        self.__address = address
        self.__order_products = []
        self.__sent_out = False

    def set_name(self, name):
        self.__name = name

    def set_email(self, email):
        self.__email =email

    def set_address(self, address):
        self.__address = address

    def set_order_products(self, id, qty, date):
        self.__order_products.append({'product_id': id, 'quantity': qty, 'date': date})


    def set_sent_out(self, status):
        self.__sent_out = status

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_address(self):
        return self.__address

    def get_order_products(self):
        return self.__order_products

    def get_sent_out(self):
        return self.__sent_out