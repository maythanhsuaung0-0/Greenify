class Product:
    def __init__(self):
        self.__name = None
        self.__desp = None
        self.__qty = None
        self.__multimedia = None
        self.__options = None

    def get_name(self):
        return self.__name

    def get_desp(self):
        return self.__desp

    def get_qty(self):
        return self.__qty

    def get_multimedia(self):
        return self.__multimedia

    def get_options(self):
        return self.__options

    def set_name(self, name):
        self.__name = name

    def set_desp(self, desp):
        self.__desp = desp

    def set_qty(self, qty):
        self.__qty = qty

    def set_multimedia(self, multimedia):
        self.__multimedia = multimedia

    def set_options(self, options):
        self.__options = options

