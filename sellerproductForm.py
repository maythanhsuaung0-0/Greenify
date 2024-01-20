from wtforms import Form, StringField, FileField, TextAreaField, IntegerField, DecimalField, validators
from set_image import create_image_set


class CreateProductForm(Form):
    product_name = StringField('Product Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    product_price = DecimalField('Price ($)', [validators.NumberRange(min=1), validators.DataRequired()])
    product_stock = IntegerField('Stock', [validators.NumberRange(min=100), validators.DataRequired()])
    image = FileField('Product Image', [validators.DataRequired(), validators.regexp(r'^[^/\\]*\.(jpg|png)$', message='Only JPG or PNG files are accepted')])
    description = TextAreaField('Product Description', [validators.Optional()])