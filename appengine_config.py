from gaesessions import SessionMiddleware
import endpoints

# Make webapp.template use django 1.2
webapp_django_version = '1.2'

def webapp_add_wsgi_middleware(app):
    app = SessionMiddleware(app, no_datastore=True, cookie_key=endpoints.COOKIE_KEY)
    return app