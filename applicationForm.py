from wtforms import Form, StringField, EmailField, TextAreaField, FileField, validators


class ApplicationForm(Form):
    business_name = StringField('Business Name', [validators.data_required(), validators.length(max=15)])
    business_desc = TextAreaField("Business Description", [validators.data_required()])
    seller_email = EmailField("Email Address", [validators.data_required(), validators.email()])
    support_document = FileField("Supporting documents", [validators.optional(), validators.regexp('^[^/\\]\.jpg$')])
