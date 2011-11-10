import os

# Google's OAuth 2.0 endpoints
AUTH_ENDPOINT = "https://accounts.google.com/o/oauth2/auth"
CODE_ENDPOINT = "https://accounts.google.com/o/oauth2/token"
TOKENINFO_ENDPOINT = "https://accounts.google.com/o/oauth2/tokeninfo"
USERINFO_ENDPOINT = 'https://www.googleapis.com/oauth2/v1/userinfo'
SCOPE = "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"
LOGOUT_URI = 'https://accounts.google.com/logout'

# client ID
CLIENT_ID = "812741506391.apps.googleusercontent.com"
CLIENT_SECRET = 'secret'
REDIRECT_URI = 'https://' + os.environ["HTTP_HOST"] + '/oauthcallback'
CODE_REDIRECT_URI = 'https://' + os.environ["HTTP_HOST"] + '/code'
ROOT_URI = 'https://' + os.environ["HTTP_HOST"]