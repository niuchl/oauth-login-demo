from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch
from django.utils import simplejson as json
from gaesessions import get_current_session

import logging
import endpoints
import os
import urllib

def get_params():
    return {
              'scope':endpoints.SCOPE,
              'state':'/profile',
              'redirect_uri': endpoints.REDIRECT_URI,
              'response_type':'token',
              'client_id':endpoints.CLIENT_ID
            }
                        
def get_target_url():
    params = get_params()
    return endpoints.AUTH_ENDPOINT + '?' + urllib.urlencode(params)

def validate_access_token(access_token):    
        # check the token audience using exact match (TOKENINFO)
        url = endpoints.TOKENINFO_ENDPOINT + '?access_token=' + access_token
    
        tokeninfo = json.loads(urlfetch.fetch(url).content)
        
        if('error' in tokeninfo) or (tokeninfo['audience'] != endpoints.CLIENT_ID):
            logging.warn('invalid access token = %s' % access_token)
            return False
        else:
            return True

class LogoutHandler(webapp.RequestHandler):
    def get(self):      
        session = get_current_session()
        session.terminate()
        
        #need to clean this up...
        logouturl = 'https://accounts.google.com/o/oauth2/auth?scope=https://www.googleapis.com/auth/userinfo.email+https://www.googleapis.com/auth/userinfo.profile&state=/profile&redirect_uri=http://localhost:8092/oauthcallback&response_type=token&client_id=812741506391.apps.googleusercontent.com'
        logoutparams = {'continue': logouturl}
        
        logging.info("encoded params == %s" % urllib.urlencode(logoutparams))
        
        self.redirect('https://accounts.google.com/logout?service=lso&%s' % urllib.urlencode(logoutparams))

class CallbackHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write(template.render('templates/scripthandler.html', {}))
        
class CatchTokenHandler(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        a_t = self.request.get('access_token')
        
        if not validate_access_token(a_t):
            self.error(400)
        
        session.regenerate_id()
        session['access_token'] = a_t

class CodeHandler(webapp.RequestHandler):
    def get(self):
        a_c = self.request.get('code')
        logging.warn("Code: %s" % a_c)
        payload = {
            'code':a_c,
            'client_id':endpoints.CLIENT_ID,
            'client_secret':endpoints.CLIENT_SECRET,
            'redirect_uri': endpoints.CODE_REDIRECT_URI,
            'grant_type':'authorization_code'
        }
        
        encoded_payload = urllib.urlencode(payload)
        ac_result = json.loads(urlfetch.fetch(url=endpoints.CODE_ENDPOINT,
                                              payload=encoded_payload,
                                              method=urlfetch.POST).content)
                                              
        a_t = ac_result['access_token']
        if not validate_access_token(a_t):
            self.error(400)
        
        session = get_current_session()
        session.regenerate_id()
        session['access_token'] = a_t
        
        self.redirect('/profile')
            
        
class ProfileHandler(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        template_info = {'target_url' : get_target_url()}
        
        if ('access_token' in session):
            # we need to validate the access_token (long-lived sessions, token might have timed out)
            if(validate_access_token(session['access_token'])):            
                # get the user profile information (USERINFO)
                userinfo = json.loads(urlfetch.fetch(endpoints.USERINFO_ENDPOINT,
                                                    headers={'Authorization': 'Bearer ' + session['access_token']}).content)
                
                template_info = {
                                  'target_url' : get_target_url(),
                                  'userinfo' : userinfo
                                }
        
        self.response.out.write(template.render('templates/profileview.html', template_info))