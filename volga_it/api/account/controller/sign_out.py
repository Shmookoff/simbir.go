from ..models import AccessToken
from ..schemas import AccessTokenPayload


def sign_out(access_token: AccessTokenPayload):
    AccessToken.destroy(int(access_token.jti))
