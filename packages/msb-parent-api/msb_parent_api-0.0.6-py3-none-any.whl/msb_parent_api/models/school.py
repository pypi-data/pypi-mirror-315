"""School Model Definition."""
from msb_parent_api.base import DataModel
from msb_parent_api.msb_api_client import Schools
from typing import Optional


class School(DataModel):
    """Student Model Definition."""
    def __init__(self, school_resp: Schools):
        self._grade                              = school_resp.grade
        self._homeroom                           = school_resp.homeroom
        self._active                             = school_resp.active
        self._enabled                            = school_resp.enabled
        self._schoolName                         = school_resp.schoolName
        self._schoolSID                          = school_resp.schoolSID
        self._schoolID                           = school_resp.schoolID
        self._schoolMenuLink                     = school_resp.schoolMenuLink
        self._schoolNumber                       = school_resp.schoolNumber

    @property
    def grade(self) -> int:
        """Property Definition."""
        return self._grade
    
    @property
    def homeroom(self) -> Optional[str]:
        """Property Definition."""
        return self._homeroom
    
    @property
    def active(self) -> bool:
        """Property Definition."""
        return self._active
    
    @property
    def enabled(self) -> bool:
        """Property Definition."""
        return self._enabled
    
    @property
    def schoolName(self) -> str:
        """Property Definition."""
        return self._schoolName
    
    @property
    def schoolSID(self) -> str:
        """Property Definition."""
        return self._schoolSID
    
    @property
    def schoolID(self) -> int:
        """Property Definition."""
        return self._schoolID
    
    @property
    def schoolMenuLink(self) -> Optional[str]:
        """Property Definition."""
        return self._schoolMenuLink
    
    @property
    def schoolNumber(self) -> int:
        """Property Definition."""
        return self._schoolNumber