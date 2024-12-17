import urllib
import xml.etree.ElementTree as ET

import requests
import webob
import webob.exc
import webob.cookies


class CASMiddleware(object):

    def __init__(self, app, config):
        self._app = app
        self._config = config

    def __call__(self, environ, start_response):
        request = webob.Request(environ)

        if request.path_info == '/cas/logout':
            cas_server = self._config['CAS.server']
            params = urllib.urlencode({'service': request.application_url})
            logout_url = '{}/logout?{}'.format(cas_server, params)
            response = webob.exc.HTTPFound(location=logout_url)
            self._remove_username_cookie(request, response)
            return response(environ, start_response)

        username = None
        if 'ticket' in request.GET:
            username = self._get_username_from_ticket(request)
            if username:
                response = webob.exc.HTTPFound(location=request.path_url)
                self._add_username_to_cookie(request, response, username)
                return response(environ, start_response)

        username = self._get_username_from_cookie(request)
        new_environ = self._add_logout_url_to_environ(environ)
        if username:
            new_environ = self._add_username_to_environ(username, new_environ)

        new_request = webob.Request(new_environ)
        app_response = new_request.get_response(self._app)

        if app_response.status_code == 401:
            params = urllib.urlencode({'service':
                                       self._make_service_url(request)})
            login_url = '{}/login?{}'.format(self._config['CAS.server'],
                                             params)
            response = webob.exc.HTTPFound(location=login_url)
            return response(environ, start_response)
        else:
            return app_response(new_environ, start_response)

    def _add_username_to_environ(self, username, environ):
        new_environ = environ.copy()
        new_environ['REMOTE_USER'] = username
        return new_environ

    def _add_logout_url_to_environ(self, environ):
        new_environ = environ.copy()
        new_environ['CAS.logout-url'] = '/cas/logout'
        return new_environ

    def _get_username_from_ticket(self, request):
        cas_server = self._config['CAS.server']
        validation_url = '{}/serviceValidate'.format(cas_server)
        params = {'service': self._make_service_url(request),
                  'ticket': request.GET['ticket']}
        validation_response = requests.get(validation_url, params=params)
        validation_tree = ET.fromstring(validation_response.text)
        ns = {'cas': 'http://www.yale.edu/tp/cas'}
        success = validation_tree.find('./cas:authenticationSuccess', ns)
        if success is not None:
            return success.find('./cas:user', ns).text

    def _get_cookie(self, request, expired=False):
        cookie_name = self._config.get('CAS.cookie', 'cas-username')
        cookie_secret = self._config.get('CAS.cookie-secret',
                                         'seekrit' + 'x' * 121)
        cookie_salt = self._config.get('CAS.cookie-salt', 'saltie')
        cookie_secure = self._config.get('CAS.cookie-secure', 'true') == 'true'
        if expired:
            cookie_max_age = 0
        else:
            cookie_max_age = self._config.get('CAS.cookie-max-age', 86400)
        cookie_httponly = (
            self._config.get('CAS.cookie-httponly', 'false') == 'true')
        cookie_path = '/'
        cookie_profile = webob.cookies.SignedCookieProfile(
            cookie_secret,
            cookie_salt,
            cookie_name,
            secure=cookie_secure,
            max_age=cookie_max_age,
            httponly=cookie_httponly,
            path=cookie_path
        ).bind(request)
        return cookie_profile

    def _add_username_to_cookie(self, request, response, username):
        cookie = self._get_cookie(request)
        cookie.set_cookies(response, username)

    def _get_username_from_cookie(self, request):
        cookie = self._get_cookie(request)
        return cookie.get_value()

    def _remove_username_cookie(self, request, response):
        cookie = self._get_cookie(request, expired=True)
        cookie.set_cookies(response, None)

    def _make_service_url(self, request):
        url = '{}://'.format(request.environ['wsgi.url_scheme'])

        if request.environ.get('HTTP_HOST'):
            url += request.environ['HTTP_HOST']
        else:
            url += request.environ['SERVER_NAME']
            if request.environ['wsgi.url_scheme'] == 'https':
                if request.environ['SERVER_PORT'] != '443':
                    url += ':' + request.environ['SERVER_PORT']
            else:
                if request.environ['SERVER_PORT'] != '80':
                    url += ':' + request.environ['SERVER_PORT']

        url += urllib.quote(request.environ.get('SCRIPT_NAME', ''))
        return url
