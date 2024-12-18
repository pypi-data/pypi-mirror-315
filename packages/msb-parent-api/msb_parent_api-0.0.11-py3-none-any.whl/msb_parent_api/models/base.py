"""Base Model Definition."""
from typing import Optional
from pydantic import BaseModel, Field

class Schools(BaseModel):
    """School Definition"""
    grade                              : int
    homeroom                           : Optional[str] = None
    active                             : bool
    enabled                            : bool
    schoolName                         : str
    schoolSID                          : str
    schoolID                           : int
    schoolMenuLink                     : Optional[str] = None
    schoolNumber                       : int

class MealPaymentsAcceptedPaymentMethods(BaseModel):
    """Meal Payments Definition"""
    isVisaAccepted                     : bool
    isMasterCardAccepted               : bool
    isDiscoverAccepted                 : bool
    isAmexAccepted                     : bool
    isECheckAccepted                   : bool
    creditCardAccepted                 : bool

class StudentResponse(BaseModel):
    """Student Response Definition."""
    class Config:
        exclude = ['mealpaymentsAcceptedPaymentMethods']
    balance                            : float
    balanceLastUpdated                 : str
    canBeFunded                        : bool
    firstName                          : str
    lastName                           : str
    pendingAmount                      : float
    clientKey                          : str
    schools                            : Optional[list[Schools]] = None
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
    #mealPaymentsAcceptedPaymentMethods : Optional[MealPaymentsAcceptedPaymentMethods] = None
    status                             : str
    eligibility                        : str
    outstandingInvoicesCount           : int
    outstandingInvoicesAmount          : int
    householdID                        : Optional[str] = None

class MealResponse(BaseModel):
    itemDescription                    : str
    extendedDescription                : Optional[str] = None
    mealSession                        : str
    schoolName                         : Optional[str] = None
    studentName                        : str
    studentSID                         : str
    totalTransactionAmount             : str
    transactionAmount                  : str
    transactionDate                    : str
    transactionID                      : str