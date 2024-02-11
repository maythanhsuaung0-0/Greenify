from wtforms import Form, StringField, EmailField, TextAreaField, FileField, validators


def no_special_characters(form, field):
    special_characters = "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?"
    if any(char in special_characters for char in field.data):
        raise validators.ValidationError("Special characters are not allowed.")


class ApplicationForm(Form):
    seller_name = StringField('Fullname', validators=[validators.DataRequired(), no_special_characters])
    business_name = StringField('Business Name', validators=[validators.DataRequired(), no_special_characters])
    business_desc = TextAreaField("Business Description", validators=[validators.DataRequired(), no_special_characters])
    seller_email = EmailField("Email Address", [validators.DataRequired(), validators.Email()])
    support_document = FileField('Upload Supporting Document (* pdf file only *)', [validators.optional()],render_kw={'accept': '.pdf'})
