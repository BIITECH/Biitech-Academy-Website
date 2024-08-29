from flask import *
from forms import *
from models import *
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from flask_ckeditor import upload_success, upload_fail
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from flask_wtf.csrf import CSRFProtect
from flask_ckeditor import CKEditor
import urllib.request
from database import db
import uuid as uuid
import os
import logging
import requests
import random

# Mail Jet
from mailjet_rest import Client
from mail.send_reply import MailSender
from mail.mailing_code import AdminUpdate

# Create instances for both MailSender and AdminUpdate
mail_sender = MailSender()
admin_update_mail = AdminUpdate()

# Cloudinary CDN Service
import cloudinary
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

# Flask Admin
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
ckeditor = CKEditor(app)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biitech-academy.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://biitech_academy_database_user:nfHPWg17KyVlXqRdz8lONGxqTQ0OJCCP@dpg-cp7i2om3e1ms73akun3g-a.oregon-postgres.render.com/biitech_academy_database'
app.config['SECRET_KEY'] = "cairocoders-ednalan"
app.config['FLASK_DEBUG'] = True

cloudinary.config(
    cloud_name="biitech-academy-content",
    api_key="391767891145195",
    api_secret="lrc2j9zAIkB4A9vRDBJP5bkVH6I",
)

upload("https://upload.wikimedia.org/wikipedia/commons/a/ae/Olympic_flag.jpg",
       public_id="olympic_flag")
url, options = cloudinary_url(
    "olympic_flag", width=100, height=150, crop="fill")

UPLOAD_FOLDER = 'static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_EXTENSIONS'] = [
    'jpg', 'jpeg', 'png', 'JPG', 'gif', 'PNG', 'JPEG']
app.config['CKEDITOR_FILE_UPLOADER'] = 'upload'

# Paystack configuration
PAYSTACK_SECRET_KEY = 'SK_TEST_49A761Ad2E3efdbcae223606ab466f0a6371db99'

# initializing the database
db.init_app(app)
admin = Admin(app, name='Biitech Academy Admin', template_mode='bootstrap3')
# Admin access
column_list = ['user_id']
admin.add_view(ModelView(Users, db.session))
admin.add_view(ModelView(CourseRegisters, db.session))
admin.add_view(ModelView(Courses, db.session))
admin.add_view(ModelView(CourseRegistration, db.session))
admin.add_view(ModelView(TaskMonitors, db.session))
admin.add_view(ModelView(CourseMonitors, db.session))
admin.add_view(ModelView(NewsLetters, db.session))
admin.add_view(ModelView(Blogs, db.session))

migrate = Migrate(app, db)

# Flask_Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Replace these values with your Google API credentials
CLIENT_ID = '656892946937-vphteod8aaec3east0ivec80svo7dgko.apps.googleusercontent.com'
CLIENT_SECRET = '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'
REDIRECT_URI = 'https://biitechacademy.com/google-callback/account-redirect'

# Google Authentication
GOOGLE_AUTH_URL = 'https://accounts.google.com/o/oauth2/auth'
GOOGLE_TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'
GOOGLE_USERINFO_URL = 'https://www.googleapis.com/oauth2/v1/userinfo'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

app.config['MAX_CONTENT_LENGTH'] = 16 * 900 * 900
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'JPG', 'gif', 'PNG', 'JPEG'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
@app.route('/renaissance/admin/auth/user/create-blog-post', methods=['GET', 'POST'])
@login_required
def create_post():   
    form = BlogForm() 
    if form.validate_on_submit():
        creator_id = current_user.id
        blog = Blogs(
            title=form.title.data,
            content=form.content.data,
            file=form.file.data,
            alt=form.alt.data,
            title_tag=form.title_tag.data,
            url_link=form.url_link.data,
            meta_description=form.meta_description.data,
            keyword=form.keyword.data,
            user_id=creator_id
        )

        if form.file.data:
            blog.file = form.file.data
            filename = secure_filename(blog.file.filename)
            file_name = str(uuid.uuid1()) + "_" + filename
            saver = form.file.data
            blog.file = file_name

            try:
                upload_result = cloudinary.uploader.upload(
                    saver, folder="biitech-academy-uploads")
                blog.file = upload_result['public_id']
                db.session.add(blog)
                db.session.commit()
                flash("Blog post has been created successfully.")
                return redirect(url_for("dashboard"))
            except Exception as e:
                flash(f"Error! looks like there was a problem: {e}. Try Again!")
                return redirect(url_for('create_post', form=form))
        else:
            db.session.add(blog)
            db.session.commit()
            flash("Blog article successfully created !")
            return redirect(url_for("dashboard"))

        form.title.data = ''
        form.content.data = ''
        form.file.data = ''
        form.alt.data = ''
        form.title_tag.data = ''
        form.url_link.data = ''
        form.meta_description.data = ''
        form.keyword.data = ''

    blogs = Blogs.query.order_by(Blogs.date_posted.desc()).all
    blog = Blogs.query.order_by(Blogs.date_posted.desc()).all
    return render_template('pages/create-blog.html',
        title_tag="",
        meta_description="",
        keywords="",
        form=form,
        blog=blog,
        blogs=blogs,
        url_link="https://www.renaissance.com/renaissance/renaissance/admin/auth/user/create-blog-post",
        revised="20th of May 2024",
    )

