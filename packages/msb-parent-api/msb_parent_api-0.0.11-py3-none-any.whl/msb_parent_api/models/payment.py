"""Payment Model Definition."""
from msb_parent_api.base import DataModel
from msb_parent_api.msb_api_client import MealPaymentsAcceptedPaymentMethods
from typing import Optional


class Payment(DataModel):
    """Payment Model Definition."""
    def __init__(self, payment_resp: MealPaymentsAcceptedPaymentMethods):
        self._isVisaAccepted                     = payment_resp.isVisaAccepted
        self._isMasterCardAccepted               = payment_resp.isMasterCardAccepted
        self._isDiscoverAccepted                 = payment_resp.isDiscoverAccepted
        self._isAmexAccepted                     = payment_resp.isAmexAccepted
        self._isECheckAccepted                   = payment_resp.isECheckAccepted
        self._creditCardAccepted                 = payment_resp.creditCardAccepted

    @property
    def isVisaAccepted(self) -> bool:
        """Property Definition."""
        return self._isVisaAccepted
    
    @property
    def isAmexAccepted(self) -> bool:
        """Property Definition."""
        return self._isAmexAccepted
    
    @property
    def isDiscoverAccepted(self) -> bool:
        """Property Definition."""
        return self._isDiscoverAccepted
    
    @property
    def isMasterCardAccepted(self) -> bool:
        """Property Definition."""
        return self._isMasterCardAccepted
    
    @property
    def isECheckAccepted(self) -> bool:
        """Property Definition."""
        return self._isECheckAccepted
    
    @property
    def creditCardAccepted(self) -> bool:
        """Property Definition."""
        return self._creditCardAccepted