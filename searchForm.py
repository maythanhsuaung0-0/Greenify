from wtforms import Form, StringField

class Search(Form):
    search_query = StringField(label='')