@app.route('/renaissance/admin/auth/user/edit-blog-post/<int:id>', methods=['GET', 'POST'])
def edit_post(id): 
    blog = Blogs.query.get_or_404(id)
    form = BlogForm(obj=blog) 

    title_tag = blog.title_tag
    meta_description = blog.meta_description
    keyword = blog.keyword

    if form.validate_on_submit():
        blog.title = form.title.data
        blog.content = form.content.data
        blog.title_tag = form.title_tag.data
        blog.url_link = form.url_link.data
        blog.meta_description = form.meta_description.data
        blog.keyword = form.keyword.data
        db.session.commit()

        flash("Your blog post has been successfully updated!")
        return redirect(url_for("posts"))

    return render_template('pages/edit-blog.html',
        title_tag=title_tag,
        meta_description=meta_description,
        keywords=keyword,
        form=form,
        revised="20th of May 2024",
    )

@app.route('/blog-posts/delete/<int:id>')
@login_required
def delete_post(id):
    post_to_delete = Blogs.query.get_or_404(id)
    id = current_user.id
    if id == post_to_delete.user_id or id == 1:
        try:
            db.session.delete(post_to_delete)
            db.session.commit()

            # return message
            flash("Blog post was deleted successfully!")

            # Grab all the post from the DataBase
            blogs = Blogs.query.order_by(Blogs.date_posted)
            return redirect(url_for('posts', blogs=blogs))

        except:
            # return error message
            flash("Whoops!!! there was a Problem deleting post try again...")
            blogs = Blogs.query.order_by(Blogs.date_posted)
            return redirect(url_for('dashboard_blog', blogs=blogs))
    else:
        # return message
        flash("You are not authorized to Delete this Post!")
        # Grab all the post from the DataBase
        blogs = Blogs.query.order_by(Blogs.date_posted)
        return redirect(url_for('posts', blogs=blogs))

@app.route('/biitech-academy/blog', methods=['GET', 'POST'])
def blog():
    return render_template('pages/blog.html',
        title_tag="Biitech Academy Blog | Insights and Updates",
        meta_description="Stay updated with the latest insights, news, and updates from Biitech Academy. Explore our blog for articles on tech education and career development.",
        keywords="tech blog, Biitech Academy updates, IT education, career insights, tech news, professional development, tech articles, learning resources, industry trends, educational blog",
        url_link="https://www.biitechacademy.com/biitech-academy/blog",
        revised="20th of February 2024",
    )

@app.route('/', methods=['GET', 'POST'])
def index():
    courses = Courses.query.order_by(Courses.date_created.desc())
    return render_template('index.html',
        title_tag="Biitech Academy | Learn Train Thrive",
        meta_description="Empowering tomorrow's tech leaders with tailored programs, career guidance, and professional development.",
        keywords="tech education, career guidance, networking, job search support, professional development, IT skills, industry professionals, tech training, mentorship, personalized learning, Biitech Academy, IT courses, tech careers, learning journey, tech leaders",
        url_link="https://www.biitechacademy.com",
        revised="20th of February 2024",
        courses=courses,
    )

@app.route('/biitech-academy/course-list', methods=['GET', 'POST'])
def courses():
    created_courses = Courses.query.order_by(Courses.date_created.desc())
    return render_template('pages/courses.html',
        created_courses=created_courses,
        title_tag="Biitech Academy Courses | Explore Your Tech Career",
        meta_description="Discover tailored IT courses at Biitech Academy. Empower your tech career with our expert-led programs and professional development opportunities.",
        keywords="IT courses, tech education, career training, Biitech Academy, professional development, tech skills, industry professionals, tech careers, course list, learning programs, IT training, tech learning, personalized courses, tech industry, educational opportunities",
        url_link="https://www.biitechacademy.com/biitech-academy/course-list",
        revised="20th of February 2024",
    )

