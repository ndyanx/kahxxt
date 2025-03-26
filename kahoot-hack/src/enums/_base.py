from enum import Enum


class RequestMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class RequestReturn(str, Enum):
    TEXT = "text"
    JSON = "json"
    SOUP = "soup"
    RESPONSE = "response"
