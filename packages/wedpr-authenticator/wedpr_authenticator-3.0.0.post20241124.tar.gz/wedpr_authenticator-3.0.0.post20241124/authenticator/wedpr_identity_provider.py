"""
A JupyterHub authenticator class for use with WeDPR as an identity provider.
"""
from jupyter_server.auth.identity import IdentityProvider
from jupyter_server.auth.identity import User
import jwt
from .wedpr_token_content import WeDPRTokenContent
from tornado import web
from traitlets import Unicode, default
import psutil
import os


class WeDPRIdentityProvider(IdentityProvider):
    """Authenticate local UNIX users with WeDPR-Auth"""
    AUTH_TOKEN_FIELD = "Authorization"
    AUTH_ALGORITHMS = ["HS256", "HS512", "HS384"]

    auth_secret = Unicode("<generated>",
                          help="auth_secret").tag(config=True)

    CURRENT_USER = psutil.Process().username()

    @default("auth_secret")
    def _auth_secret_default(self):
        if os.getenv("JUPYTER_AUTH_SECRET"):
            return os.getenv("JUPYTER_AUTH_SECRET")
        return None

    def _get_token_from_header(self, handler: web.RequestHandler):
        try:
            token = handler.request.headers.get(
                WeDPRIdentityProvider.AUTH_TOKEN_FIELD, "")
            self.log.info(f"#### _get_token_from_header: {token}")
        except KeyError as e:
            token = None
        return token

    def _get_token_from_cookie(self, handler: web.RequestHandler):
        try:
            token = handler.get_secure_cookie(
                WeDPRIdentityProvider.AUTH_TOKEN_FIELD)
        except KeyError as e:
            token = None
        return token

    def _get_token_from_param(self, handler: web.RequestHandler):
        token = None
        try:
            token = handler.get_query_argument(
                WeDPRIdentityProvider.AUTH_TOKEN_FIELD)
            self.log.info(f"#### _get_token_from_param: {token}")
        except Exception as e:
            token = None
        return token

    def _get_token(self, handler: web.RequestHandler):
        token = self._get_token_from_param(handler)
        if token is None:
            token = self._get_token_from_cookie(handler)
        if token is None:
            return self._get_token_from_header(handler)
        return token

    def set_user_cookie(self, handler: web.RequestHandler, token) -> None:
        """Call this on handlers to set the login cookie for success"""
        cookie_options = {}
        cookie_options.update(self.cookie_options)
        cookie_options.setdefault("httponly", True)
        # tornado <4.2 has a bug that considers secure==True as soon as
        # 'secure' kwarg is passed to set_secure_cookie
        secure_cookie = self.secure_cookie
        if secure_cookie is None:
            secure_cookie = handler.request.protocol == "https"
        if secure_cookie:
            cookie_options.setdefault("secure", True)
        # type:ignore[attr-defined]
        cookie_options.setdefault("path", handler.base_url)
        cookie_name = self.get_cookie_name(handler)
        handler.set_secure_cookie(
            WeDPRIdentityProvider.AUTH_TOKEN_FIELD, token, **cookie_options)

    def get_user(self, handler: web.RequestHandler):
        """Authenticate with jwt token, and return the username if login is successful.
        Return None otherwise.
        """
        token = self._get_token(handler)
        if token is None:
            self.log.warning(
                f"WeDPR auth failed for no authorization information defined in the header and cookie! error: {e}")
            return None
        try:
            token_payload = jwt.decode(
                token, self.auth_secret, WeDPRIdentityProvider.AUTH_ALGORITHMS)
            user_info = WeDPRTokenContent.deserialize(token_payload)
        except Exception as e:
            self.log.warning(
                f"WeDPR auth failed for jwt verify failed! error: {e}")
            return None
        if user_info is None:
            return None
        user_name = user_info.get_user_information().username
        if user_name != WeDPRIdentityProvider.CURRENT_USER:
            self.log.warning(
                f"WeDPR auth failed for invalid user, admitted-user: {WeDPRIdentityProvider.CURRENT_USER}, tried user: {user_name}")
            return None
        self.log.info(f"WeDPR auth success, username: {user_name}")
        user = User(username=user_name)
        self.set_user_cookie(handler, token)
        return user
