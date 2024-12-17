"""Base Model Definition."""
from typing import Optional
from pydantic import BaseModel, Field

class StudentResponse(BaseModel):
    """Student Response Definition."""
    balance                            : float
    balanceLastUpdated                 : str
    canBeFunded                        : bool
    firstName                          : str
    lastName                           : str
    pendingAmount                      : float
    clientKey                          : str
    schools                            : Optional[str] = None
    studentID                          : str
    studentSID                         : str
    dailySpendingLimitAmt              : float
    weeklySpendingLimitAmt             : float
    breakfastSpendingLimitAmt          : float
    lunchSpendingLimitAmt              : float
    snackSpendingLimitAmt              : float
    dinnerSpendingLimitAmt             : float
    lowBalanceThreshold                : float
    sendLowBalanceNotification         : bool
    limitMealOptions                   : str
    allowALaCarteVending               : bool
    allowReimbursableMealVending       : bool
    lastFundedAmt                      : float
    mealPaymentsAcceptedPaymentMethods : Optional[str] = None
    status                             : str
    eligibility                        : str
    outstandingInvoicesCount           : int
    outstandingInvoicesAmount          : int
    householdID                        : str