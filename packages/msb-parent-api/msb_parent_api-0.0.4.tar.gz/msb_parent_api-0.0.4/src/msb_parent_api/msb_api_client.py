"""Infinite Campus API Client."""
import logging

from urllib.parse import urljoin

import aiohttp

from .errors import MySchoolBucksError
from .models.base import StudentResponse

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)


def _enable_debug_logging():
    _LOGGER.setLevel(logging.DEBUG)


class MySchoolBucksApiClient():
    """MySchoolBucks Parent API Client."""
    def __init__(
        self,
        base_url,
        username,
        secret,
        apikey,
        appauth,
        path: str = None,
        debug=False,
    ):
        if debug:
            _enable_debug_logging()

        self._base_url = base_url

        _LOGGER.debug(f"generated base url: {self._base_url}")

        self._username = username
        self._secret = secret
        self._apikey = apikey
        self._appauth = appauth
        self._headers = {
            "Accept": "application/json",
            "apiKey": self._apikey,
            "appAuthorization": self._appauth,
            "deviceDesc": "samsung SM-S901U Android 14",
            "content-type": "application/json; charset=utf-8",
            "userID": self._username,
            "password": self._secret
            }

    async def authenticate(self, session):
        """Test if we can authenticate with the district."""
        try:
            request_url = urljoin(
                self._base_url, (f"/mobileapi/9.0/auth/userSession")
            )
            async with session.post(request_url,headers=self._headers) as authresponse:
                response = authresponse
                responsetext = await response.text()
                responsejson = await response.json()
                if response.status == 200 and responsejson['loginResult'] == 'SuccessfulLogon':
                    return True
                raise MySchoolBucksError(400, "Bad Credentials")
        except Exception as error:
            raise MySchoolBucksError(400, error)

    async def _get_request(self, end_url: str):
        """Perform GET request to API endpoint."""
        request_url = urljoin(self._base_url, end_url)
        async with aiohttp.ClientSession() as session:
            authenticated = await self.authenticate(session)
            if authenticated:
                async with session.get(f"{request_url}", headers=self._headers) as resp:
                    response = resp
                    responsetext = await resp.text()
                    response_json = await resp.json()
                    if response.status >= 400:
                        raise MySchoolBucksError(response.status, responsetext)
                    return response_json
            raise MySchoolBucksError(400, "Bad Credentials")

    async def get_students(self) -> list[StudentResponse]:
        """Get MySchoolBucks Students."""
        parsed_response = await self._get_request("/mobileapi/9.0/parent/students")
        if parsed_response:
            studentresp: list[StudentResponse] = [StudentResponse(**resp) for resp in parsed_response]
            return studentresp
        return []