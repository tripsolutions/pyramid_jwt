from .policy import (
    JWTAuthenticationPolicy,
    JWTCookieAuthenticationPolicy,
    json_encoder_factory,
)


def includeme(config):
    json_encoder_factory.registry = config.registry
    config.add_directive(
        "set_jwt_authentication_policy",
        set_jwt_authentication_policy,
        action_wrap=True,
    )
    config.add_directive(
        "set_jwt_cookie_authentication_policy",
        set_jwt_cookie_authentication_policy,
        action_wrap=True,
    )


def create_jwt_authentication_policy(
    config,
    private_key=None,
    public_key=None,
    algorithm=None,
    expiration=None,
    leeway=None,
    http_header=None,
    auth_type=None,
    callback=None,
    json_encoder=None,
    audience=None,
):
    settings = config.get_settings()
    private_key = private_key or settings.get("jwt.private_key")
    audience = audience or settings.get("jwt.audience")
    algorithm = algorithm or settings.get("jwt.algorithm") or "HS512"
    if not algorithm.startswith("HS"):
        public_key = public_key or settings.get("jwt.public_key")
    else:
        public_key = None
    if expiration is None and "jwt.expiration" in settings:
        expiration = int(settings.get("jwt.expiration"))
    leeway = int(settings.get("jwt.leeway", 0)) if leeway is None else leeway
    http_header = http_header or settings.get("jwt.http_header") or "Authorization"
    if http_header.lower() == "authorization":
        auth_type = auth_type or settings.get("jwt.auth_type") or "JWT"
    else:
        auth_type = None
    return JWTAuthenticationPolicy(
        private_key=private_key,
        public_key=public_key,
        algorithm=algorithm,
        leeway=leeway,
        expiration=expiration,
        http_header=http_header,
        auth_type=auth_type,
        callback=callback,
        json_encoder=json_encoder,
        audience=audience,
    )


def create_jwt_cookie_authentication_policy(
    config,
    private_key=None,
    public_key=None,
    algorithm=None,
    expiration=None,
    leeway=None,
    http_header=None,
    auth_type=None,
    callback=None,
    json_encoder=None,
    audience=None,
    cookie_name=None,
    https_only=None,
    samesite=None,
    reissue_time=None,
    cookie_path=None,
    accept_header=None,
    header_first=None,
    reissue_callback=None,
):
    settings = config.get_settings()
    cookie_name = cookie_name or settings.get("jwt.cookie_name")
    cookie_path = cookie_path or settings.get("jwt.cookie_path")
    reissue_time = reissue_time or settings.get("jwt.cookie_reissue_time")
    if https_only is None:
        https_only = settings.get("jwt.https_only_cookie", True)
    if samesite is None:
        samesite = settings.get("jwt.samesite", None)
    if accept_header is None:
        accept_header = settings.get("jwt.cookie_accept_header", False)
    if header_first is None:
        header_first = settings.get("jwt.cookie_prefer_header", False)

    auth_policy = create_jwt_authentication_policy(
        config,
        private_key,
        public_key,
        algorithm,
        expiration,
        leeway,
        http_header,
        auth_type,
        callback,
        json_encoder,
        audience,
    )

    return JWTCookieAuthenticationPolicy.make_from(
        auth_policy,
        cookie_name=cookie_name,
        https_only=https_only,
        samesite=samesite,
        reissue_time=reissue_time,
        cookie_path=cookie_path,
        accept_header=accept_header,
        header_first=header_first,
        reissue_callback=reissue_callback,
    )


def configure_jwt_authentication_policy(config, auth_policy, register=True):
    def _request_create_token(
        request, principal, expiration=None, audience=None, **claims
    ):
        return auth_policy.create_token(principal, expiration, audience, **claims)

    def _request_claims(request):
        return auth_policy.get_claims(request)

    def _request_token(request):
        return auth_policy.get_token(request)

    config.add_request_method(_request_claims, "jwt_claims", reify=True)
    config.add_request_method(_request_token, "jwt_token", reify=True)
    config.add_request_method(_request_create_token, "create_jwt_token")

    if register:
        config.set_authentication_policy(auth_policy)


def set_jwt_cookie_authentication_policy(
    config,
    private_key=None,
    public_key=None,
    algorithm=None,
    expiration=None,
    leeway=None,
    http_header=None,
    auth_type=None,
    callback=None,
    json_encoder=None,
    audience=None,
    cookie_name=None,
    https_only=None,
    samesite=None,
    reissue_time=None,
    cookie_path=None,
    accept_header=None,
    header_first=None,
    reissue_callback=None,
):
    policy = create_jwt_cookie_authentication_policy(
        config,
        private_key,
        public_key,
        algorithm,
        expiration,
        leeway,
        http_header,
        auth_type,
        callback,
        json_encoder,
        audience,
        cookie_name,
        https_only,
        samesite,
        reissue_time,
        cookie_path,
        accept_header,
        header_first,
        reissue_callback,
    )
    configure_jwt_authentication_policy(config, policy)


def set_jwt_authentication_policy(
    config,
    private_key=None,
    public_key=None,
    algorithm=None,
    expiration=None,
    leeway=None,
    http_header=None,
    auth_type=None,
    callback=None,
    json_encoder=None,
    audience=None,
):
    policy = create_jwt_authentication_policy(
        config,
        private_key,
        public_key,
        algorithm,
        expiration,
        leeway,
        http_header,
        auth_type,
        callback,
        json_encoder,
        audience,
    )

    configure_jwt_authentication_policy(config, policy)