@app.route('/biitech-academy/course-details/<int:id>', methods=['GET', 'POST'])
def course(id):
    form = PaymentForm()
    course = Courses.query.get_or_404(id)
    created_courses = Courses.query.order_by(Courses.date_created.desc()).all()

    # Ensure course_title and course_description exist and have enough length
    title_tag = course.course_title[:50] if len(course.course_title) > 50 else course.course_title
    meta_description = course.course_description[:160] if len(course.course_description) > 160 else course.course_description
    keywords = course.course_title[:50] if len(course.course_title) > 50 else course.course_title
    
    return render_template('grid/course.html',
        created_courses=created_courses,
        course=course,
        title_tag=title_tag,
        meta_description=meta_description,
        keywords=keywords,
        url_link=f"https://www.biitechacademy.com/biitech-academy/course-details/{id}",
        revised="20th of February 2024",
        form=form,
    )

@app.route('/biitech-academy/get-in-touch/contact-form', methods=['GET', 'POST'])
def contact():
    form = MessagesForm()
    return render_template('pages/contact.html',
        title_tag="Contact Biitech Academy | Get In Touch",
        meta_description="Reach out to Biitech Academy with your questions and inquiries. Our team is here to help you with information on courses, admissions, and more.",
        keywords="contact Biitech Academy, get in touch, course inquiries, admissions questions, support, tech education help, information request, Biitech Academy contact form, communication",
        form=form,
        url_link="https://www.biitechacademy.com/biitech-academy/get-in-touch/contact-form",
        revised="20th of February 2024",
    )

@app.route('/about/biitech-academy', methods=['GET', 'POST'])
def about():
    return render_template('pages/about.html',
        title_tag="About Biitech Academy | Our Mission and Vision",
        meta_description="Learn about Biitech Academy's mission to empower tech leaders through education. Discover our vision, values, and the team dedicated to your success.",
        keywords="about Biitech Academy, mission, vision, tech education, leadership, educational values, Biitech team, empowering success, academy overview, educational goals",
        url_link="https://www.biitechacademy.com/about/biitech-academy",
        revised="20th of February 2024",
    )

@app.route('/biitech-academy/professional-programs', methods=['GET', 'POST'])
def programs():
    return render_template('pages/programs.html',
        title_tag="Biitech Academy Professional Programs | Advance Your Career",
        meta_description="Explore professional programs at Biitech Academy designed to advance your tech career. Gain industry-relevant skills and knowledge through our expert-led courses.",
        keywords="professional programs, Biitech Academy, career advancement, tech skills, industry courses, tech training, expert-led programs, career development, professional education, IT programs",
        url_link="https://www.biitechacademy.com/biitech-academy/professional-programs",
        revised="20th of February 2024",
    )

@app.route('/biitech-academy/career-services', methods=['GET', 'POST'])
def career_services():
    return render_template('pages/career.html',
        title_tag="Biitech Academy Career Services | Your Path to Success",
        meta_description="Discover career services at Biitech Academy, including personalized guidance, job search support, and networking opportunities to help you succeed in your tech career.",
        keywords="career services, Biitech Academy, job search support, career guidance, networking, professional development, tech careers, career success, IT job support, career opportunities",
        url_link="https://www.biitechacademy.com/biitech-academy/career-services",
        revised="20th of February 2024",
    )

@app.route('/biitech-academy/event-lists', methods=['GET', 'POST'])
def events():
    return render_template('event.html',
        title_tag="Biitech Academy Events | Connect and Grow",
        meta_description="Stay updated on upcoming events at Biitech Academy. Join our workshops, networking events, and seminars to connect with industry professionals and grow your tech career.",
        keywords="Biitech Academy events, workshops, networking, tech seminars, industry connections, professional growth, tech events, learning opportunities, event calendar, tech community",
        url_link="https://www.biitechacademy.com/biitech-academy/event-lists",
        revised="20th of February 2024",
    )

@app.route('/biitech-academy/becoming-a-tutor', methods=['GET', 'POST'])
def tutor():
    return render_template('tutor.html',
        title_tag="Become a Tutor at Biitech Academy | Share Your Expertise",
        meta_description="Join Biitech Academy as a tutor and share your expertise with aspiring tech professionals. Help shape the future of tech education by becoming a part of our dedicated team.",
        keywords="becoming a tutor, Biitech Academy, teach tech, tutor application, share expertise, tech education, tutor opportunities, join our team, educational impact, tech professionals",
        url_link="https://www.biitechacademy.com/biitech-academy/becoming-a-tutor",
        revised="20th of February 2024",
    )

