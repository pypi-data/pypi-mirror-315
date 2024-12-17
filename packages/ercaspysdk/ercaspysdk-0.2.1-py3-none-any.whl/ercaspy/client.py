# client.py
import requests
from .models import *
from .exceptions import APIError
from requests.exceptions import JSONDecodeError
import json

class Ercaspy:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.merchant.staging.ercaspay.com/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _request(self, method: str, endpoint: str, data=None, params=None):
        url = f"{self.base_url}{endpoint}"
        try:
          
            response = requests.request(
                method, url, headers=self.headers, json=data, params=params
            )
            
            if response.status_code not in range(200, 300):
                try:
                    # Attempt to parse JSON error response
                    error_data = response.json()
                    error_message = error_data.get("errorMessage", "An error occurred")
                except JSONDecodeError:
                    # If response is not JSON, fall back to raw text
                    error_message = response.text or f"HTTP {response.status_code} Error"
                
                # Return clean error structure
                clean_error = {
                    "message": error_message,
                    "status": "failed",
                    "code": response.status_code,
                }
                raise APIError(message=error_message, status_code=response.status_code, response_data=clean_error)
            
            # Parse JSON for successful responses
            try:
                return response.json()
            except JSONDecodeError:
                raise APIError(
                    message={"message": "Invalid JSON response", "status": "failed", "code": 500}
                )

        except requests.RequestException as e:
            raise APIError(
                message={"message": f"Request failed: {str(e)}", "status": "failed", "code": 500}
            )

        
    def initiate_payment(self, payment_data: CheckOutRequest, **args) -> TransactionResponse:
        response_data = self._request(
            "POST", "/payment/initiate", data=payment_data
        )
        return TransactionResponse(**response_data)

    def verify_transaction(self, payment_ref: str) -> TransactionResponse:
        response_data = self._request("GET", f"/payment/transaction/verify/{payment_ref}")
        return TransactionResponse(**response_data)
    
    def initiate_bank_transfer_request(self, transaction_ref:str ) -> TransactionResponse :
        response_data = self._request("GET", f"/payment/bank-transfer/request-bank-account/{transaction_ref}")
        return TransactionResponse(**response_data)
    
    def initiate_bank_transfer(self, data:TransferRequest) -> TransactionResponse :
       checkout_response = self.initiate_payment(data)
       transaction_reference = checkout_response.responseBody['transactionReference']
  
     
       get_account_details = self.initiate_bank_transfer_request(transaction_reference)
       return get_account_details
       
       
         
    
    def check_direct_payment_status(self, transaction_ref:str, payment_method:str) ->  TransactionResponse:
        response_data = self._request("POST", f"/payment/status/{transaction_ref}" , data={
            "payment_method": payment_method,
            "reference": transaction_ref
        } )
        return TransactionResponse(**response_data)

    def initiate_ussd_transaction(self, data:TransferRequest , bank_name:str ) -> TransactionResponse:
        checkout_response = self.initiate_payment(data)
        reference = checkout_response.responseBody['transactionReference']
        print(reference)
        response_data = self._request("POST", f"/payment/ussd/request-ussd-code/{reference}", data={
            "bank_name": bank_name
        })
       
        return TransactionResponse(**response_data)
    

    def initiate_card_transaction(self,payload, transaction_ref) -> TransactionResponse:
        from .utils import get_device_details

        data = {
            "payload":payload,
            "deviceDetails":get_device_details(),
            "transactionReference":transaction_ref
        }
        response_data = self._request("POST", "/payment/cards/initialize", data=data)

        return TransactionResponse(**response_data)

    def submit_otp(self, otp:str, transaction_ref:str, gateaway_ref:str  ) -> TransactionResponse:
        data = {
            "otp": otp,
            "gatewayReference": gateaway_ref,
        }

        print(data)
        response_data = self._request("POST", f"/payment/cards/otp/submit/{transaction_ref}", data=data)
        return TransactionResponse(**response_data)
    
    def resend_otp(self, transaction_ref:str, gateaway_ref:str  ) -> TransactionResponse:
        data = {
            "gatewayReference": gateaway_ref,
        }
        response = self._request("POST", f"/payment/cards/otp/resend/{transaction_ref}" , data=data)
        return TransactionResponse(**response)

    def get_card_details(self, transaction_reference) -> TransactionResponse:
        response = self._request("GET", f"/payment/cards/details/{transaction_reference}")
        return TransactionResponse(**response)
    
    def verify_card_transaction(self, reference:str ):
        data = {
            "reference": reference
        }

        response = self._request("POST", f"/payment/cards/transaction/verify", data=data)
        return TransactionResponse(**response)
    
    def cancle_transaction(self, transaction_ref:str ) -> TransactionResponse:
        response = self._request("GET", f"/payment/cancel/{transaction_ref}")
        return TransactionResponse(**response)

    def get_banks_list(self):
        response = self._request("GET", "/payment/ussd/supported-banks")
        return (response)
       
