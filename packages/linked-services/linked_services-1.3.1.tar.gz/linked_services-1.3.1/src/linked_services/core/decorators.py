import datetime as dt
import functools
import hashlib
import hmac
import logging
import urllib.parse
import uuid
from datetime import datetime, timedelta
from typing import Any, Callable, Coroutine, Optional, TypedDict

import jwt
from asgiref.sync import sync_to_async
from django.http import HttpRequest
from django.utils import timezone
from rest_framework.views import APIView

from linked_services.core.settings import get_setting
from linked_services.core.utils import AttrDict

from .exceptions import ProgrammingError, ValidationException

__all__ = ["get_handlers", "get_decorators"]

logger = logging.getLogger(__name__)


def get_payload(app, date, signed_headers, request: HttpRequest):
    headers = dict(request.headers)
    headers.pop("Authorization", None)
    payload = {
        "timestamp": date,
        "app": app,
        "method": request.method,
        "params": dict(request.GET),
        "body": request.data if request.data is not None else None,
        "headers": {k: v for k, v in headers.items() if k in signed_headers},
    }

    return payload


def hmac_signature(app, date, signed_headers, request, key, fn):
    payload = get_payload(app, date, signed_headers, request)

    paybytes = urllib.parse.urlencode(payload).encode("utf8")

    return hmac.new(key, paybytes, fn).hexdigest()


TOLERANCE = 2


Info = tuple[Any, str, str, str, bool, list[str], list[str], str, str, str]
Key = tuple[bytes, bytes]

GetUserScopesFn = Callable[[str, int], tuple[list[str], list[str]]]
GetAppKeysFn = Callable[[str], tuple[Info, Key, Optional[Key]]]
GetUserFn = Callable[[int | str | uuid.UUID, int | str | uuid.UUID], Any | None]
AGetUserFn = Callable[[int | str | uuid.UUID, int | str | uuid.UUID], Coroutine[Any | None, None, None]]


class Token(TypedDict):
    sub: Optional[Any]
    iss: str
    app: str
    aud: str
    exp: int
    iat: int
    typ: str


class App(TypedDict):
    id: Any
    private_key: bytes
    public_key: bytes
    algorithm: str
    strategy: str
    schema: str
    require_an_agreement: bool
    webhook_url: str
    redirect_url: str
    app_url: str


LinkSchemaFn = Callable[[HttpRequest, list[str], str, bool], tuple[App, Token]]
SignatureSchemaFn = Callable[[HttpRequest, list[str], str, bool], App]


