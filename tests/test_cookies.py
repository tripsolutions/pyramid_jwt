import uuid

import pytest

from pyramid.interfaces import IAuthenticationPolicy
from webob import Request
from zope.interface.verify import verifyObject

from pyramid_jwt.policy import JWTCookieAuthenticationPolicy


@pytest.fixture(scope="module")
def principal():
    return str(uuid.uuid4())


def test_interface():
    verifyObject(IAuthenticationPolicy, JWTCookieAuthenticationPolicy("secret"))


def test_cookie(principal):
    dummy_request = Request.blank("/")
    policy = JWTCookieAuthenticationPolicy("secret")
    token = policy.create_token(principal)
    cookie = policy.remember(dummy_request, token).pop()

    assert len(cookie) == 2

    header, cookie = cookie
    assert header == "Set-Cookie"
    assert len(cookie) > 0


def test_cookie_name(principal):
    dummy_request = Request.blank("/")
    policy = JWTCookieAuthenticationPolicy("secret", cookie_name="auth")
    token = policy.create_token(principal)
    _, cookie = policy.remember(dummy_request, token).pop()

    name, value = cookie.split("=", 1)
    assert name == "auth"


def test_secure_cookie():
    policy = JWTCookieAuthenticationPolicy("secret", https_only=True)
    dummy_request = Request.blank("/")
    token = policy.create_token(str(uuid.uuid4()))
    _, cookie = policy.remember(dummy_request, token).pop()

    assert "; secure;" in cookie
    assert "; HttpOnly" in cookie


def test_insecure_cookie(principal):
    dummy_request = Request.blank("/")
    policy = JWTCookieAuthenticationPolicy("secret", https_only=False)
    token = policy.create_token(principal)
    _, cookie = policy.remember(dummy_request, token).pop()

    assert "; secure;" not in cookie
    assert "; HttpOnly" in cookie


def test_cookie_decode(principal):
    dummy_request = Request.blank("/")
    policy = JWTCookieAuthenticationPolicy("secret", https_only=False)

    token = policy.create_token(principal)
    header, cookie = policy.remember(dummy_request, token).pop()
    name, value = cookie.split("=", 1)

    value, _ = value.split(";", 1)
    dummy_request.cookies = {name: value}

    claims = policy.get_claims(dummy_request)
    assert claims["sub"] == principal


def test_invalid_cookie_reissue(principal):
    dummy_request = Request.blank("/")
    policy = JWTCookieAuthenticationPolicy("secret", https_only=False, reissue_time=10)

    token = "invalid value"
    header, cookie = policy.remember(dummy_request, token).pop()
    name, value = cookie.split("=", 1)

    value, _ = value.split(";", 1)
    dummy_request.cookies = {name: value}

    claims = policy.get_claims(dummy_request)
    assert not claims


def test_cookie_max_age(principal):
    dummy_request = Request.blank("/")
    policy = JWTCookieAuthenticationPolicy("secret", cookie_name="auth", expiration=100)
    _, cookie = policy.remember(dummy_request, principal).pop()
    _, value = cookie.split("=", 1)

    _, meta = value.split(";", 1)
    assert "Max-Age=100" in meta
    assert "expires" in meta


@pytest.mark.freeze_time
def test_expired_token(principal, freezer):
    dummy_request = Request.blank("/")
    policy = JWTCookieAuthenticationPolicy("secret", cookie_name="auth", expiration=1)
    token = policy.create_token(principal)
    _, cookie = policy.remember(dummy_request, token).pop()
    name, value = cookie.split("=", 1)

    freezer.tick(delta=2)

    value, _ = value.split(";", 1)
    dummy_request.cookies = {name: value}
    claims = policy.get_claims(dummy_request)

    assert claims == {}
