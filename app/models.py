from database import db
from datetime import date, datetime
from flask_login import UserMixin

class NewsLetters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subscription_newsletter = db.Column(db.String(), nullable=True)

class Blogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    content = db.Column(db.Text, nullable=False)
    file = db.Column(db.String(), nullable=False)
    alt = db.Column(db.String(), nullable=False)
    title_tag = db.Column(db.String(), nullable=False)
    url_link = db.Column(db.String(), nullable=False)
    meta_description = db.Column(db.Text, nullable=False)
    keyword = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Returns only the month and year: March 2023
    def formatted_date(self):
        return self.date_posted.strftime("%B %Y")

    # Returns day, month, and year: 15 March 2023
    def formatted_date_with_day(self):
        return self.date_posted.strftime("%d %B %Y")

    # Returns time: 9:30 am
    def formatted_time(self):
        return self.date_posted.strftime("%I:%M %p").lstrip('0')

    def time_since_posted(self):
        time_diff = datetime.now() - self.date_posted
        hours, remainder = divmod(time_diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if time_diff.days > 0:
            return f"{time_diff.days} days ago"
        elif hours > 0:
            return f"{hours} hours ago"
        elif minutes > 0:
            return f"{minutes} minutes ago"
        else:
            return "just now"

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_title = db.Column(db.String(), nullable=False)
    task_priority = db.Column(db.String(), nullable=False)
    task_description = db.Column(db.Text, nullable=False)
    task_submission_url = db.Column(db.String(), nullable=True)
    task_status = db.Column(db.String(), nullable=True)
    task_deadline = db.Column(db.String(), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def formatted_date(self):
        return self.date_added.strftime("%B %Y")

    def formatted_date_with_day(self):
        return self.date_added.strftime("%d %B %Y")

    def formatted_time(self):
        return self.date_added.strftime("%I:%M %p").lstrip('0')

    def time_since_posted(self):
        time_diff = datetime.now() - self.date_added
        hours, remainder = divmod(time_diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if time_diff.days > 0:
            return f"{time_diff.days} days ago"
        elif hours > 0:
            return f"{hours} hours ago"
        elif minutes > 0:
            return f"{minutes} minutes ago"
        else:
            return "just now"

class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(), nullable=False)
    event_description = db.Column(db.Text, nullable=False)
    event_location = db.Column(db.String(), nullable=False)
    event_url = db.Column(db.String(), nullable=False)
    event_time = db.Column(db.String(), nullable=False)
    event_date = db.Column(db.String(), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def formatted_date(self):
        return self.date_added.strftime("%B %Y")

    def formatted_date_with_day(self):
        return self.date_added.strftime("%d %B %Y")

    def formatted_time(self):
        return self.date_added.strftime("%I:%M %p").lstrip('0')

    def time_since_posted(self):
        time_diff = datetime.now() - self.date_added
        hours, remainder = divmod(time_diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if time_diff.days > 0:
            return f"{time_diff.days} days ago"
        elif hours > 0:
            return f"{hours} hours ago"
        elif minutes > 0:
            return f"{minutes} minutes ago"
        else:
            return "just now"

class CourseMonitors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_course_point = db.Column(db.Integer, default=0)
    user_course_progress = db.Column(db.Integer, default=0)
    user_course_status = db.Column(db.Boolean, default=False)
    course = db.relationship('Courses', backref='monitors', single_parent=True, cascade='all, delete-orphan')
    date_started = db.Column(db.DateTime, default=datetime.utcnow)

    def formatted_date(self):
        return self.date_added.strftime("%B %Y")

    def formatted_date_with_day(self):
        return self.date_added.strftime("%d %B %Y")

    def formatted_time(self):
        return self.date_added.strftime("%I:%M %p").lstrip('0')

    def time_since_posted(self):
        time_diff = datetime.now() - self.date_added
        hours, remainder = divmod(time_diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if time_diff.days > 0:
            return f"{time_diff.days} days ago"
        elif hours > 0:
            return f"{hours} hours ago"
        elif minutes > 0:
            return f"{minutes} minutes ago"
        else:
            return "just now"

class TaskMonitors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_point = db.Column(db.Integer, default=0)
    user_progress = db.Column(db.Integer, default=0)
    user_task_status = db.Column(db.Boolean, default=False)
    task = db.relationship('Tasks', backref='taskmonitors', single_parent=True, cascade='all, delete-orphan')
    date_started = db.Column(db.DateTime, default=datetime.utcnow)

    def formatted_date(self):
        return self.date_added.strftime("%B %Y")

    def formatted_date_with_day(self):
        return self.date_added.strftime("%d %B %Y")

    def formatted_time(self):
        return self.date_added.strftime("%I:%M %p").lstrip('0')

    def time_since_posted(self):
        time_diff = datetime.now() - self.date_added
        hours, remainder = divmod(time_diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if time_diff.days > 0:
            return f"{time_diff.days} days ago"
        elif hours > 0:
            return f"{hours} hours ago"
        elif minutes > 0:
            return f"{minutes} minutes ago"
        else:
            return "just now"

class CourseRegistration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    course_registration_status = db.Column(db.Boolean, default=False)
    date_started = db.Column(db.DateTime, default=datetime.utcnow)

    def formatted_date(self):
        return self.date_added.strftime("%B %Y")

    def formatted_date_with_day(self):
        return self.date_added.strftime("%d %B %Y")

    def formatted_time(self):
        return self.date_added.strftime("%I:%M %p").lstrip('0')

    def time_since_posted(self):
        time_diff = datetime.now() - self.date_added
        hours, remainder = divmod(time_diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if time_diff.days > 0:
            return f"{time_diff.days} days ago"
        elif hours > 0:
            return f"{hours} hours ago"
        elif minutes > 0:
            return f"{minutes} minutes ago"
        else:
            return "just now"

class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_title = db.Column(db.String(), nullable=False)
    course_description = db.Column(db.Text(), nullable=False)
    course_duration = db.Column(db.String(), nullable=False)
    course_lesson = db.Column(db.String(), nullable=False)
    course_img = db.Column(db.String(), nullable=True)
    course_video = db.Column(db.String(), nullable=True)
    courses_instructor = db.Column(db.String(), nullable=True)
    courses_url = db.Column(db.String(), nullable=True)
    courses_schedule = db.Column(db.String(), nullable=True)
    courses_price = db.Column(db.Integer, nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    course_foreignkey = db.relationship('CourseRegistration', backref='registrations', single_parent=True, cascade='all, delete-orphan')
    
    def formatted_date(self):
        return self.date_added.strftime("%B %Y")

    def formatted_date_with_day(self):
        return self.date_added.strftime("%d %B %Y")

    def formatted_time(self):
        return self.date_added.strftime("%I:%M %p").lstrip('0')

    def time_since_posted(self):
        time_diff = datetime.now() - self.date_added
        hours, remainder = divmod(time_diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if time_diff.days > 0:
            return f"{time_diff.days} days ago"
        elif hours > 0:
            return f"{hours} hours ago"
        elif minutes > 0:
            return f"{minutes} minutes ago"
        else:
            return "just now"

class CourseRegisters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_title_registered = db.Column(db.String(), nullable=False)
    course_description_registered = db.Column(db.Text(), nullable=False)
    course_duration_registered = db.Column(db.String(), nullable=False)
    course_lesson_registered = db.Column(db.String(), nullable=False)
    course_lesson_registered_status = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def formatted_date(self):
        return self.date_added.strftime("%B %Y")

    def formatted_date_with_day(self):
        return self.date_added.strftime("%d %B %Y")

    def formatted_time(self):
        return self.date_added.strftime("%I:%M %p").lstrip('0')

    def time_since_posted(self):
        time_diff = datetime.now() - self.date_added
        hours, remainder = divmod(time_diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if time_diff.days > 0:
            return f"{time_diff.days} days ago"
        elif hours > 0:
            return f"{hours} hours ago"
        elif minutes > 0:
            return f"{minutes} minutes ago"
        else:
            return "just now"

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    
    # User Names
    first_name = db.Column(db.String(), nullable=True)
    last_name = db.Column(db.String(), nullable=True)
    middle_name = db.Column(db.String(), nullable=True)
    
    # User contact informations
    email = db.Column(db.String(), nullable=False, unique=True)
    contact = db.Column(db.String(), nullable=True)
    content = db.Column(db.Text(), nullable=True)

    # User Account Informations
    password_hash = db.Column(db.String())
    profile_pic = db.Column(db.String(), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # User Social Media Details
    facebook_account = db.Column(db.String(), nullable=True)
    linkedin_account = db.Column(db.String(), nullable=True)

    # Administrators Control
    user_status = db.Column(db.String(), nullable=True, default='Student')

    # Many to Many Relationship Setup
    courses = db.relationship('Courses', backref='user', lazy=True, cascade='all, delete-orphan')
    registrations = db.relationship('CourseRegistration', backref='user', lazy=True, cascade='all, delete-orphan')
    tasks = db.relationship('Tasks', backref='user', lazy=True, cascade='all, delete-orphan')
    courseregisters = db.relationship('CourseRegisters', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def formatted_date(self):
        return self.date_added.strftime("%B %Y")

    def formatted_date_with_day(self):
        return self.date_added.strftime("%d %B %Y")

    def formatted_time(self):
        return self.date_added.strftime("%I:%M %p").lstrip('0')

    def time_since_posted(self):
        time_diff = datetime.now() - self.date_added
        hours, remainder = divmod(time_diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if time_diff.days > 0:
            return f"{time_diff.days} days ago"
        elif hours > 0:
            return f"{hours} hours ago"
        elif minutes > 0:
            return f"{minutes} minutes ago"
        else:
            return "just now"

    @property
    def password(self):
        raise AttributeError(' Password Not A Readable Attribute !!! ')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # create string
    def __repr__(self):
        return '<Name %r>' % self.name
