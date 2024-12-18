"""Base MySchoolBucks Class."""
import logging

from .models.student import Student
from .models.meal import Meal
from .msb_api_client import MySchoolBucksApiClient

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)


class MySchoolBucks():
    """Define MySchoolBucks Class."""
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
        self._api_client = MySchoolBucksApiClient(base_url, username, secret, apikey, appauth, debug)

        if debug:
            _LOGGER.setLevel(logging.DEBUG)

    async def authenticate(self, session) -> bool:
        """Authenticate with mySchoolBucks."""
        authresp = await self._api_client.authenticate(session)
        return authresp

    async def students(self) -> list[Student]:
        """Get Students."""
        studentsresp = await self._api_client.get_students()
        students = [Student(response) for response in studentsresp]
        return students
    
    async def meals(self, clientKey, studentSID) -> list[Meal]:
        """Get Meals."""
        mealsresp = await self._api_client.get_meals(clientKey, studentSID)
        meals = [Meal(response) for response in mealsresp]
        return meals