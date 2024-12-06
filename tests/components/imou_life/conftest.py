from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest
from pyimouapi import ImouOpenApiClient

imou_token_return = {
    "accessToken": "test_token",
    "expireTime": 3600,
    "currentDomain": "https://openapi.imoulife.com:443"
}


@pytest.fixture
def imou_config_flow() -> Generator[MagicMock]:
    with (
        patch.object(ImouOpenApiClient, "async_get_token", return_value=True),
        patch("homeassistant.components.imou_life.config_flow.ImouOpenApiClient") as mock_client
    ):
        instance = mock_client.return_value = ImouOpenApiClient(
            "test_app_id",
            "test_app_secret",
            "openapi.imoulife.com"
        )
        instance.async_get_token = MagicMock(return_value=imou_token_return)
        yield mock_client
