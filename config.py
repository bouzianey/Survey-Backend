import os

# Set environment variables
username = os.environ['EMAIL_USER']
password = os.environ['EMAIL_PASS']

# administrator list
ADMINS = [os.environ['EMAIL_USER']]

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 587,
    "MAIL_USE_TLS": True,
    "MAIL_USE_SSL": False,
    "MAIL_USERNAME": username,
    "MAIL_PASSWORD": password
}

POSTS_PER_PAGE = 6
