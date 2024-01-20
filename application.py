class ApplicationFormFormat:
    id = 0
    def __init__(self,id,s_name,name, email, desc):
        ApplicationFormFormat.id = id
        ApplicationFormFormat.id += 1
        self.__id = ApplicationFormFormat.id
        self.__seller_name = s_name
        self.__name = name
        self.__email = email
        self.__password = None
        self.__profile_image = None
        self.__desc = desc
        self.__doc = None
        self.__date = None

    def set_profile_image(self,img):
        self.__profile_image = img

    def set_seller_name(self,n):
        self.__seller_name = n

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

    def get_seller_name(self):
        return self.__seller_name

    def get_name(self):
        return self.__name
    
    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    def get_profile_image(self):
        return self.__profile_image

    def get_desc(self):        
        return self.__desc
    
    def get_doc(self):
        return self.__doc

    def get_application_id(self):
        return self.__id

    def get_date(self):
        return self.__date
        