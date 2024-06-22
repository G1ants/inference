from enum import StrEnum
from typing import Any


class Functions(StrEnum):
    GET_RESPONSE = "get_response"


def get_response_function() -> list[dict[str, Any]]:
    # TODO: if necessary
    response_functions: list[dict[str, Any]] = [
        {
            "name": Functions.GET_RESPONSE,
        }
    ]
