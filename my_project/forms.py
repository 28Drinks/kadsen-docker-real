from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    IntegerField,
    DateField,
    RadioField,
)
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from flask_wtf.file import FileField, FileAllowed
from my_project.models import User

#register form
class RegisterForm(FlaskForm):
    def validate_username(  #check validations
        self, username_to_check
    ):  # has to be name 'validate_username' since we named it 'username' down below
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("Username already taken!")    #validation error msg

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(
            email_address=email_address_to_check.data
        ).first()
        if email_address:
            raise ValidationError("Email address already registert!")

    username = StringField(     #form content with validators
        label="User Name:", validators=[Length(min=3, max=15), DataRequired()]
    )
    email_address = StringField(
        label="Email Address:", validators=[Email(), DataRequired()]
    )
    password1 = PasswordField(
        label="Password:", validators=[Length(min=4, max=25), DataRequired()]
    )
    password2 = PasswordField(
        label="Confirm Password:", validators=[EqualTo("password1"), DataRequired()]
    )
    submit = SubmitField(label="Create Account")

#login form
class LoginForm(FlaskForm):
    username = StringField(label="User Name:", validators=[DataRequired()])
    password = PasswordField(label="Password:", validators=[DataRequired()])
    submit = SubmitField(label="Login")

#profile form
# class ProfileForm(FlaskForm):
#     name = StringField(label="Name: (min.3-max.35)", validators=[Length(min=5, max=35)])
#     picture = FileField(
#         label="Profile Picture: (jpg/png)", validators=[FileAllowed(["jpg", "png"])]  #only allow images with .ong or .jpg
#     )
#     submit = SubmitField(label="Update Profile")

