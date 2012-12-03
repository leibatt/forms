from wtforms import Form, BooleanField, TextField, validators

class RegistrationForm(Form):
    username     = TextField('Username', [validators.Length(min=4, max=25,message="must be 4-25 characters")])
    email        = TextField('Email Address', [validators.Length(min=6),validators.Email(message="this doesn't seem like an email")])
    password        = TextField('Password', [validators.Length(min=6, max=35,message="must be 6-35 characters")])
    accept_rules = BooleanField('I accept the site rules', [validators.Required(message="must accept site rules to proceed")])

