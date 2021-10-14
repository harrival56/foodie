from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length

class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class UserEditForm(FlaskForm):
    """Form for editing users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])


class MenuForm(FlaskForm):
    """Form for adding menu"""

    # title = StringField("Title", validators=[DataRequired()])
    day = SelectField("Day", choices=[('Monday', 'mon'), ("Tuesday", 'tue'),
    ('Wednesday','wen'), ('Thursday','thur'), ('Friday', 'fri'),
    ('Saturday', 'sat'), ('Sunday', 'sun')], validators=[DataRequired()])
    time = SelectField("Time", choices=[('Breakfast','Breakfast'),
    ('Lunch', 'Lunch'), ('Dinner','Dinner')], validators=[DataRequired()])