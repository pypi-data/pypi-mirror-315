import mock
from webob import exc

from .. import middleware
from ..middleware import CASMiddleware


SIMPLE_RESPONSE = 'Hello World\b'


def simpleapp(environ, start_response):
    if 'REMOTE_USER' in environ:
        start_response("200 OK", [('Content-type', 'text/plain')])
        return ['Hello {}\n'.format(environ['REMOTE_USER'])]
    else:
        response = exc.HTTPUnauthorized()
        return response(environ, start_response)


class FakeResponse(object):

    @classmethod
    def success(cls, username):
        text = '''<cas:serviceResponse xmlns:cas="http://www.yale.edu/tp/cas">
 <cas:authenticationSuccess>
  <cas:user>{}</cas:user>
  <cas:proxyGrantingTicket>PGTIOU-84678-8a9d...</cas:proxyGrantingTicket>
 </cas:authenticationSuccess>
</cas:serviceResponse>'''.format(username)
        return cls(text)

    @classmethod
    def failure(cls, ticket):
        text = '''<cas:serviceResponse xmlns:cas="http://www.yale.edu/tp/cas">
 <cas:authenticationFailure code="INVALID_TICKET">
    Ticket {} not recognized
  </cas:authenticationFailure>
</cas:serviceResponse>'''.format(ticket)
        return cls(text)

    def __init__(self, contents):
        self.text = contents


