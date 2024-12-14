from enum import Enum
import requests
from . import config, error


class Request:
    class Method(Enum):
        GET = 1
        POST = 2
        PUT = 3
        DELETE = 4

    @classmethod
    def call(
        cls,
        method: Method,
        url: str,
        data: dict[str, str] | None = None,
    ):
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {config.secret_key}",
        }

        if method == Request.Method.GET:
            resp = requests.get(url, headers=headers)
        elif method == Request.Method.POST:
            resp = requests.post(url, headers=headers, json=data)
        elif method == Request.Method.PUT:
            resp = requests.put(url, headers=headers, json=data)
        elif method == Request.Method.DELETE:
            resp = requests.delete(url, headers=headers)
        else:
            raise ValueError("Invalid method")

        return cls.process_response(resp)

    @classmethod
    def process_response(cls, resp):
        response = resp.json()
        print(resp, response)

        if resp.status_code == 400:
            message = response.get("errorMessage")
            raise error.ErcasBadRequestError(message)
        if resp.status_code == 404:
            message = response.get("errorMessage")
            raise error.ErcasNotFoundError(message)
        if resp.status_code == 422:
            message = response.get("errorMessage")
            raise error.ErcasUnprocessableError(message)
        return response.get("responseBody")
