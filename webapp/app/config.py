from private.keys import FLASK_MAIL_PASSWORD, FLASK_MAIL_USER

MAIL_SERVER = 'mail.eprojecttrackers.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = FLASK_MAIL_USER
MAIL_PASSWORD = FLASK_MAIL_PASSWORD
MAIL_DEFAULT_SENDER = ('eportal mail service', 'eri_portal@eprojecttrackers.com')
MAIL_MAX_EMAILS = None
MAIL_ASCII_ATTACHMENTS = False
ADMINS = ['phanveehuen@gmail.com']
MAIL_DEBUG = True
MAIL_SUPPRESS_SEND = False