def get_handlers(get_app_keys: GetAppKeysFn, get_user_scopes: GetUserScopesFn) -> tuple[
    LinkSchemaFn,
    SignatureSchemaFn,
]:

    # required_scopes is really a tuple of n strings
    def link_schema(request: HttpRequest, required_scopes: list[str], authorization: str, use_signature: bool):
        """Authenticate the request and return a two-tuple of (user, token)."""

        try:
            authorization = dict([x.split("=") for x in authorization.split(",")])

        except Exception:
            raise ValidationException("Unauthorized", code=401, slug="authorization-header-malformed")

        if sorted(authorization.keys()) != ["App", "Token"]:
            raise ValidationException("Unauthorized", code=401, slug="authorization-header-bad-schema")

        info, key, legacy_key = get_app_keys(authorization["App"])
        (
            app_id,
            alg,
            strategy,
            schema,
            require_an_agreement,
            required_app_scopes,
            optional_app_scopes,
            webhook_url,
            redirect_url,
            app_url,
        ) = info
        public_key, private_key = key

        if schema != "LINK":
            raise ValidationException("Unauthorized", code=401, slug="authorization-header-forbidden-schema")

        if strategy != "JWT":
            raise ValidationException("Unauthorized", code=401, slug="authorization-header-forbidden-strategy")

        try:
            key = public_key if public_key else private_key
            whoamy = get_setting("app_name")
            payload = jwt.decode(authorization["Token"], key, algorithms=[alg], audience=whoamy)

        except Exception:
            if not legacy_key:
                raise ValidationException("Unauthorized", code=401, slug="wrong-app-token")

        if not payload:
            try:
                legacy_public_key, legacy_private_key = legacy_key

                key = legacy_public_key if legacy_public_key else legacy_private_key
                payload = jwt.decode(authorization["Token"], key, algorithms=[alg])

            except Exception:
                raise ValidationException("Unauthorized", code=401, slug="wrong-legacy-app-token")

        if payload["sub"] and require_an_agreement:
            required_app_scopes, optional_app_scopes = get_user_scopes(authorization["App"], payload["sub"])
            all_scopes = required_app_scopes + optional_app_scopes

            for s in required_scopes:
                if s not in all_scopes:
                    raise ValidationException("Unauthorized", code=401, slug="forbidden-scope")

        if "exp" not in payload or payload["exp"] < timezone.now().timestamp():
            raise ValidationException("Expired token", code=401, slug="expired")

        app = {
            "id": app_id,
            "private_key": private_key,
            "public_key": public_key,
            "algorithm": alg,
            "strategy": strategy,
            "schema": schema,
            "require_an_agreement": require_an_agreement,
            "webhook_url": webhook_url,
            "redirect_url": redirect_url,
            "app_url": app_url,
        }

        payload["sub"] = int(payload["sub"]) if payload["sub"] else None

        return app, payload

    # required_scopes is really a tuple of n strings
    def signature_schema(request: HttpRequest, required_scopes: list[str], authorization: str, use_signature: bool):
        """Authenticate the request and return a two-tuple of (user, token)."""

        try:
            authorization = dict([x.split("=") for x in authorization.split(",")])

        except Exception:
            raise ValidationException("Unauthorized", code=401, slug="authorization-header-malformed")

        if sorted(authorization.keys()) != ["App", "Date", "Nonce", "SignedHeaders"]:
            raise ValidationException("Unauthorized", code=401, slug="authorization-header-bad-schema")

        info, key, legacy_key = get_app_keys(authorization["App"])
        (
            app_id,
            alg,
            strategy,
            schema,
            require_an_agreement,
            required_app_scopes,
            optional_app_scopes,
            webhook_url,
            redirect_url,
            app_url,
        ) = info
        public_key, private_key = key

        if require_an_agreement:
            required_app_scopes, optional_app_scopes = get_user_scopes(authorization["App"])
            all_scopes = required_app_scopes + optional_app_scopes

            for s in required_scopes:
                if s not in all_scopes:
                    raise ValidationException("Unauthorized", code=401, slug="forbidden-scope")

        if schema != "LINK":
            raise ValidationException("Unauthorized", code=401, slug="authorization-header-forbidden-schema")

        if strategy != "SIGNATURE" and not use_signature:
            raise ValidationException("Unauthorized", code=401, slug="authorization-header-forbidden-strategy")

        if alg not in ["HS256", "HS512"]:
            raise ValidationException("Algorithm not implemented", code=401, slug="algorithm-not-implemented")

        fn = hashlib.sha256 if alg == "HS256" else hashlib.sha512

        key = public_key if public_key else private_key
        if (
            hmac_signature(
                authorization["App"], authorization["Date"], authorization["SignedHeaders"], request, key, fn
            )
            != authorization["Nonce"]
            and not legacy_key
        ):
            if not legacy_key:
                raise ValidationException("Unauthorized", code=401, slug="wrong-app-token")

        if legacy_key:
            legacy_public_key, legacy_private_key = legacy_key
            key = legacy_public_key if legacy_public_key else legacy_private_key
            if (
                hmac_signature(
                    authorization["App"], authorization["Date"], authorization["SignedHeaders"], request, key, fn
                )
                != authorization["Nonce"]
            ):
                raise ValidationException("Unauthorized", code=401, slug="wrong-legacy-app-token")

        try:
            date = datetime.fromisoformat(authorization["Date"])
            date = date.replace(tzinfo=dt.timezone.utc)
            now = timezone.now()
            if (now - timedelta(minutes=TOLERANCE) > date) or (now + timedelta(minutes=TOLERANCE) < date):
                raise Exception()

        except Exception:
            raise ValidationException("Unauthorized", code=401, slug="bad-timestamp")

        app = {
            "id": app_id,
            "private_key": private_key,
            "public_key": public_key,
            "algorithm": alg,
            "strategy": strategy,
            "schema": schema,
            "require_an_agreement": require_an_agreement,
            "webhook_url": webhook_url,
            "redirect_url": redirect_url,
            "app_url": app_url,
        }

        return app

    return link_schema, signature_schema


