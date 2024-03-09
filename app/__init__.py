# __init__.py

from flask import Flask
from flask_mail import Mail

#Initialize a flask application 
app = Flask(__name__, template_folder='templates')

#Above we have created Flask application object named app







# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# use smtp's server address for sending mails (In this case we are using gmail's SMTP server)


app.config['MAIL_PORT'] = 587
# Port 587 is commonly used for secure SMTP submission

app.config['MAIL_USE_TLS'] = True
# Enable Transport Layer Security (TLS) for secure connection with SMTP server


app.config['MAIL_USERNAME'] = 'developernachiket@gmail.com'
# This email address is used for authentication when connecting to SMTP server

app.config['MAIL_PASSWORD'] = 'rssqpznwvusseaxr'



app.config['MAIL_DEFAULT_SENDER'] = 'user@bloodbank.com'
# Default sender for email address


mail = Mail(app)
# Initialize mail extension with flask app



from app import routes
# Import the routes module from app package 
# Assumes you have file named routes.py in same directory where there is application script (in app.py)

