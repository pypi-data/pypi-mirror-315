import sys
sys.path.append("..")
#from .client import PaymentGatewayClient
from ercaspy.client import Ercaspy
from ercaspy.exceptions import APIError

client = Ercaspy(api_key="ECRS-TEST-SKpkfMcETxlWCmBIiqNdlBvEHefPWpVsEqjxEtCX4D")

payment_data = {
   "amount":"1500",
    "paymentReference":"olamide123456",
    "customerName":"Sheden",
    "customerEmail":"shedenbright@gmail.com",
    "currency":"NGN",
    "redirectUrl":"https://frontendurl.com",
    "paymentMethods":"card"   
}


def initiate_payment():
    try:
        payment_data = {
        "amount":"500",
            "paymentReference":"olamide123456",
            "customerName":"Sheden",
            "customerEmail":"shedenbright@gmail.com",
            "currency":"NGN",
            "redirectUrl":"https://frontendurl.com",
            "paymentMethods":"card"   
        }

        response = client.initiate_payment(payment_data=payment_data)
        print(response)

    except APIError as e:
     print(f"An error occurred while verifying payment status: {e}")

#initiate_payment(payment_data)


def bank_transfer(trans_ref):
   
   try:
      bank_transfer = client.initiate_bank_transfer(transaction_ref=f"{trans_ref}")
      print(bank_transfer)
   except APIError as e:
      print(f"An error occured: {e}")



#bank_transfer("ERCS|20241213184609|1734111969262")
      

def verify_payment(transaction_ref, payment_method):
   try:
      
      response = client.check_direct_payment_status(transaction_ref=f"{transaction_ref}", payment_method=payment_method)
      print(response)
   except APIError as e:
      print(f"An error occurred while verifying payment status: {e}")



def new_bank_transfer(data):
   try:
      res =  client.initiate_bank_transfer(data=data)
      print(res)
   except APIError as e:
      print(e)

#new_bank_transfer(payment_data)

def ussd_transaction(payment_data):
   try:
      response = client.initiate_ussd_transaction(data=payment_data, bank_name="fcmb")
      print(response)
   except APIError as e:
      print(f"An error occurred while initiating USSD transaction: {e}")

#ussd_transaction(payment_data=payment_data)


#verify_payment('ERCS|20241214113507|1734172507514', 'ussd')


def  initiate_card_transaction(payload, transaction_ref):
   try:
      response = client.initiate_card_transaction(payload=payload, transaction_ref=transaction_ref)
      print(response)

   except APIError as e:
      print(f"An error occurred while initiating card transaction: {e}")
#print(initiate_card_transactions(payment_data))


def submit_otp(otp, transaction_ref, gateaway_ref):
   try:
      response = client.submit_otp(otp=otp, transaction_ref=transaction_ref, gateaway_ref=gateaway_ref)
      print(response)

   except APIError as e:
      print(f"An error occurred while submitting OTP: {e}")


data ={
   "otp":"123456",
   "gatewayReference":"ERFkil34jD",
  
}

def resend_otp(transaction_ref, gateaway_ref):
   try: 
      response = client.resend_otp(transaction_ref, gateaway_ref)
      print(response)
   except APIError as e:
      print(f"An error occurred while resending OTP: {e}")

def get_card_details(transaction_ref):
   try: 
      response = client.get_card_details(transaction_ref)
      print(response)

   except APIError as e:
      print(f"An error occurred while getting card details: {e}")


def verify_card_transaction(reference):
   try:
      response = client.verify_card_transaction(reference)
      print(response)
   except APIError as e:
      print(f"An error occurred while verifying card transaction: {e}")


def cancle_transaction(transaction_ref):
   try:
      response = client.cancle_transaction(transaction_ref)
      print(response)
   except APIError as e:
      print(f"An error occurred while cancelling transaction: {e}")


def verify_transaction(transaction_ref):
   try:
      response = client.verify_transaction(transaction_ref)
      print(response)
   except APIError as e:
      print(f"An error occurred while verifying transaction: {e}")


#submit_otp(otp="123456", transaction_ref="ERCS|20241215151139|1734271899175", gateaway_ref="bP2wxwdRCY")
#resend_otp(transaction_ref="ERCS|20241215151139|1734271899175", gateaway_ref="bP2wxwdRCY")
#initiate_payment(payment_data)
data ={
   "card_number":"5123450000000008",
   "cvv":"100",
   "pin":"1234",
   "expiry_date":"0139",
   "transaction_reference":"ERCS|20241216191025|1734372625377"

}

from ercaspy.utils import encryptCard

payload = encryptCard(data["card_number"], data["cvv"],data['pin'] , data["expiry_date"])



#initiate_card_transaction(payload=payload, transaction_ref=data['transaction_reference'])
#get_card_details("ERCS|20241215173021|1734280221912")
#verify_card_transaction("dZIsCEqg53")
#cancle_transaction(transaction_ref="ERCS|20241215151139|1734271899175")
#ussd_transaction(payment_data=payment_data)
#verify_payment("ERCS|20241215222920|1734298160289", payment_method="ussd")
#verify_transaction("ERCS|20241215222920|1734298160289")
#new_bank_transfer(payment_data)
#initiate_payment()


#print(client.get_banks_list())
