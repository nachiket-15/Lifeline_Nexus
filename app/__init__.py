# __init__.py

from flask import Flask
from flask_mail import Mail

app = Flask(__name__, template_folder='templates')

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'developernachiket@gmail.com'
app.config['MAIL_PASSWORD'] = 'rssqpznwvusseaxr'
app.config['MAIL_DEFAULT_SENDER'] = 'user@bloodbank.com'

mail = Mail(app)

from app import routes
