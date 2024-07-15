from flask import request, abort, jsonify
from functools import wraps
from jose import jwt
from urllib.request import urlopen
import json
import os

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
API_AUDIENCE = os.getenv("AUTH0_AUDIENCE")
ALGORITHMS = ['RS256']

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header"""
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                         "description": "Authorization header is expected."}, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({"code": "invalid_header",
                         "description": "Authorization header must start with Bearer."}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                         "description": "Token not found."}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                         "description": "Authorization header must be Bearer token."}, 401)

    token = parts[1]
    return token

def check_permissions(permission, payload):
    """Checks if the requested permission is in the payload permissions array"""
    if 'permissions' not in payload:
        raise AuthError({"code": "invalid_claims",
                         "description": "Permissions not included in JWT."}, 400)

    if permission not in payload['permissions']:
        raise AuthError({"code": "unauthorized",
                         "description": "Permission not found."}, 403)
    return True

def verify_decode_jwt(token):
    """Verifies the JWT token using Auth0's public keys"""
    jsonurl = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({"code": "invalid_header",
                         "description": "Authorization malformed."}, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f"https://{AUTH0_DOMAIN}/"
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError({"code": "token_expired",
                             "description": "Token expired."}, 401)
        except jwt.JWTClaimsError:
            raise AuthError({"code": "invalid_claims",
                             "description": "Incorrect claims. Please, check the audience and issuer."}, 401)
        except Exception:
            raise AuthError({"code": "invalid_header",
                             "description": "Unable to parse authentication token."}, 400)
    raise AuthError({"code": "invalid_header",
                     "description": "Unable to find the appropriate key."}, 400)

def requires_auth(permission=''):
    """Decorator method for requiring auth on endpoints"""
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                token = get_token_auth_header()
                payload = verify_decode_jwt(token)
                check_permissions(permission, payload)
            except AuthError as e:
                abort(e.status_code, e.error['description'])
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator
