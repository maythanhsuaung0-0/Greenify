from wtforms import Form, StringField, validators, EmailField, PasswordField, IntegerField


class update(Form):
    search_query = StringField(label='')
    email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('', [validators.DataRequired(), validators.length(min=8, max=30)])
    confirm_password = PasswordField('', [validators.DataRequired(), validators.length(min=8, max=30)])
    name = StringField('Name', [validators.DataRequired()])
    contact_number = IntegerField('Phone Number', [validators.DataRequired(), validators.NumberRange(min=00000000, max=99999999)])
    postal_code = IntegerField('Postal Code', [validators.DataRequired(), validators.NumberRange(min=000000, max=999999)])
    address = StringField('Address', [validators.DataRequired()])