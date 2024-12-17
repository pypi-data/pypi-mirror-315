from pydantic import BaseModel, Field
from typing import Optional

class CheckOutRequest(BaseModel):
    amount: float
    paymentReference: str
    paymentMethods: Optional[str] = Field(None, description="Comma separated string of payment methods")
    customerName: str
    customerEmail: str
    customerPhoneNumber: Optional[str] = Field(None, description="Phone number of the customer")
    currency: Optional[str]= Field(default="NGN", description="Currency you want to receive payment in. Default is NGN.")
    feeBearer: Optional[str] = Field(None, description="Bearer of the charge (customer or merchant)")
    redirectUrl: Optional[str] = Field(None, description="URL to redirect user after payment completion")
    description: Optional[str] = Field(None, description="Description for the transaction")
    metadata: Optional[dict] = Field(None, description="Additional information relating to the transaction")

class TransactionResponse(BaseModel):
    requestSuccessful: Optional[bool] 
    responseCode: Optional[str] 
    responseMessage:Optional[str] 
    responseBody: dict = Field(default={}, description="Detailed response body")


class TransferRequest(BaseModel):
    amount: float
    paymentReference: str
    paymentMethods: str = Field(default="bank-transfer", description="Payment method for bank transfer")
    customerName: str
    customerEmail: str
    currency: str = Field(default="NGN", description="Currency for the transaction. Default is NGN.")

class ErrorResponse(BaseModel):
    error: str
    message: Optional[str]


class CardRequest(BaseModel):
    # card_number: str
    # cvv:str
    # pin:str
    # expiry_date:str
    payload: str
    transaction_reference: str
    #device_details: dict


class SubmitOtpRequest(BaseModel):
    otp: str
    gatewayReference: str
    transactionReference: str