@app.route('/auth/user/account', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash("Login Successful!")
            return redirect(url_for('index'))
        else:
            flash("The email or password provided does not match our records. Please verify your credentials and try again. If you continue to experience difficulties, consider resetting your password or contact our support team for assistance.")
    return render_template('authentication/signin.html',
        form=form,
        title_tag="Biitech Academy Login | Access Your Account",
        meta_description="Log in to your Biitech Academy account. Access your courses, progress, and personalized content to continue your learning journey.",
        keywords="login, Biitech Academy, user account, access account, login form, sign in, authentication, user login, account access, login credentials",
        url_link="https://www.biitechacademy.com/login-user/account",
        revised="20th of February 2024",
    )

@app.route('/google-callback/account-redirect')
def google_callback():
    code = request.args.get('code')
    data = {
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code',
    }
    response = requests.post(GOOGLE_TOKEN_URL, data=data)
    access_token = response.json().get('access_token')
    if access_token:
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(GOOGLE_USERINFO_URL, headers=headers)
        if response.status_code == 200:
            profile_data = response.json()
            user = Users.query.filter_by(email=profile_data['email']).first()
            if user:
                login_user(user)
                flash("Login Successful!", 'success')
                if user.id == 1:
                    return redirect(url_for('admin'))
                else:
                    return redirect(url_for('dashboard'))
            else:
                hashed_pw = generate_password_hash('your_random_password', "sha256")
                user = Users(name=profile_data['name'], email=profile_data['email'], password_hash=hashed_pw)
                db.session.add(user)
                db.session.commit()
                login_user(user)
                flash("User Created and Logged In Successfully", "success")
                return redirect(url_for('dashboard'))

    return redirect(url_for('google_login'))

@app.route('/continue/with/google')
def google_login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': 'openid email profile',
    }
    auth_url = f"{GOOGLE_AUTH_URL}?{'&'.join(f'{key}={value}' for key, value in params.items())}"
    return redirect(auth_url)

@app.route('/auth/user/create-account', methods=['GET', 'POST'])
def add_user():
    email = None
    form = UserForm()
    if form.validate_on_submit():
        # Check if user with email already exists
        user = Users.query.filter_by(email=form.email.data).first()
        if user is not None:
            flash("This User Already Exists")
            return render_template("authentication/signup.html", form=form)

        hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
        user = Users(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                middle_name=form.middle_name.data,
                email=form.email.data,
                contact=form.contact.data,
                password_hash=hashed_pw
            )
        
        # Generate a 6-digit OTP
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        session['otp'] = otp
        session['user_data'] = {
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'middle_name': form.middle_name.data,
            'email': form.email.data,
            'contact': form.contact.data,
            'password_hash': hashed_pw
        }
        
        sender_email = 'contact@biitechacademy.com'
        recipient_email = form.email.data
        subject = 'Confirmation OTP'
        api_key = '614f1d5db217f5a35c8ed583bbf4f09c'
        api_secret = '118dec95ed600a827d6400f210f3a524'

        mailjet = Client(auth=(api_key, api_secret), version='v3.1')

        data = {
            'Messages': [
                {
                    "From": {
                        "Email": sender_email,
                        "Name": "BIITECH Academy"
                    },
                    "To": [
                        {
                            "Email": recipient_email,
                            "Name": recipient_email
                        }
                    ],
                    "Subject": subject,
                    "TextPart": "",
                    "HTMLPart": f'''<div style="width: 100%; display: flex; height: auto; margin: auto; justify-content: center; align-items: center; background-color: #f0f0f0;">
                                        <div style="width: 100%; max-width: 600px; height: 100%; justify-content: center; align-items: center; max-height: 600px; background-color: #000; border-radius: 10px; margin: 10px auto; padding: 20px;">
                                          <div style="justify-content: center; align-items: center; margin: auto; padding: 0 15px;">
                                            <h2 style="font-size: 1.8em; font-weight: bold; color: #fff; text-align: center;">Enrollment Confirmation</h2>
                                            <p style="font-size: 1.2em; font-weight: 500; color: #fff; text-align: center;">Welcome to BIITECH Academy</p>
                                          </div>

                                          <div style="justify-content: center; align-items: center; margin: auto;">
                                            <p style="font-size: 1em; font-weight: 500; color: #fff; text-align: center;">Dear {recipient_email},</p>
                                            <p style="font-size: 1em; font-weight: 500; color: #fff; text-align: center;">We are delighted to welcome you to BIITECH Academy. Prepare to embark on a rewarding learning journey with us. A representative will contact you shortly. In the meantime, please enter the OTP below to get started:</p>
                                            <p style="font-size: 1em; font-weight: 500; color: #fff; text-align: center; font-family: monospace;">{otp}</p>
                                            <a href="https://www.biitechacademy.com/auth/user/account" style="width: max-content; padding: 10px 20px; margin: auto; height: auto; display: flex; justify-content: center; align-items: center; background-color: #fff; color: #000; font-size: 1em; font-weight: 500; border-radius: 10px; text-decoration: none;">Get Started Here</a>
                                          </div>
                                        </div>
                                    </div>''',
                    "CustomID": "AppGettingStartedTest"
                }
            ]
        }

        result = mailjet.send.create(data=data)
        flash("An OTP has been sent to your email. Please enter it to complete your registration.")
        return redirect(url_for('verify_otp'))
    
    return render_template("authentication/signup.html", form=form, email=email,
        title_tag="Biitech Academy Create Account | Join Our Platform",
        meta_description="Sign up for an account at Biitech Academy and start your learning journey today. Receive a confirmation OTP to complete your registration.",
        keywords="create account, sign up, Biitech Academy, user registration, registration form, account creation, confirmation OTP, learning platform"
    )

