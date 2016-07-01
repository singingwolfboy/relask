import jwt
import time
from flask import current_app
from flask.sessions import SessionInterface, SessionMixin

JWT_HEADER_NAME = 'Authorization'
JWT_SCHEMA = 'Bearer'
JWT_DEFAULT_ALGORITHM = 'HS256'
HEADER_SET_BEARER = 'X-Set-Bearer'


class JWTSession(dict, SessionMixin):
    @property
    def expired(self):
        # noinspection PyTypeChecker
        return self.get('expire_at', 0) < time.time()

    @classmethod
    def load(cls, token):
        config = current_app.config
        # noinspection PyCallingNonCallable
        return cls(jwt.decode(
            token,
            key=config.get('JWT_SECRET', config['SECRET_KEY']),
            verify=config.get('JWT_VERIFY', True),
            algorithms=config.get('JWT_ALGORITHMS', None),
            options=config.get('JWT_OPTIONS', None),
        ))

    def dump(self, json_encoder=None):
        config = current_app.config
        # noinspection PyTypeChecker
        self['expire_at'] = (
            time.time() +
            current_app.permanent_session_lifetime.total_seconds())
        return jwt.encode(
            self,
            key=config.get('JWT_SECRET', config['SECRET_KEY']),
            algorithm=config.get('JWT_ALGORITHMS', [JWT_DEFAULT_ALGORITHM])[0],
            json_encoder=json_encoder,
        )


class JWTSessionInterface(SessionInterface):
    json_encoder = None
    header_name = JWT_HEADER_NAME
    schema = JWT_SCHEMA
    header_set_bearer = HEADER_SET_BEARER

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.session_interface = self
        self.header_name = app.config.get('JWT_HEADER_NAME', self.header_name)
        self.schema = app.config.get('JWT_SCHEMA', self.schema)

    def open_session(self, app, request):
        header_value = request.headers.get(self.header_name, '')
        if header_value.startswith(self.schema + ' '):
            session = JWTSession.load(header_value[len(self.schema) + 1:])
            if not session.expired:
                return session
        return JWTSession()

    def save_session(self, app, session, response):
        response.headers[self.header_set_bearer] = session.dump(
            json_encoder=self.json_encoder) if session else ''
