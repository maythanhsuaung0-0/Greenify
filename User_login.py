class UserLogin:

    def __init__(self, email, password):
        self.__email = email
        self.__password = password

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    def set_email(self, email):
        self.__email = email

    def set_password(self, password):
        self.__password = password

    def check_password(self, entered_password):
        return self.__password == entered_password
