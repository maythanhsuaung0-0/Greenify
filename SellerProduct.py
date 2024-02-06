class SellerProduct:
    def __init__(self, product_name, product_price, product_stock, description):
        self.__product_id = None
        self.__product_name = product_name
        self.__product_price = product_price
        self.__product_stock = product_stock
        self.__image = ""
        self.__description = description

    def set_product_id(self, id):
        self.__product_id = id

    def get_product_id(self):
        return self.__product_id

    def set_product_name(self, product_name):
        self.__product_name = product_name

    def get_product_name(self):
        return self.__product_name

    def set_product_price(self, product_price):
        self.__product_price = product_price

    def get_product_price(self):
        return self.__product_price

    def set_product_stock(self, product_stock):
        self.__product_stock = product_stock

    def get_product_stock(self):
        return self.__product_stock

    def set_image(self, image):
        self.__image = image

    def get_image(self):
        return self.__image

    def set_description(self, description):
        self.__description = description

    def get_description(self):
        return self.__description