class ApplicationFormFormat:
    id = 1
    def __init__(self, name, email, desc, doc):
        ApplicationFormFormat.__class__.id += 1
        self.__id = ApplicationFormFormat.__class__.id
        self.__name = name
        self.__email = email
        self.__desc = desc
        self.__doc = doc
    
    def set_name(self, name):     
        self.__name = name

    def set_email(self, email):
        self.__email = email

    def set_desc(self, desc):     
        self.__desc = desc

    def set_doc(self, doc):
        self.__doc = doc
    
    def get_name(self):
        return self.__name
    
    def get_email(self):
        return self.__email
    
    def get_desc(self):        
        return self.__desc
    
    def get_doc(self):
        return self.__doc

    def get_application_id(self):
        return self.__id
        