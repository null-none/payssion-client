import requests
import hashlib
import json
from collections.abc import MutableMapping
from urllib.parse import urlencode, unquote

from .exceptions import ValidationError, AuthorizationError, FailedRequest


class Payssion:

    VERSION = "1.3.0.160612"

    api_url = ""
    api_key = ""
    secret_key = ""

    sig_keys = {
        "create": ["api_key", "pm_id", "amount", "currency", "order_id", "secrey_key"],
        "details": ["api_key", "transaction_id", "order_id", "secret_key"],
    }

    http_errors = {
        400: "400 Bad Request",
        401: "401 Unauthorized",
        500: "500 Internal Server Error",
        501: "501 Not Implemented",
        502: "502 Bad Gateway",
        503: "503 Service Unavailable",
        504: "504 Gateway Timeout",
    }

    is_success = False
    ssl_verify = False

    allowed_request_methods = [
        "get",
        "put",
        "post",
        "delete",
    ]

    def __init__(self, api_key, secret_key, is_livemode=False):
        self.api_key = api_key
        self.secret_key = secret_key
        self.set_live_mode(is_livemode)

    def flatten(self, dictionary, parent_key=False, separator=".", separator_suffix=""):
        items = []
        for key, value in dictionary.items():
            new_key = (
                str(parent_key) + separator + key + separator_suffix
                if parent_key
                else key
            )
        if isinstance(value, MutableMapping):
            items.extend(flatten(value, new_key, separator, separator_suffix).items())
        elif isinstance(value, list) or isinstance(value, tuple):
            for k, v in enumerate(value):
                items.extend(
                    flatten({str(k): v}, new_key, separator, separator_suffix).items()
                )
        else:
            items.append((new_key, value))
        return dict(items)

    def set_live_mode(self, is_livemode):
        if is_livemode:
            self.api_url = "https://www.payssion.com/api/v1/payment/"
        else:
            self.api_url = "http://sandbox.payssion.com/api/v1/payment/"

    def set_url(self, url):
        self.api_url = url

    def set_ssl_verify(self, ssl_verify):
        self.ssl_verify = ssl_verify

    def set_is_success(self):
        self.is_success = True

    def create(self, params):
        return self.call("create", "post", params)

    def get_details(self, params):
        return self.call("details", "post", params)

    def check_request_method(self, request):
        if request in allowed_request_methods:
            return True
        return False

    def get_sig(self, params, sig_keys):
        msg_array = {}
        for key in sig_keys:
            msg_array[key] = params[key]
        msg_array["secret_key"] = self.secret_key
        msg = "|".join(msg_array)
        md5 = hashlib.md5()
        md5.update(msg)
        return md5.hexdigest()

    def get_headers(self):
        ua = {
            "version": self.VERSION,
            "lang": "python",
            "lang_version": "3.7",
            "publisher": "payssion",
            "uname": "uname",
        }
        headers = {
            "X-Payssion-Client-User-Agent": json.dumps(ua),
            "User-Agent": "Payssion/php/{}".format(self.VERSION),
            "Content-Type": "application/x-www-form-urlencoded",
        }
        return headers

    def push_data(self, method, request, params):
        api = requests.Session()
        api.headers.update(self.get_headers())
        params = flatten(params, False, "[", "]")
        query = urlencode(params)
        query_parsed = unquote(query)
        response = requests.post("{}{}".format(self.api_url, method), data=query_parsed)
        return response

    def call(self, method, request, params):
        self.is_succes = False
        if not self.check_request_method(request):
            raise "Not allowed request method type"
        params["api_key"] = self.api_key
        params["api_sig"] = self.get_sig(params, self.sig_keys[method])
        resposne = self.push_data(method, request, params)
        status_code = response.status_code
        data = response.json()
        if status_code >= 200 and status_code < 300:
            return data
        else:
            if status_code == 401:
                raise AuthorizationError(message, payload)
            if status_code == 400:
                raise ValidationError(message, payload)
            raise FailedRequest(message, status_code, payload)
        return data
