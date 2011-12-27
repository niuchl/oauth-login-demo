import os

# Google's OAuth 2.0 endpoints
AUTH_ENDPOINT = "https://accounts.google.com/o/oauth2/auth"
CODE_ENDPOINT = "https://accounts.google.com/o/oauth2/token"
TOKENINFO_ENDPOINT = "https://accounts.google.com/o/oauth2/tokeninfo"
USERINFO_ENDPOINT = 'https://www.googleapis.com/oauth2/v1/userinfo'
SCOPE = "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"
LOGOUT_URI = 'https://accounts.google.com/logout'

# client ID / secret & cookie key
CLIENT_ID = 'updatetoyourclientid'
CLIENT_SECRET = 'updatetoyourclientsecret'
COOKIE_KEY = 'createacookiekey - probably using os.urandom(64)'

is_secure = os.environ.get('HTTPS') == 'on'
protocol = {False: 'http', True: 'https'}[is_secure]

ROOT_URI = protocol +'://' + os.environ["HTTP_HOST"]

RESPONSE_TYPE='token'

if (RESPONSE_TYPE == 'token'):
    REDIRECT_URI = ROOT_URI + '/oauthcallback'
elif (RESPONSE_TYPE == 'code'):
    REDIRECT_URI = ROOT_URI + '/code'
else:
    REDIRECT_URI = ROOT_URI + '/code'

CATCHTOKEN_URI = ROOT_URI + '/catchtoken'    





