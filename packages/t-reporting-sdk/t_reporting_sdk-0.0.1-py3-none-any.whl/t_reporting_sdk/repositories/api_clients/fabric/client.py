import logging
from os import environ
from typing import Any, Optional

import requests
from pydantic import BaseModel, Field

from t_reporting_sdk.repositories.api_clients.fabric.auth import JWTAuth


logger = logging.getLogger(__name__)


class FabricClientConfig(BaseModel):
    user_email: str = Field(default=environ.get("FABRIC_USER_EMAIL"), validate_default=True)
    user_otp_secret: str = Field(default=environ.get("FABRIC_USER_OTP_SECRET"), validate_default=True)
    base_url: str = Field(default=environ.get("FABRIC_BASE_URL"), validate_default=True)


class FabricClient:
    def __init__(
        self, 
        config: Optional[FabricClientConfig] = None,
    ):
        config = config or FabricClientConfig()
        fabric_auth = JWTAuth(
            email=config.user_email,
            otp_secret=config.user_otp_secret,
            auth_url=config.base_url + "/verify",
            refresh_url=config.base_url + "/refresh-token",
        )
        self._session = requests.Session()
        self._session.auth = fabric_auth

        # Using the /me endpoint as a temporary solution for reporting.
        # This should be replaced with the actual reporting endpoint when available.
        self._reporting_url = config.base_url + "/me"

    def send_report(self, report: Any) -> Any:
        # This is a temporary solution because the actual reporting endpoint is not yet available.
        # The proper reporting endpoint should be used once it is implemented.
        response = self._session.get(self._reporting_url)
        response.raise_for_status()
