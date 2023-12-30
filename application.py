class ApplicationFormFormat:
    id = 0
    def __init__(self, name, email, desc):
        ApplicationFormFormat.id += 1
        self.__id = ApplicationFormFormat.id
        self.__name = name
        self.__email = email
        self.__password = None
        self.__desc = desc
        self.__doc = None
        self.__date = None

    def get_id(self):
        return self.__id

    def set_name(self, name):     
        self.__name = name

    def set_email(self, email):
        self.__email = email

    def set_password(self,pw):
        self.__password = pw

    def set_desc(self, desc):     
        self.__desc = desc

    def set_doc(self, doc):
        self.__doc = doc

    def set_date(self,date):
        self.__date = date

    def get_name(self):
        return self.__name
    
    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    def get_desc(self):        
        return self.__desc
    
    def get_doc(self):
        return self.__doc

    def get_application_id(self):
        return self.__id

    def get_date(self):
        return self.__date
        