from wtforms import Form, StringField, FileField, TextAreaField, IntegerField, DecimalField, validators


class CreateProductForm(Form):
    product_name = StringField('Product Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    product_price = DecimalField('Price ($)', [validators.NumberRange(min=1), validators.DataRequired()])
    product_stock = IntegerField('Stock', [validators.NumberRange(min=20), validators.DataRequired()])
    image = FileField('Product Image', [validators.DataRequired()])
    description = TextAreaField('Product Description', [validators.Optional()])
