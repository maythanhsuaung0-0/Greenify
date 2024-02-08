class SellerOrder:
    def __init__(self, name, email, address, date, order_id):
        self.__name = name
        self.__email = email
        self.__address = address
        self.__date = date
        self.__order_id = order_id
        self.__order_products = []
        self.__total_products = 0
        self.__sent_out = False
        self.__total = 0

    def set_name(self, name):
        self.__name = name

    def set_email(self, email):
        self.__email =email

    def set_address(self, address):
        self.__address = address

    def set_order_products(self, id, qty, product_price):
        self.__order_products.append({'product_id': id, 'quantity': qty, 'product_price': product_price })


    def set_sent_out(self, status):
        self.__sent_out = status

    def set_date(self, date):
        self.__date = date

    def set_order_id(self, order_id):
        self.__order_id = order_id

    def set_total(self, total):
        self.__total += int(total)

    def set_total_products(self,product):
        print(product)
        self.__total_products += int(product)

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

    def get_date(self):
        return self.__date

    def get_order_id(self):
        return self.__order_id

    def get_total(self):
        return self.__total

    def get_total_products(self):
        return self.__total_products