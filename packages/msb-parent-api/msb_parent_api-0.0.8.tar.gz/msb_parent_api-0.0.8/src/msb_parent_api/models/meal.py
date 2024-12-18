"""Meal Model Definition."""
from msb_parent_api.base import DataModel
from msb_parent_api.msb_api_client import MealResponse
from typing import Optional


class Meal(DataModel):
    """Student Model Definition."""
    def __init__(self, meal_resp: MealResponse):
        self._itemDescription = meal_resp.itemDescription
        self._extendedDescription = meal_resp.extendedDescription
        self._mealSession = meal_resp.mealSession
        self._schoolName = meal_resp.schoolName
        self._studentName = meal_resp.studentName
        self._studentSID = meal_resp.studentSID
        self._totalTransactionAmount = meal_resp.totalTransactionAmount
        self._transactionAmount = meal_resp.transactionAmount
        self._transactionDate = meal_resp.transactionDate
        self._transactionID = meal_resp.transactionID
    
    @property
    def itemDescription(self) -> str:
        """Property Definition."""
        return self._itemDescription
    
    @property
    def extendedDescription(self) -> Optional[str]:
        """Property Definition."""
        return self._extendedDescription
    
    @property
    def mealSession(self) -> str:
        """Property Definition."""
        return self._mealSession
    
    @property
    def schoolName(self) -> Optional[str]:
        """Property Definition."""
        return self._schoolName
    
    @property
    def studentSID(self) -> str:
        """Property Definition."""
        return self._studentSID
    
    @property
    def studentName(self) -> str:
        """Property Definition."""
        return self._studentName
    
    @property
    def totalTransactionAmount(self) -> str:
        """Property Definition."""
        return self._totalTransactionAmount
    
    @property
    def transactionAmount(self) -> str:
        """Property Definition."""
        return self._transactionAmount
    
    @property
    def transactionDate(self) -> str:
        """Property Definition."""
        return self._transactionDate
    
    @property
    def transactionID(self) -> str:
        """Property Definition."""
        return self._transactionID
    
