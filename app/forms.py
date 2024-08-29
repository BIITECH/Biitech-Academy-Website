from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField

class BlogForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    content = CKEditorField(validators=[DataRequired()])
    file = FileField()
    alt = StringField(validators=[DataRequired()])
    title_tag = StringField(validators=[DataRequired()])
    url_link = StringField(validators=[DataRequired()])
    meta_description = TextAreaField(validators=[DataRequired()])
    keyword = TextAreaField(validators=[DataRequired()])
    submit = SubmitField()

class OTPForm(FlaskForm):
    otp = StringField(validators=[DataRequired()])
    submit = SubmitField()

class PaymentForm(FlaskForm):
    client_name = StringField(validators=[DataRequired()])
    client_email = StringField(validators=[DataRequired()])
    price_field = StringField(validators=[DataRequired()])
    submit = SubmitField()

class NewsLettersForm(FlaskForm):
    newsletters_email = StringField(validators=[DataRequired()])
    submit = SubmitField()

class TaskForm(FlaskForm):
    task_title = StringField(validators=[DataRequired()])
    task_priority = StringField(validators=[DataRequired()])
    task_description = CKEditorField(validators=[DataRequired()])
    task_submission_url = StringField()
    task_status = StringField()
    task_deadline = StringField()
    submit = SubmitField()

class EventForm(FlaskForm):
    event_name = StringField(validators=[DataRequired()])
    event_description = CKEditorField(validators=[DataRequired()])
    event_location = StringField(validators=[DataRequired()])
    event_url = StringField(validators=[DataRequired()])
    event_time = StringField(validators=[DataRequired()])
    event_date = StringField(validators=[DataRequired()])
    submit = SubmitField()

class CoursesForm(FlaskForm):
    course_title = StringField(validators=[DataRequired()])
    course_description = CKEditorField()
    course_duration = StringField(validators=[DataRequired()])
    course_lesson = StringField(validators=[DataRequired()])
    course_img = FileField()
    course_video = StringField(validators=[DataRequired()])
    courses_instructor = StringField(validators=[DataRequired()])
    courses_url = StringField(validators=[DataRequired()])
    courses_schedule = StringField(validators=[DataRequired()])
    courses_price = StringField(validators=[DataRequired()])
    submit = SubmitField()

class MessagesForm(FlaskForm):
    recipient_emails = StringField(validators=[DataRequired()])
    phone = StringField(validators=[DataRequired()])
    subject = StringField(validators=[DataRequired()])
    message = StringField(validators=[DataRequired()])
    submit = SubmitField()

class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField()

class UserForm(FlaskForm):
	# User Names
    first_name = StringField(validators=[DataRequired()])
    last_name = StringField(validators=[DataRequired()])
    middle_name = StringField(validators=[DataRequired()])

    # User contact informations
    email = StringField(validators=[DataRequired()])
    contact = StringField(validators=[DataRequired()])
    content = CKEditorField()
    user_status = StringField()

    # User contact informations
    password_hash = PasswordField(validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match!')])
    password_hash2 = PasswordField(validators=[DataRequired()])
    profile_pic = FileField()
    
    facebook_account = StringField()
    linkedin_account = StringField()
    submit = SubmitField()

class ForgotPasswordForm(FlaskForm):
    email = StringField(validators=[DataRequired()])
    submit = SubmitField()

class ResetPasswordForm(FlaskForm):
    password_hash = PasswordField(validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match!')])
    password_hash2 = PasswordField(validators=[DataRequired()])
    submit = SubmitField()

class SearchForm(FlaskForm):
    searched = StringField(validators=[DataRequired()])
    submit = SubmitField()

class PasswordForm(FlaskForm):
    email = StringField(validators=[DataRequired()])
    password_hash = PasswordField(validators=[DataRequired()])
    submit = SubmitField()

class NamerForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    submit = SubmitField()