class TestCASMiddleware(object):

    def base_config(self):
        return {
            'CAS.server': 'https://cas.com/cas',
        }

    def base_environ(self):
        return {
            'HTTP_HOST': 'localhost',
            'SCRIPT_NAME': '',
            'PATH_INFO': '/',
            'wsgi.url_scheme': 'https',
            'REQUEST_METHOD': 'GET',
        }

    def _run_request(self, app, environ):
        statuses = []
        header_lists = []

        def _start_response(status, headers):
            statuses.append(status)
            header_lists.append(headers)
        response = app(environ, _start_response)
        return {'response': response,
                'status': statuses[0],
                'headers': header_lists[0]}

    def test_unauthenticated_request(self):
        LOGIN_REDIRECT_STATUS = "302 Found"
        LOGIN_REDIRECT_RESPONSE = [
            "302 Found\n\nThe resource was found at"
            " https://cas.com/cas/login?service=https%3A%2F%2Flocalhost;"
            " you should be redirected automatically.  "
        ]
        LOGIN_REDIRECT_HEADERS = [
            ('Location',
             'https://cas.com/cas/login?service=https%3A%2F%2Flocalhost'),
            ('Content-Length', '137'),
            ('Content-Type', 'text/plain; charset=UTF-8'),
        ]

        config = self.base_config()
        app = CASMiddleware(simpleapp, config)
        environ = self.base_environ()
        result = self._run_request(app, environ)
        assert result['response'] == LOGIN_REDIRECT_RESPONSE, result
        assert result['status'] == LOGIN_REDIRECT_STATUS, result
        assert result['headers'] == LOGIN_REDIRECT_HEADERS, result

    def test_logout_request(self):
        LOGOUT_REDIRECT_STATUS = "302 Found"
        LOGOUT_REDIRECT_RESPONSE = [
            "302 Found\n\nThe resource was found at"
            " https://cas.com/cas/logout?service=https%3A%2F%2Flocalhost;"
            " you should be redirected automatically.  "
        ]
        LOGOUT_REDIRECT_HEADERS = [
            ('Set-Cookie',
             'cas-username=; Max-Age=0; Path=/;'
             ' expires=Wed, 31-Dec-97 23:59:59 GMT; secure'),
            ('Location',
             'https://cas.com/cas/logout?service=https%3A%2F%2Flocalhost'),
            ('Content-Length', '138'),
            ('Content-Type', 'text/plain; charset=UTF-8'),
        ]

        config = self.base_config()
        app = CASMiddleware(simpleapp, config)
        environ = self.base_environ()
        environ['PATH_INFO'] = '/cas/logout'
        result = self._run_request(app, environ)
        assert result['response'] == LOGOUT_REDIRECT_RESPONSE, result
        assert result['status'] == LOGOUT_REDIRECT_STATUS, result
        assert result['headers'] == LOGOUT_REDIRECT_HEADERS, result

    def test_logged_in_request_with_ticket(self):
        TICKETED_REDIRECT_STATUS = "302 Found"
        TICKETED_REDIRECT_RESPONSE = [
            "302 Found\n\nThe resource was found at"
            " https://localhost;"
            " you should be redirected automatically.  "
        ]
        TICKETED_REDIRECT_HEADERS = [
            ('Set-Cookie',
             'cas-username=SB5zz_4QOXw8PvwVCaSoQhbpfw0Yko1w-'
             '7H5f1SPwWxJFt9CeKyzsIHMN3F5gzpr8qIVTHhRr1UYRGB'
             'Q5SiXJSJtYWQwNjAxNyI; Max-Age=86400; Path=/;'
             ' expires=Mon, 11-Jan-2016 04:23:22 GMT; secure'),
            ('Location', 'https://localhost'),
            ('Content-Length', '97'),
            ('Content-Type', 'text/plain; charset=UTF-8')
        ]

        config = self.base_config()
        app = CASMiddleware(simpleapp, config)
        environ = self.base_environ()
        environ['PATH_INFO'] = ''
        environ['QUERY_STRING'] = 'ticket=ST-12345678'
        requests = middleware.requests
        with mock.patch.object(requests, 'get') as get:
            get.return_value = FakeResponse.success('mad06017')
            result = self._run_request(app, environ)
        assert result['response'] == TICKETED_REDIRECT_RESPONSE, result
        assert result['status'] == TICKETED_REDIRECT_STATUS, result
        assert result['headers'][0][0] == 'Set-Cookie'
        assert result['headers'][1:] == TICKETED_REDIRECT_HEADERS[1:], result

    def test_logged_in_request_with_invalid_ticket(self):
        LOGIN_REDIRECT_STATUS = "302 Found"
        LOGIN_REDIRECT_RESPONSE = [
            "302 Found\n\nThe resource was found at"
            " https://cas.com/cas/login?service=https%3A%2F%2Flocalhost;"
            " you should be redirected automatically.  "
        ]
        LOGIN_REDIRECT_HEADERS = [
            ('Location',
             'https://cas.com/cas/login?service=https%3A%2F%2Flocalhost'),
            ('Content-Length', '137'),
            ('Content-Type', 'text/plain; charset=UTF-8'),
        ]

        config = self.base_config()
        app = CASMiddleware(simpleapp, config)
        environ = self.base_environ()
        environ['PATH_INFO'] = ''
        environ['QUERY_STRING'] = 'ticket=ST-12345678'
        requests = middleware.requests
        with mock.patch.object(requests, 'get') as get:
            get.return_value = FakeResponse.failure('ST-12345678')
            result = self._run_request(app, environ)
        assert result['response'] == LOGIN_REDIRECT_RESPONSE, result
        assert result['status'] == LOGIN_REDIRECT_STATUS, result
        assert result['headers'] == LOGIN_REDIRECT_HEADERS, result

    def test_authenticated_request_with_cookie(self):
        COOKIE_AUTHENTICATED_STATUS = "200 OK"
        COOKIE_AUTHENTICATED_RESPONSE = ['Hello mad06017\n']
        COOKIE_AUTHENTICATED_HEADERS = [
            ('Content-type', 'text/plain'),
        ]

        config = self.base_config()
        app = CASMiddleware(simpleapp, config)
        environ = self.base_environ()
        environ['HTTP_COOKIE'] = ('cas-username=SB5zz_4QOXw8PvwVCaSoQhbpfw0Yko'
                                  '1w-7H5f1SPwWxJFt9CeKyzsIHMN3F5gzpr8qIVTHhRr'
                                  '1UYRGBQ5SiXJSJtYWQwNjAxNyI; Max-Age=86400;'
                                  ' Path=/; expires=Fri, 15-Jan-2016 03:48:05'
                                  ' GMT; secure')
        result = self._run_request(app, environ)
        assert result['response'] == COOKIE_AUTHENTICATED_RESPONSE, result
        assert result['status'] == COOKIE_AUTHENTICATED_STATUS, result
        assert result['headers'] == COOKIE_AUTHENTICATED_HEADERS, result

    def test_logged_in_request_with_ticket_https_port_223(self):
        TICKETED_REDIRECT_STATUS = "302 Found"
        TICKETED_REDIRECT_RESPONSE = [
            "302 Found\n\nThe resource was found at"
            " https://localhost:223;"
            " you should be redirected automatically.  "
        ]
        TICKETED_REDIRECT_HEADERS = [
            ('Set-Cookie',
             'cas-username=SB5zz_4QOXw8PvwVCaSoQhbpfw0Yko1w-'
             '7H5f1SPwWxJFt9CeKyzsIHMN3F5gzpr8qIVTHhRr1UYRGB'
             'Q5SiXJSJtYWQwNjAxNyI; Max-Age=86400; Path=/;'
             ' expires=Mon, 11-Jan-2016 04:23:22 GMT; secure'),
            ('Location', 'https://localhost:223'),
            ('Content-Length', '101'),
            ('Content-Type', 'text/plain; charset=UTF-8')
        ]

        config = self.base_config()
        app = CASMiddleware(simpleapp, config)
        environ = self.base_environ()
        del environ['HTTP_HOST']
        environ['SERVER_NAME'] = 'localhost'
        environ['SERVER_PORT'] = '223'
        environ['PATH_INFO'] = ''
        environ['QUERY_STRING'] = 'ticket=ST-12345678'
        requests = middleware.requests
        with mock.patch.object(requests, 'get') as get:
            get.return_value = FakeResponse.success('mad06017')
            result = self._run_request(app, environ)
        assert result['response'] == TICKETED_REDIRECT_RESPONSE, result
        assert result['status'] == TICKETED_REDIRECT_STATUS, result
        assert result['headers'][0][0] == 'Set-Cookie'
        assert result['headers'][1:] == TICKETED_REDIRECT_HEADERS[1:], result

    def test_logged_in_request_with_ticket_http_port_80(self):
        TICKETED_REDIRECT_STATUS = "302 Found"
        TICKETED_REDIRECT_RESPONSE = [
            "302 Found\n\nThe resource was found at"
            " http://localhost:80;"
            " you should be redirected automatically.  "
        ]
        TICKETED_REDIRECT_HEADERS = [
            ('Set-Cookie',
             'cas-username=SB5zz_4QOXw8PvwVCaSoQhbpfw0Yko1w-'
             '7H5f1SPwWxJFt9CeKyzsIHMN3F5gzpr8qIVTHhRr1UYRGB'
             'Q5SiXJSJtYWQwNjAxNyI; Max-Age=86400; Path=/;'
             ' expires=Mon, 11-Jan-2016 04:23:22 GMT; secure'),
            ('Location', 'http://localhost:80'),
            ('Content-Length', '99'),
            ('Content-Type', 'text/plain; charset=UTF-8')
        ]

        config = self.base_config()
        app = CASMiddleware(simpleapp, config)
        environ = self.base_environ()
        del environ['HTTP_HOST']
        environ['wsgi.url_scheme'] = 'http'
        environ['SERVER_NAME'] = 'localhost'
        environ['SERVER_PORT'] = '80'
        environ['PATH_INFO'] = ''
        environ['QUERY_STRING'] = 'ticket=ST-12345678'
        requests = middleware.requests
        with mock.patch.object(requests, 'get') as get:
            get.return_value = FakeResponse.success('mad06017')
            result = self._run_request(app, environ)
        assert result['response'] == TICKETED_REDIRECT_RESPONSE, result
        assert result['status'] == TICKETED_REDIRECT_STATUS, result
        assert result['headers'][0][0] == 'Set-Cookie'
        assert result['headers'][1:] == TICKETED_REDIRECT_HEADERS[1:], result

    def test_logged_in_request_with_ticket_http_port_223(self):
        TICKETED_REDIRECT_STATUS = "302 Found"
        TICKETED_REDIRECT_RESPONSE = [
            "302 Found\n\nThe resource was found at"
            " http://localhost:223;"
            " you should be redirected automatically.  "
        ]
        TICKETED_REDIRECT_HEADERS = [
            ('Set-Cookie',
             'cas-username=SB5zz_4QOXw8PvwVCaSoQhbpfw0Yko1w-'
             '7H5f1SPwWxJFt9CeKyzsIHMN3F5gzpr8qIVTHhRr1UYRGB'
             'Q5SiXJSJtYWQwNjAxNyI; Max-Age=86400; Path=/;'
             ' expires=Mon, 11-Jan-2016 04:23:22 GMT; secure'),
            ('Location', 'http://localhost:223'),
            ('Content-Length', '100'),
            ('Content-Type', 'text/plain; charset=UTF-8')
        ]

        config = self.base_config()
        app = CASMiddleware(simpleapp, config)
        environ = self.base_environ()
        del environ['HTTP_HOST']
        environ['wsgi.url_scheme'] = 'http'
        environ['SERVER_NAME'] = 'localhost'
        environ['SERVER_PORT'] = '223'
        environ['PATH_INFO'] = ''
        environ['QUERY_STRING'] = 'ticket=ST-12345678'
        requests = middleware.requests
        with mock.patch.object(requests, 'get') as get:
            get.return_value = FakeResponse.success('mad06017')
            result = self._run_request(app, environ)
        assert result['response'] == TICKETED_REDIRECT_RESPONSE, result
        assert result['status'] == TICKETED_REDIRECT_STATUS, result
        assert result['headers'][0][0] == 'Set-Cookie'
        assert result['headers'][1:] == TICKETED_REDIRECT_HEADERS[1:], result

    def test_logged_in_request_with_ticket_http_port_80(self):
        TICKETED_REDIRECT_STATUS = "302 Found"
        TICKETED_REDIRECT_RESPONSE = [
            "302 Found\n\nThe resource was found at"
            " http://localhost:223;"
            " you should be redirected automatically.  "
        ]
        TICKETED_REDIRECT_HEADERS = [
            ('Set-Cookie',
             'cas-username=SB5zz_4QOXw8PvwVCaSoQhbpfw0Yko1w-'
             '7H5f1SPwWxJFt9CeKyzsIHMN3F5gzpr8qIVTHhRr1UYRGB'
             'Q5SiXJSJtYWQwNjAxNyI; Max-Age=86400; Path=/;'
             ' expires=Mon, 11-Jan-2016 04:23:22 GMT; secure'),
            ('Location', 'http://localhost:223'),
            ('Content-Length', '100'),
            ('Content-Type', 'text/plain; charset=UTF-8')
        ]

        config = self.base_config()
        app = CASMiddleware(simpleapp, config)
        environ = self.base_environ()
        del environ['HTTP_HOST']
        environ['wsgi.url_scheme'] = 'http'
        environ['SERVER_NAME'] = 'localhost'
        environ['SERVER_PORT'] = '223'
        environ['PATH_INFO'] = ''
        environ['QUERY_STRING'] = 'ticket=ST-12345678'
        requests = middleware.requests
        with mock.patch.object(requests, 'get') as get:
            get.return_value = FakeResponse.success('mad06017')
            result = self._run_request(app, environ)
        assert result['response'] == TICKETED_REDIRECT_RESPONSE, result
        assert result['status'] == TICKETED_REDIRECT_STATUS, result
        assert result['headers'][0][0] == 'Set-Cookie'
        assert result['headers'][1:] == TICKETED_REDIRECT_HEADERS[1:], result

    def test_unauthenticated_request_https_port_223(self):
        LOGIN_REDIRECT_STATUS = "302 Found"
        LOGIN_REDIRECT_RESPONSE = [
            "302 Found\n\nThe resource was found at"
            " https://cas.com/cas/login?service=https%3A%2F%2Flocalhost%3A223;"
            " you should be redirected automatically.  "
        ]
        LOGIN_REDIRECT_HEADERS = [
            ('Location',
             'https://cas.com/cas/login?service=https%3A%2F%2Flocalhost%3A223'),
            ('Content-Length', '143'),
            ('Content-Type', 'text/plain; charset=UTF-8'),
        ]

        config = self.base_config()
        app = CASMiddleware(simpleapp, config)
        environ = self.base_environ()
        del environ['HTTP_HOST']
        environ['SERVER_NAME'] = 'localhost'
        environ['SERVER_PORT'] = '223'
        result = self._run_request(app, environ)
        assert result['response'] == LOGIN_REDIRECT_RESPONSE, result
        assert result['status'] == LOGIN_REDIRECT_STATUS, result
        assert result['headers'] == LOGIN_REDIRECT_HEADERS, result

    def test_unauthenticated_request_https_port_443(self):
        LOGIN_REDIRECT_STATUS = "302 Found"
        LOGIN_REDIRECT_RESPONSE = [
            "302 Found\n\nThe resource was found at"
            " https://cas.com/cas/login?service=https%3A%2F%2Flocalhost;"
            " you should be redirected automatically.  "
        ]
        LOGIN_REDIRECT_HEADERS = [
            ('Location',
             'https://cas.com/cas/login?service=https%3A%2F%2Flocalhost'),
            ('Content-Length', '137'),
            ('Content-Type', 'text/plain; charset=UTF-8'),
        ]

        config = self.base_config()
        app = CASMiddleware(simpleapp, config)
        environ = self.base_environ()
        del environ['HTTP_HOST']
        environ['SERVER_NAME'] = 'localhost'
        environ['SERVER_PORT'] = '443'
        result = self._run_request(app, environ)
        assert result['response'] == LOGIN_REDIRECT_RESPONSE, result
        assert result['status'] == LOGIN_REDIRECT_STATUS, result
        assert result['headers'] == LOGIN_REDIRECT_HEADERS, result

    def test_unauthenticated_request_http_port_223(self):
        LOGIN_REDIRECT_STATUS = "302 Found"
        LOGIN_REDIRECT_RESPONSE = [
            "302 Found\n\nThe resource was found at"
            " https://cas.com/cas/login?service=http%3A%2F%2Flocalhost%3A223;"
            " you should be redirected automatically.  "
        ]
        LOGIN_REDIRECT_HEADERS = [
            ('Location',
             'https://cas.com/cas/login?service=http%3A%2F%2Flocalhost%3A223'),
            ('Content-Length', '142'),
            ('Content-Type', 'text/plain; charset=UTF-8'),
        ]

        config = self.base_config()
        app = CASMiddleware(simpleapp, config)
        environ = self.base_environ()
        del environ['HTTP_HOST']
        environ['wsgi.url_scheme'] = 'http'
        environ['SERVER_NAME'] = 'localhost'
        environ['SERVER_PORT'] = '223'
        result = self._run_request(app, environ)
        assert result['response'] == LOGIN_REDIRECT_RESPONSE, result
        assert result['status'] == LOGIN_REDIRECT_STATUS, result
        assert result['headers'] == LOGIN_REDIRECT_HEADERS, result

    def test_unauthenticated_request_http_port_80(self):
        LOGIN_REDIRECT_STATUS = "302 Found"
        LOGIN_REDIRECT_RESPONSE = [
            "302 Found\n\nThe resource was found at"
            " https://cas.com/cas/login?service=http%3A%2F%2Flocalhost;"
            " you should be redirected automatically.  "
        ]
        LOGIN_REDIRECT_HEADERS = [
            ('Location',
             'https://cas.com/cas/login?service=http%3A%2F%2Flocalhost'),
            ('Content-Length', '136'),
            ('Content-Type', 'text/plain; charset=UTF-8'),
        ]

        config = self.base_config()
        app = CASMiddleware(simpleapp, config)
        environ = self.base_environ()
        del environ['HTTP_HOST']
        environ['wsgi.url_scheme'] = 'http'
        environ['SERVER_NAME'] = 'localhost'
        environ['SERVER_PORT'] = '80'
        result = self._run_request(app, environ)
        assert result['response'] == LOGIN_REDIRECT_RESPONSE, result
        assert result['status'] == LOGIN_REDIRECT_STATUS, result
        assert result['headers'] == LOGIN_REDIRECT_HEADERS, result

    def test_unauthenticated_request_httponly(self):
        LOGIN_REDIRECT_STATUS = "302 Found"
        LOGIN_REDIRECT_RESPONSE = [
            "302 Found\n\nThe resource was found at"
            " https://cas.com/cas/login?service=https%3A%2F%2Flocalhost;"
            " you should be redirected automatically.  "
        ]
        LOGIN_REDIRECT_HEADERS = [
            ('Location',
             'https://cas.com/cas/login?service=https%3A%2F%2Flocalhost'),
            ('Content-Length', '137'),
            ('Content-Type', 'text/plain; charset=UTF-8'),
        ]

        config = self.base_config()
        config['CAS.cookie-httponly'] = 'true'
        app = CASMiddleware(simpleapp, config)
        environ = self.base_environ()
        result = self._run_request(app, environ)
        assert result['response'] == LOGIN_REDIRECT_RESPONSE, result
        assert result['status'] == LOGIN_REDIRECT_STATUS, result
        assert result['headers'] == LOGIN_REDIRECT_HEADERS, result

    def test_unauthenticated_request_cookie_secure(self):
        LOGIN_REDIRECT_STATUS = "302 Found"
        LOGIN_REDIRECT_RESPONSE = [
            "302 Found\n\nThe resource was found at"
            " https://cas.com/cas/login?service=https%3A%2F%2Flocalhost;"
            " you should be redirected automatically.  "
        ]
        LOGIN_REDIRECT_HEADERS = [
            ('Location',
             'https://cas.com/cas/login?service=https%3A%2F%2Flocalhost'),
            ('Content-Length', '137'),
            ('Content-Type', 'text/plain; charset=UTF-8'),
        ]

        config = self.base_config()
        config['CAS.cookie-secure'] = 'false'
        app = CASMiddleware(simpleapp, config)
        environ = self.base_environ()
        result = self._run_request(app, environ)
        assert result['response'] == LOGIN_REDIRECT_RESPONSE, result
        assert result['status'] == LOGIN_REDIRECT_STATUS, result
        assert result['headers'] == LOGIN_REDIRECT_HEADERS, result