@app.route('/auth/user/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    form = OTPForm()
    if form.validate_on_submit():
        if session['otp'] == form.otp.data:
            user_data = session.pop('user_data', None)
            if user_data:
                user = Users(
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    middle_name=user_data['middle_name'],
                    email=user_data['email'],
                    contact=user_data['contact'],
                    password_hash=user_data['password_hash']
                )

                db.session.add(user)
                db.session.commit()
                flash("Your account has been created successfully. Please log in.")
                # Assuming mail_sender and admin_update_mail are correctly set up and used for sending emails.
                mail_sender.send_confirmation_email(user_data['email'], user_data['contact'])  # Modify as needed
                admin_update_mail.send_admin_mail(user_data['email'], user_data['contact'])    # Modify as needed
                return redirect(url_for('login'))
            else:
                flash("Session expired. Please try again.")
                return redirect(url_for('add_user'))
        else:
            flash("Invalid OTP. Please try again.")
    
    return render_template("authentication/verify_otp.html",
        title_tag="Biitech Academy Verify OTP | Confirm Your Registration",
        meta_description="Verify the OTP sent to your email to complete your registration at Biitech Academy. Once verified, your account will be successfully created.",
        keywords="verify OTP, Biitech Academy, registration confirmation, confirm account, OTP verification, user registration, account creation, registration process",
        form=form
    )

@app.route('/biitech-academy/auth/delete-users/<int:id>')
@login_required
def delete(id):
    our_users = Users.query.order_by(Users.date_added)
    if id == current_user.id or current_user.id == 1:
        user_to_delete = Users.query.get_or_404(id)
        name = None
        form = UserForm()

        try:
            db.session.delete(user_to_delete)
            db.session.commit()
            if current_user.id == 1:
                return redirect( url_for('admin'))
            else:
                flash("User deleted successfully!!")
                return render_template("authentication/signup.html",
                                       form=form,
                                       name=name,
                                       our_users=our_users)

        except:
            flash("Whoops! There was a problem deleting user, Try Again... ")
            return render_template("authentication/signup.html",
                                   form=form,
                                   name=name,
                                   our_users=our_users)
    else:
        flash("Sorry, you can't delete this User")
        return redirect(url_for('dashboard'))

@app.route('/biitech-academy/auth/admin-secret/update-user-information/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_update(id):
    name_to_update = Users.query.get_or_404(id)
    form = UserForm(obj=name_to_update)

    if request.method == "POST":
        # Validate the form
        if form.validate_on_submit():
            if any("Biitech Academy" in request.form.get(field, "") or "Biitech" in request.form.get(field, "")
                   for field in ['first_name', 'last_name', 'middle_name', 'email']):
                flash("You are not allowed to use 'Biitech Academy' or 'Biitech' in your user information.", "danger")
                return redirect(url_for("admin_update", id=id))
            
            # Update user information
            name_to_update.first_name = request.form['first_name']
            name_to_update.last_name = request.form['last_name']
            name_to_update.middle_name = request.form['middle_name']
            name_to_update.email = request.form['email']
            name_to_update.contact = request.form['contact']
            name_to_update.user_status = request.form['user_status']
            name_to_update.facebook_account = request.form['facebook_account']
            name_to_update.linkedin_account = request.form['linkedin_account']
            
            try:
                db.session.commit()
                flash("User information updated successfully.", "success")
                return redirect(url_for('all_users'))
            except Exception as e:
                db.session.rollback()
                flash("Error updating user information: " + str(e), "danger")
            
            return redirect(url_for("admin_update", id=id))

    return render_template("administrator/update.html", form=form, name_to_update=name_to_update, id=id,
        title_tag="Admin Update User Information | Biitech Academy",
        meta_description="Update user information for Biitech Academy. Admins can modify user details securely and efficiently.",
        keywords="admin update, user information, Biitech Academy, user management, admin dashboard, user details, user modification"
    )

@app.route('/biitech-academy/update-user-information/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    if 'biitech-academy/course-details/' in request.url_rule.rule:
        flash('Complete your registration to enroll for this course!')
    name_to_update = Users.query.get_or_404(id)
    form = UserForm(obj=name_to_update)

    if request.method == "POST":
        if "name" in request.form:
            if "Biitech Academy" in request.form.get('first_name') or "Biitech" in request.form.get('first_name') or \
            "Biitech Academy" in request.form.get('last_name') or "Biitech" in request.form.get('last_name') or \
            "Biitech Academy" in request.form.get('middle_name') or "Biitech" in request.form.get('middle_name') or \
            "Biitech Academy" in request.form.get('email') or "Biitech" in request.form.get('email'):
                flash("You are not allowed to use 'Biitech Academy' or 'Biitech' in your user information.")
                return redirect(url_for("update", id=id))

        name_to_update.first_name = request.form['first_name']
        name_to_update.last_name = request.form['last_name']
        name_to_update.middle_name = request.form['middle_name']
        name_to_update.email = request.form['email']
        name_to_update.contact = request.form['contact']
        name_to_update.facebook_account = request.form['facebook_account']
        name_to_update.linkedin_account = request.form['linkedin_account']

        if request.files.get('profile_pic'):
            # save the image
            pic_filename = secure_filename(request.files['profile_pic'].filename)
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
            saver = request.files['profile_pic']

            try:
                # upload to cloudinary
                upload_result = cloudinary.uploader.upload(saver, folder="biitech-academy-uploads")
                name_to_update.profile_pic = upload_result['public_id']
                db.session.commit()

                # save to local folder
                saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
                flash("User Updated Successfully !")
                return redirect(url_for("dashboard"))
            except Exception as e:
                flash("Error! Looks Like There Was a Problem... Try Again!")
                print(e)
                return redirect(url_for("update", id=id))
        else:
            db.session.commit()
            flash("User Updated Successfully !")
            return redirect(url_for("update", id=id))

    return render_template("forms/update.html", form=form, name_to_update=name_to_update, id=id or 1,
        title_tag="Update User Information | Biitech Academy",
        meta_description="Update your user information at Biitech Academy. Keep your profile up-to-date for a seamless learning experience.",
        keywords="update user information, Biitech Academy, user profile, user details, profile update, user account, edit user information"
    )

@app.route('/biitech-academy/auth/registered-users', methods=['GET', 'POST'])
@login_required
def all_users():
    our_users = Users.query.order_by(Users.date_added.desc()).all()
    return render_template('administrator/users.html',
        our_users=our_users,
        title_tag="Registered Users | Biitech Academy",
        meta_description="View all registered users at Biitech Academy. Admins can manage user accounts and access user details here.",
        keywords="registered users, Biitech Academy, user management, user accounts, admin dashboard, user details, user list",
        url_link="https://www.biitechacademy.com/biitech-academy/becoming-a-tutor",
        revised="20th of February 2024",
    )

@app.route('/biitech-academy/user-dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    events = Events.query.order_by(Events.date_created).limit(3)
    created_courses = Courses.query.order_by(Courses.date_created.desc())
    created_tasks = Tasks.query.order_by(Tasks.date_created.desc()).limit(5)
    return render_template('dashboard/dashboard.html',
        keywords="user dashboard, Biitech Academy, personalized dashboard, events, courses, tasks, learning journey",
        title_tag="User Dashboard | Biitech Academy",
        events=events,
        meta_description="Access your personalized dashboard at Biitech Academy. Stay updated on events, courses, and tasks tailored to your learning journey.",
        created_tasks=created_tasks,
        created_courses=created_courses,
        url_link="https://www.biitechacademy.com/biitech-academy/user-dashboard",
        revised="20th of February 2024",
    )

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You Have Successfully Logged Out! ")
    return redirect(url_for('index'))

@app.route('/files/<path:filename>')
def uploaded_files(filename):
    app = current_app._get_current_object()
    path = (app.config['UPLOAD_FOLDER'])
    return send_from_directory(path, filename)

@app.route('/upload', methods=['POST'])
def upload():
    app = current_app._get_current_object()
    f = request.files.get('upload')

    # Add more validations here
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    saver.save(os.path.join((app.config['UPLOAD_FOLDER']), f.filename))
    url = url_for('main.uploaded_files', filename=f.filename)
    return upload_success(url, filename=f.filename)

@app.route('/biitech-academy/dashboard-courses', methods=['GET', 'POST'])
@login_required
def dashboard_courses():
    created_courses = Courses.query.order_by(Courses.date_created.desc())
    return render_template('dashboard/courses.html',
        created_courses=created_courses,
        title_tag="Dashboard Courses | Biitech Academy",
        meta_description="Explore courses available on your dashboard at Biitech Academy. Choose from a variety of options to enhance your skills and knowledge.",
        keywords="dashboard courses, Biitech Academy, courses, learning, skills, knowledge",
        url_link="https://www.biitechacademy.com/biitech-academy/dashboard-courses",
        revised="20th of February 2024",
    )

@app.route('/biitech-academy/auth/admin-panel', methods=['GET', 'POST'])
@login_required
def admin():
    return render_template('administrator/admin.html',
        title_tag="Admin Panel | Biitech Academy",
        meta_description="Access the admin panel at Biitech Academy. Manage user accounts, courses, and other administrative tasks efficiently.",
        keywords="admin panel, Biitech Academy, administrator, user management, course management, administrative tasks",
        url_link="https://www.biitechacademy.com/biitech-academy/auth/admin-panel",
        revised="20th of February 2024",
    )

@app.route('/biitech-academy/auth/admin-panel/create-course', methods=['GET', 'POST'])
@login_required
def create_course():
    form = CoursesForm()
    if form.validate_on_submit():
        creator_id = current_user.id
        created_course = Courses(
            course_title=form.course_title.data,
            course_description=form.course_description.data,
            course_duration=form.course_duration.data,
            course_lesson=form.course_lesson.data,
            course_video=form.course_video.data,
            courses_instructor=form.courses_instructor.data,
            courses_url=form.courses_url.data,
            courses_schedule=form.courses_schedule.data,
            courses_price=form.courses_price.data,
            user_id=creator_id
        )

        if form.course_img.data:
            created_course.course_img = form.course_img.data
            filename = secure_filename(created_course.course_img.filename)
            file_name = str(uuid.uuid1()) + "_" + filename
            saver = form.course_img.data
            created_course.course_img = file_name

            try:
                upload_result = cloudinary.uploader.upload(
                    saver, folder="biitech-academy-uploads")
                created_course.course_img = upload_result['public_id']
                db.session.add(created_course)
                db.session.commit()
                
                flash("Post Successfully Added !")
                return redirect(url_for("courses"))
            except:
                flash("Error! looks like there was a problem... Try again!")
                return render_template("forms/create-course.html", form=form)
        else:
            db.session.add(created_course)
            db.session.commit()
            flash("Post Successfully Added !")
            return redirect(url_for("courses"))

        form.course_title.data = ''
        form.course_description.data = ''
        form.course_duration.data = ''
        form.course_lesson.data = ''
        form.course_video.data = ''
        form.courses_instructor.data = ''
        form.courses_url.data = ''
        form.courses_schedule.data = ''
        form.courses_price.data = ''
        
    return render_template('forms/create-course.html',
                           form=form,
                           title_tag="Create New Course",
                           meta_description="Create a new course on Biitech Academy",
                           keywords="courses, create, education",
                           url_link="https://www.biitechacademy.com/biitech-academy/auth/admin-panel/create-course",
                           revised="20th of February 2024")

@app.route('/biitech-academy/auth/admin-panel/edit-created-course/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_created_course(id):
    created_course = Courses.query.get_or_404(id)
    form = CoursesForm(obj=created_course)

    if form.validate_on_submit():
        created_course.course_title = form.course_title.data
        created_course.course_description = form.course_description.data
        created_course.course_duration = form.course_duration.data
        created_course.course_lesson = form.course_lesson.data
        created_course.course_video = form.course_video.data
        created_course.courses_instructor = form.courses_instructor.data
        created_course.courses_url = form.courses_url.data
        created_course.courses_schedule = form.courses_schedule.data
        created_course.courses_price = form.courses_price.data
        
        db.session.commit()
        flash("Post Successfully Updated")
        return redirect(url_for('dashboard_courses'))

    else:
        our_user = Users.query.order_by(Users.date_added.desc()).first()
        our_users = Users.query.order_by(Users.date_added.desc()).all()
        created_courses = Courses.query.order_by(Courses.date_created.desc())

        if current_user.id == created_course.user_id or current_user.id == 1:
            return render_template('edit-course.html',
                                   form=form,
                                   our_user=our_user,
                                   our_users=our_users,
                                   created_course=created_course,
                                   created_courses=created_courses)
        else:
            flash("You need Authorization to access this Post")
            return render_template("dashboard.html",
                                   form=form,
                                   our_user=our_user,
                                   our_users=our_users,
                                   created_course=created_course,
                                   created_courses=created_courses)

@app.route('/biitech-academy/auth/admin-panel/delete-course/<int:id>')
@login_required
def delete_course(id):
    course_to_delete = Courses.query.get_or_404(id)
    id = current_user.id
    if id == course_to_delete.user_id or id == 1:
        try:
            db.session.delete(course_to_delete)
            db.session.commit()
            flash("Course Was Deleted Successfully!")
            created_courses = Courses.query.order_by(Courses.date_created)
            return render_template("dashboard-courses.html", created_courses=created_courses)

        except:
            flash("Whoops!!! There was a Problem Deleting Post Try Again...")
            created_courses = Courses.query.order_by(Courses.date_created)
            return render_template("dashboard-courses.html", created_courses=created_courses)
    else:
        flash("You are not authorized to Delete this Post!")
        created_courses = Courses.query.order_by(Courses.date_created.desc())
        return render_template("dashboard-courses.html", created_courses=created_courses)

@app.route('/biitech-academy/auth/admin-panel/create-program', methods=['GET', 'POST'])
@login_required
def create_program():
    return render_template('create-program.html',
        title_tag="Create Program | Admin Panel | Biitech Academy",
        meta_description="Create a new program within the admin panel at Biitech Academy. Customize program details and settings to fit your requirements.",
        keywords="create program, admin panel, Biitech Academy, program management, program creation",
        url_link="https://www.biitechacademy.com/biitech-academy/auth/admin-panel/create-program",
        revised="20th of February 2024",
    )

@app.route('/biitech-academy/auth/admin-panel/create-events', methods=['GET', 'POST'])
@login_required
def create_events():
    form = EventForm()
    if form.validate_on_submit():
        created_event = Events(
            event_name=form.event_name.data,
            event_description=form.event_description.data,
            event_location=form.event_location.data,
            event_url=form.event_url.data,
            event_time=form.event_time.data,
            event_date=form.event_date.data
        )

        db.session.add(created_event)
        db.session.commit()
        flash("You have successfully created an event!")
        return redirect(url_for("dashboard"))

    # Reset form data after submission
    form.event_name.data = ''
    form.event_description.data = ''
    form.event_location.data = ''
    form.event_url.data = ''

    # Fetch latest created courses for display
    created_courses = Courses.query.order_by(Courses.date_created.desc()).limit(5)
    return render_template('forms/create-events.html',
                           form=form,
                           created_courses=created_courses,
                           title_tag="Create Events | Admin Panel | Biitech Academy",
                           meta_description="Organize new events through the admin panel at Biitech Academy. Schedule, describe, and manage events for learners and professionals.",
                           keywords="create events, admin panel, Biitech Academy, event management, event creation",
                           url_link="https://www.biitechacademy.com/biitech-academy/auth/admin-panel/create-program",
                           revised="20th of February 2024")

@app.route('/biitech-academy/auth/admin-panel/create-task', methods=['GET', 'POST'])
@login_required
def create_tasks():
    form = TaskForm()
    created_courses = Courses.query.order_by(Courses.date_created.desc())
    creator_id = current_user.id
    if form.validate_on_submit():
        course_id = request.form.get('course_id')
        created_task = Tasks(
            task_title=form.task_title.data,
            task_priority=form.task_priority.data,
            task_description=form.task_description.data, 
            task_submission_url=form.task_submission_url.data, 
            task_status=form.task_status.data, 
            task_deadline=form.task_deadline.data,
            user_id=creator_id
        )

        db.session.add(created_task)
        db.session.commit()
        flash("You have successfully created a task!")
        return redirect(url_for("dashboard"))

    form.task_title.data = ''
    form.task_priority.data = ''
    form.task_description.data = ''
    form.task_submission_url.data = ''
    form.task_status.data = ''
    form.task_deadline.data = ''

    return render_template('forms/create-task.html',
                           form=form,
                           created_courses=created_courses,
                           title_tag="Create Task | Admin Panel | Biitech Academy",
                           meta_description="Create a new task within the admin panel at Biitech Academy. Assign priorities, deadlines, and descriptions for efficient task management.",
                           keywords="create task, admin panel, Biitech Academy, task management, task creation, priorities, deadlines",
                           url_link="https://www.biitechacademy.com/biitech-academy/auth/admin-panel/create-program",
                           revised="20th of February 2024")
    
@app.route('/biitech-academy/auth/user-course/registration/<int:id>', methods=['GET', 'POST'])
@login_required
def create_registration(id):
    created_course = Courses.query.get_or_404(id)
    registered_user_id = current_user.id
    register_course = CourseRegistration(
        user_id=registered_user_id,
        course_id=created_course.id,
        course_registration_status=True
    )
    db.session.add(register_course)
    db.session.commit()
    flash("You have successfully registered for this course")
    return redirect(url_for('dashboard'))

def payment_processing():
    pass

@app.errorhandler(404)
def page_not_found(e):
    return render_template("components/404.html"), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("components/500.html"), 500

if __name__ == '__main__':
    app.run(debug=True)