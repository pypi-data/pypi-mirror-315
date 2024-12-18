"""Student Model Definition."""
from msb_parent_api.base import DataModel
from msb_parent_api.msb_api_client import StudentResponse
from msb_parent_api.models.school import School
from msb_parent_api.models.payment import Payment
from typing import Optional


class Student(DataModel):
    """Student Model Definition."""
    def __init__(self, student_resp: StudentResponse):
        self._balance = student_resp.balance
        self._balanceLastUpdated = student_resp.balanceLastUpdated
        self._canBeFunded = student_resp.canBeFunded
        self._firstName  = student_resp.firstName
        self._lastName   = student_resp.lastName
        self._pendingAmount  = student_resp.pendingAmount
        self._clientKey  = student_resp.clientKey
        self._schools= student_resp.schools
        self._studentID  = student_resp.studentID
        self._studentSID = student_resp.studentSID
        self._dailySpendingLimitAmt  = student_resp.dailySpendingLimitAmt
        self._weeklySpendingLimitAmt = student_resp.weeklySpendingLimitAmt
        self._breakfastSpendingLimitAmt  = student_resp.breakfastSpendingLimitAmt
        self._lunchSpendingLimitAmt  = student_resp.lunchSpendingLimitAmt
        self._snackSpendingLimitAmt  = student_resp.snackSpendingLimitAmt
        self._dinnerSpendingLimitAmt = student_resp.dinnerSpendingLimitAmt
        self._lowBalanceThreshold= student_resp.lowBalanceThreshold
        self._sendLowBalanceNotification = student_resp.sendLowBalanceNotification
        self._limitMealOptions   = student_resp.limitMealOptions
        self._allowALaCarteVending   = student_resp.allowALaCarteVending
        self._allowReimbursableMealVending   = student_resp.allowReimbursableMealVending
        self._lastFundedAmt  = student_resp.lastFundedAmt
        #self._mealPaymentsAcceptedPaymentMethods = student_resp.mealPaymentsAcceptedPaymentMethods
        self._status = student_resp.status
        self._eligibility= student_resp.eligibility
        self._outstandingInvoicesCount   = student_resp.outstandingInvoicesCount
        self._outstandingInvoicesAmount  = student_resp.outstandingInvoicesAmount
        self._householdID= student_resp.householdID

    @property
    def balance(self) -> float:
        """Property Definition."""
        return self._balance

    @property
    def balanceLastUpdated(self) -> str:
        """Property Definition."""
        return self._balanceLastUpdated

    @property
    def canBeFunded(self) -> bool:
        """Property Definition."""
        return self._canBeFunded

    @property
    def firstName(self) -> str:
        """Property Definition."""
        return self._firstName

    @property
    def lastName(self) -> str:
        """Property Definition."""
        return self._lastName

    @property
    def pendingAmount(self) -> float:
        """Property Definition."""
        return self._pendingAmount

    @property
    def clientKey(self) -> str:
        """Property Definition."""
        return self._clientKey

    @property
    def schools(self) -> Optional[list[School]]:
        """Property Definition."""
        return [School(school) for school in self._schools]

    @property
    def studentID(self) -> str:
        """Property Definition."""
        return self._studentID
    
    @property
    def studentSID(self) -> str:
        """Property Definition."""
        return self._studentSID

    @property
    def dailySpendingLimitAmt(self) -> float:
        """Property Definition."""
        return self._dailySpendingLimitAmt

    @property
    def weeklySpendingLimitAmt(self) -> float:
        """Property Definition."""
        return self._weeklySpendingLimitAmt

    @property
    def brealfastSpendingLimitAmt(self) -> float:
        """Property Definition."""
        return self._breakfastSpendingLimitAmt

    @property
    def lunchSpendingLimitAmt(self) -> float:
        """Property Definition."""
        return self._lunchSpendingLimitAmt

    @property
    def snackSpendingLimitAmt(self) -> float:
        """Property Definition."""
        return self._snackSpendingLimitAmt

    @property
    def dinnerSpendingLimitAmt(self) -> float:
        """Property Definition."""
        return self._dinnerSpendingLimitAmt

    @property
    def lowBalanceThreshold(self) -> float:
        """Property Definition."""
        return self._lowBalanceThreshold

    @property
    def sendLowBalanceNotification(self) -> bool:
        """Property Definition."""
        return self._sendLowBalanceNotification

    @property
    def limitMealOptions(self) -> str:
        """Property Definition."""
        return self._limitMealOptions

    @property
    def allowALaCarteVending(self) -> bool:
        """Property Definition."""
        return self._allowALaCarteVending

    @property
    def allowReimburseableMealVending(self) -> bool:
        """Property Definition."""
        return self._allowReimbursableMealVending

    @property
    def lastFundedAmt(self) -> float:
        """Property Definition."""
        return self._lastFundedAmt

    #@property
    #def mealPaymentsAcceptedPaymentMethods(self) -> Optional[Payment]:
    #    """Property Definition."""
    #    return self._mealPaymentsAcceptedPaymentMethods

    @property
    def status(self) -> str:
        """Property Definition."""
        return self._status

    @property
    def eligibility(self) -> str:
        """Property Definition."""
        return self._eligibility

    @property
    def outstandingInvoicesCount(self) -> int:
        """Property Definition."""
        return self._outstandingInvoicesCount

    @property
    def outstnadingInvoicesAmount(self) -> int:
        """Property Definition."""
        return self._outstandingInvoicesAmount

    @property
    def householdID(self) -> str:
        """Property Definition."""
        return self._householdID