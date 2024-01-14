from wtforms import Form, StringField, EmailField, TextAreaField, FileField, validators


class ApplicationForm(Form):
    business_name = StringField('Business Name', [validators.DataRequired(), validators.length(max=15)])
    business_desc = TextAreaField("Business Description", [validators.DataRequired()])
    seller_email = EmailField("Email Address", [validators.DataRequired(), validators.Email()])
    support_document = FileField('Upload Supporting Document (* pdf file only *)', [validators.optional()],render_kw={'accept': '.pdf'})
