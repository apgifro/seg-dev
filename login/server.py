from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib

import http.cookies
import datetime

import jinja2

from database.database import Database


class Servidor(BaseHTTPRequestHandler):

    db = Database()
    message = ''
    routes = {
        '/': ('index.html', False),
        '/create': ('create.html', False),
        '/login': ('login.html', False),
        '/logout': ('', True),
        '/profile': ('profile.html', True),
        '/404': '404.html'
    }

    def do_GET(self):
        route = self._fetch_routes()
        if route is None:
            return
        page = self._render_page(route)
        self._set_send_html()
        self.wfile.write(bytes(page, "utf8"))

    def _fetch_routes(self):
        try:
            route = Servidor.routes[self.path]
            if self._is_login_required(route[1]):
                status = self._verify_login_session()
                if not status:
                    Servidor.message = 'Você precisa entrar!'
                    return self._redirect_to_login()
                if self.path == '/logout':
                    Servidor.db.close_session(self._get_cookies()['session'].value)
                    self._send_session_cookie(logout=True)
                    Servidor.message = 'Você saiu!'
                    self._redirect_to_login()
                    return
                if self.path == '/profile':
                    email = Servidor.db.get_email(self._get_cookies()['session'].value)
                    Servidor.message = email
            return route[0]
        except KeyError:
            return Servidor.routes['/404']

    def _is_login_required(self, route):
        return route == True

    def _verify_login_session(self):
        cookie = self._get_cookies()
        try:
            session = cookie['session'].value
        except KeyError:
            return False
        status = Servidor.db.is_valid_session(session)

        if status:
            return True
        return False

    def _get_cookies(self):
        return http.cookies.SimpleCookie(self.headers.get('Cookie'))

    def _render_page(self, template):
        loader = jinja2.FileSystemLoader('templates')
        environment = jinja2.Environment(loader=loader)
        page = environment.get_template(template)
        message = page.render(messages=Servidor.message)
        Servidor.message = ''
        return message

    def _set_send_html(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        content = int(self.headers['Content-Length'])
        data = self.rfile.read(content).decode('utf-8')
        fields = urllib.parse.parse_qsl(data)

        try:
            email = fields[0][1]
            password = fields[1][1]
        except IndexError:
            self._set_send_html()
            self.wfile.write(bytes('Digite usuário e senha', "utf8"))
            return

        if self.path == '/create':
            self._create_account(email, password)

        elif self.path == '/login':
            self._login_account(email, password)

    def _create_account(self, email, password):
        if len(email) > 255 or len(password) >= 1024:
            Servidor.message = 'E-mail limitado a 255 caracteres e senha a 1023.'
            self._redirect_to_create()
            return

        status = Servidor.db.create(email, password)

        if status:
            Servidor.message = 'Conta criada com sucesso!'
            self._redirect_to_login()
        else:
            Servidor.message = 'E-mail não disponível.'
            self._redirect_to_create()

    def _login_account(self, email, password):
        if len(email) > 255 or len(password) >= 1024:
            Servidor.message = 'E-mail limitado a 255 caracteres e senha a 1023.'
            self._redirect_to_create()
            return

        status = Servidor.db.login(email, password)

        if status:
            Servidor.message = 'Você entrou com sucesso!'

            self._send_session_cookie(email)
            self._redirect_to_profile()
        else:
            Servidor.message = 'E-mail ou senha incorreto(s).'
            self._redirect_to_login()

    def _send_session_cookie(self, email='', logout=False):
        if logout:
            self.send_response(303)
            cookie = http.cookies.SimpleCookie()
            cookie['session'] = ''
            cookie['session']['samesite'] = "Lax"
            expiration = datetime.datetime.now() - datetime.timedelta(days=1)
            cookie["session"]["expires"] = expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")
            self.send_header("Set-Cookie", cookie.output(header='', sep=''))
        else:
            self.send_response(303)
            session = Servidor.db.create_session(email)
            cookie = http.cookies.SimpleCookie()
            cookie['session'] = session
            cookie['session']['samesite'] = "Lax"
            expiration = datetime.datetime.now() + datetime.timedelta(days=14)
            cookie["session"]["expires"] = expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")
            self.send_header("Set-Cookie", cookie.output(header='', sep=''))

    def _redirect_to_create(self):
        self.send_response(303)
        self.send_header('Location', '/create')
        self.end_headers()

    def _redirect_to_login(self):
        self.send_response(303)
        self.send_header('Location', '/login')
        self.end_headers()

    def _redirect_to_profile(self):
        self.send_response(303)
        self.send_header('Location', '/profile')
        self.end_headers()


def run():
    print('Iniciando servidor...')
    httpd = HTTPServer(('127.0.0.1', 8080), Servidor)
    print('Servidor rodando...')
    httpd.serve_forever()


run()
