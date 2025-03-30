from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError
import phonenumbers

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class MessageForm(FlaskForm):
    recipient = StringField('Recipient Phone', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[
        DataRequired(),
        Length(min=1, max=160, message='SMS messages are limited to 160 characters')
    ])
    submit = SubmitField('Send Message')
    
    def validate_recipient(self, field):
        try:
            input_number = phonenumbers.parse(field.data, None)
            if not phonenumbers.is_valid_number(input_number):
                raise ValidationError('Invalid phone number')
        except:
            raise ValidationError('Invalid phone number format')
