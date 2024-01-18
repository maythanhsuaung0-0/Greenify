class User:
    count_id = 0

    def __init__(self, email, password, name, contact_number, postal_code, address):
        User.count_id += 1
        self.__user_id = User.count_id
        self.__email = email
        self.__password = password
        self.__name = name
        self.__contact_number = contact_number
        self.__postal_code = postal_code
        self.__address = address
        self.__login = False

    def get_user_id(self):
        return self.__user_id

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    def get_login_status(self):
        return self.__login

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_email(self, email):
        self.__email = email

    def set_password(self, password):
        self.__password = password

    def set_login_status(self, login):
        self.__login = login

    def get_name(self):
        return self.__name

    def get_contact_number(self):
        return self.__contact_number

    def get_postal_code(self):
        return self.__postal_code

    def get_address(self):
        return self.__address

    def set_name(self, name):
        self.__name = name

    def set_contact_number(self, contact_number):
        self.__contact_number = contact_number

    def set_postal_code(self, postal_code):
        self.__postal_code = postal_code

    def set_address(self, address):
        self.__address = address