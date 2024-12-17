"""Cases for testing ``get_last_activity`` capability."""

import typing as t

import httpx
from connector.generated import (
    ActivityEventType,
    ErrorResponse,
    GetLastActivity,
    GetLastActivityRequest,
    GetLastActivityResponse,
    LastActivityData
)

from tests.common_mock_data import VALID_AUTH
from connector.tests.type_definitions import MockedResponse, ResponseBodyMap

from connector.generated.models.capability_name import CapabilityName

Case: t.TypeAlias = tuple[
    CapabilityName,
    GetLastActivityRequest,
    ResponseBodyMap,
    GetLastActivityResponse | ErrorResponse,
]


def case_one_user_200() -> Case:
    """Successful request."""
    args = GetLastActivityRequest(
        request=GetLastActivity(account_ids=["user_1_id"]),
        auth=VALID_AUTH,
    )

    response_body_map = {{
        "GET": {{
            "/example": MockedResponse(
                status_code=httpx.codes.OK,
                response_body={{}},
            ),
        }},
    }}
    expected_response = GetLastActivityResponse(
        response=[
            LastActivityData(
                account_id="user_1_id",
                event_type=ActivityEventType.LAST_LOGIN,
                happened_at="2024-07-01T20:43:09-10:00",
            )
        ],
        page=None,
    )
    return CapabilityName.GET_LAST_ACTIVITY, args, response_body_map, expected_response
