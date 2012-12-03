from wtforms import Form, BooleanField, TextField, validators

class RegistrationForm(Form):
    username     = TextField('Username', [validators.Length(min=4, max=25)])
    email        = TextField('Email Address', [validators.Length(min=6, max=35)])
    accept_rules = BooleanField('I accept the site rules', [validators.Required()])