def get_decorators(
    link_schema: LinkSchemaFn, signature_schema: SignatureSchemaFn, get_user: GetUserFn, aget_user: AGetUserFn
) -> tuple[Callable, Callable]:
    def scope(scopes: Optional[list] = None, mode: Optional[str] = None) -> callable:
        """Check if the app has access to the scope provided."""

        if scopes is None:
            scopes = []

        def decorator(function: callable) -> callable:

            @functools.wraps(function)
            def wrapper(*args, **kwargs):
                request: HttpRequest

                if isinstance(scopes, list) is False:
                    raise ProgrammingError("Permission must be a list")

                if len([x for x in scopes if not isinstance(x, str)]):
                    raise ProgrammingError("Permission must be a list of strings")

                try:
                    if hasattr(args[0], "__class__") and isinstance(args[0], APIView):
                        request = args[1]

                    elif hasattr(args[0], "user"):
                        request = args[0]

                    else:
                        raise IndexError()

                except IndexError:
                    raise ProgrammingError("Missing request information, use this decorator with DRF View")

                authorization = request.headers.get("Authorization", "")
                if not authorization:
                    raise ValidationException("Unauthorized", code=401, slug="no-authorization-header")

                if authorization.startswith("Link ") and mode != "signature":
                    authorization = authorization.replace("Link ", "")
                    app, token = link_schema(request, scopes, authorization, mode == "signature")

                    cu = functools.partial(get_user, token["app"], token["sub"])
                    setattr(request, "get_user", cu)

                    return function(*args, **kwargs, token=AttrDict(**token), app=AttrDict(**app))

                elif authorization.startswith("Signature ") and mode != "jwt":
                    authorization = authorization.replace("Signature ", "")
                    app = signature_schema(request, scopes, authorization, mode == "signature")
                    return function(*args, **kwargs, app=AttrDict(**app))

                else:
                    raise ValidationException(
                        "Unknown auth schema or this schema is forbidden", code=401, slug="unknown-auth-schema"
                    )

            return wrapper

        return decorator

    def ascope(scopes: Optional[list] = None, mode: Optional[str] = None) -> callable:
        """Check if the app has access to the scope provided."""

        if scopes is None:
            scopes = []

        def decorator(function: callable) -> callable:

            @functools.wraps(function)
            async def wrapper(*args, **kwargs):
                request: HttpRequest

                if isinstance(scopes, list) is False:
                    raise ProgrammingError("Permission must be a list")

                if len([x for x in scopes if not isinstance(x, str)]):
                    raise ProgrammingError("Permission must be a list of strings")

                try:
                    if hasattr(args[0], "__class__") and isinstance(args[0], APIView):
                        request = args[1]

                    elif hasattr(args[0], "user"):
                        request = args[0]

                    else:
                        raise IndexError()

                except IndexError:
                    raise ProgrammingError("Missing request information, use this decorator with DRF View")

                authorization = request.headers.get("Authorization", "")
                if not authorization:
                    raise ValidationException("Unauthorized", code=401, slug="no-authorization-header")

                if authorization.startswith("Link ") and mode != "signature":
                    authorization = authorization.replace("Link ", "")
                    app, token = await sync_to_async(link_schema)(request, scopes, authorization, mode == "signature")

                    cu = functools.partial(get_user, token["app"], token["sub"])
                    setattr(request, "aget_user", cu)

                    return await function(*args, **kwargs, token=AttrDict(**token), app=AttrDict(**app))

                elif authorization.startswith("Signature ") and mode != "jwt":
                    authorization = authorization.replace("Signature ", "")
                    app = await sync_to_async(signature_schema)(request, scopes, authorization, mode == "signature")
                    return await function(*args, **kwargs, app=AttrDict(**app))

                else:
                    raise ValidationException(
                        "Unknown auth schema or this schema is forbidden", code=401, slug="unknown-auth-schema"
                    )

            return wrapper

        return decorator

    return scope, ascope
