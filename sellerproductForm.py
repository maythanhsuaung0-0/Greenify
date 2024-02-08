import re
from wtforms import Form, StringField, FileField, TextAreaField, IntegerField, DecimalField, validators


def no_special_characters(form, field):
    if not re.match(r'^[a-zA-Z0-9\s]+$', field.data):
        raise validators.ValidationError('Must not contain special characters')


class CreateProductForm(Form):
    product_name = StringField('Product Name', [validators.Length(min=1, max=150), validators.DataRequired(), no_special_characters])
    product_price = DecimalField('Price ($)', [validators.NumberRange(min=1), validators.DataRequired()])
    product_stock = IntegerField('Stock', [validators.NumberRange(min=100, max=500), validators.DataRequired()])
    image = FileField('Product Image', [validators.Optional(), validators.regexp(r'^[^/\\]*\.(jpg|png)$', message='Only JPG or PNG files are accepted')])
    description = TextAreaField('Product Description', [validators.Optional(), no_special_characters])
