Ercaspay SDK provides an easy way to interact with the Ercaspay payment gateway. This SDK simplifies the process of making payments, verifying transactions, and handling various payment methods.

## Installation

To install the Ercaspay SDK, you can use pip:

```bash
pip install ercaspy
```

## Usage

To use the Ercaspay SDK, you need to import the `Ercaspy` class and initialize it with your API key. Below is an example of how to initiate a payment:

```python

from ercaspy.client import Ercaspy
from ercaspy.exceptions import APIError

client = Ercaspy(api_key="YOUR_API_KEY")

payment_data = {
    "amount": "1500",
    "paymentReference": "unique_reference",
    "customerName": "John Doe",
    "customerEmail": "john.doe@example.com",
    "currency": "NGN",
    "redirectUrl": "https://your_redirect_url.com",
    "paymentMethods": "card"
}

def initiate_payment():
    try:
        response = client.initiate_checkout(payment_data=payment_data)
        print(response)
    except APIError as e:
        print(f"An error occurred while initiating payment: {e}")

initiate_payment()
```

## Error Handling

The SDK raises `APIError` exceptions for various error scenarios, including:

- Invalid API key
- Network issues
- Invalid response from the server

You can catch these exceptions in your code to handle errors gracefully.

```python
try:
    # Your API call
except APIError as e:
    print(f"An error occurred: {e}")
```

## Examples

Here are some examples of how to use the SDK for different payment methods:

### Initiating a Card Transaction

```python
data = {
    "card_number": "5123450000000008",
    "cvv": "100",
    "pin": "1234",
    "expiry_date": "0139",
    "transaction_reference": "unique_transaction_reference"
}

def initiate_card_transaction(data):
    try:
        response = client.initiate_card_transaction(data)
        print(response)
    except APIError as e:
        print(f"An error occurred while initiating card transaction: {e}")

initiate_card_transaction(data)
```

### Verifying a Transaction

```python
def verify_transaction(transaction_ref):
    try:
        response = client.verify_transaction(transaction_ref)
        print(response)
    except APIError as e:
        print(f"An error occurred while verifying transaction: {e}")

verify_transaction("unique_transaction_reference")
```

## Checkout Payment
Checkout payment allows your customer to make payment using the standard ercaspay checkout page for easy payment.

### Usage

```python
from ercaspy.client import Ercaspy
from ercaspy.exceptions import APIError

client = Ercaspy(api_key="Your Api key")
# Note: specify payment methods you want your customer to pay with, cards, ussd, and bank transfer
payment_data = {
   "amount": "1500",
   "paymentReference": "unique_transaction_code",
   "customerName": "Sheden",
   "customerEmail": "shedenbright@gmail.com",
   "currency": "NGN",
   "redirectUrl": "https://frontendurl.com",
   "paymentMethods": "card, ussd, bank-transfer"   
}

def initiate_payment(payment_method):
    try:
        response = client.initiate_payment(payment_data=payment_data)
        print(response)
    except APIError as e:
        print(f"An error occurred while verifying payment status: {e}")

# Sample response   
# requestSuccessful=True responseCode='success' responseMessage='success' responseBody={'paymentReference': 'olamide123456', 'transactionReference': 'ERCS|20241216193301|1734373981563', 'checkoutUrl': 'https://sandbox-checkout.ercaspay.com/ERCS|20241216193301|1734373981563'}

# You will redirect your user to the checkoutUrl, after successful payment, your user will be redirected back to your app, to the specified redirect url, you specified to initialize the payment.

# Read the official doc for more detail

# Verify checkout transaction

# Call the verify_transaction method to verify your checkout transaction 

client.verify_transaction('transaction_ref')

# Pass the transaction ref generated from the initiate payment method.

# Always refer to the main doc for more details

# Direct Integration

# Bank Transfer:
The bank transfer method returns dynamic bank details that your customer can make payment to, note the account number can only be used once by a customer or user.

- It takes the same payload data as initiate payment but here in the payment method you specify the bank transfer only as the payment method.

Sample payload

payment_data = {
   "amount": "1500",
   "paymentReference": "transaction_ref_generated_by_u",
   "customerName": "Sheden",
   "customerEmail": "shedenbright@gmail.com",
   "currency": "NGN",
   "redirectUrl": "https://frontendurl.com",
   "paymentMethods": "bank-transfer"   
}

# Usage
```
client.initiate_bank_transfer(data=data)

# or full integration

def bank_transfer(data):
   try:
      res = client.initiate_bank_transfer(data=data)
      print(res)
   except APIError as e:
      print(e)

# Verify or check the direct integration payment status

# To verify or check the direct integration method call the check_direct_payment_status
# Pass the transaction ref generated from the initiate bank transfer and the payment method.

# Note: payment method will be "bank-transfer" for other payments like card and ussd, you do the same.

# Always check the main doc for more details

# Usage

``` 
def verify_payment(transaction_ref, payment_method):
   try:
      response = client.check_direct_payment_status(transaction_ref=f"{transaction_ref}", payment_method=payment_method)
      print(response)
   except APIError as e:
      print(f"An error occurred while verifying payment status: {e}")

# Always refer back to the official doc for full details

# USSD PAYMENT

Ussd payment allows your customer to pay with their phone without internet. You can always refer back to the official doc for more information.

The endpoint generates the ussd code for your customer to use.

Call the initiate_ussd_transaction method to generate the ussd code for payment. It accepts two params: data and the bank_name.

The data contains the payment_data or payload you used for the initiate checkout payment and the bank transfer but in this case, the payment method would be "ussd", customer details and other things remain the same. The bank_name params allow you to define the bank you want, use the get_banks method to fetch supported banks by ercaspay.

# Usage

```python
payment_data = {
   "amount": "1500",
   "paymentReference": "olamide123456",
   "customerName": "Sheden",
   "customerEmail": "shedenbright@gmail.com",
   "currency": "NGN",
   "redirectUrl": "https://frontendurl.com",
   "paymentMethods": "ussd"   
}

def ussd_transaction(payment_data):
   try:
      response = client.initiate_ussd_transaction(data=payment_data, bank_name="fcmb")
      print(response)
   except APIError as e:
      print(f"An error occurred while initiating USSD transaction: {e}")

# Verify ussd payment:
# Note: I will advise you to set webhook for your payment verification.

You can always call check_direct_payment_status method to verify payment as it returns the status of the payment and the transaction details.

# Usage

```python
payment_method = "ussd"
transaction_ref = "Transaction ref generated by initiate ussd transaction"
def verify_payment(transaction_ref, payment_method):
   try:
      response = client.check_direct_payment_status(transaction_ref=f"{transaction_ref}", payment_method=payment_method)
      print(response)
   except APIError as e:
      print(f"An error occurred while verifying payment status: {e}")

# Get Supported bank List

client.get_bank_list()

# Card payment transaction
Card payment allows your customer to pay with their debit or credit card.

# Step One:
Call the client.initiate_payment(payment_data), then you must put "card" as your paymentMethod then, you use the generated transaction_ref to call client.initiate_card_payment.

Note:
You have to encrypt the card details using the following algo, you can always check the official doc for full details.

```python
def encryptCard(card_number: str, cvv: str, pin: str, expiry_date: str):
    """
    Encrypt data
    """
    # Read the public key
    with open('key/rsa_public_key.pub', 'rb') as key_file:
        public_key_data = key_file.read()
    public_key = RSA.import_key(public_key_data)
    # Card details
    cardParams = {
        'cvv': cvv,
        'pin': pin,
        'expiryDate': expiry_date,
        'pan': card_number
    }
    # Convert card details to JSON
    cardJson = json.dumps(cardParams).encode('utf-8')
    # Encrypt the card details using PKCS1_v1_5 padding
    cipher = PKCS1_v1_5.new(public_key)
    encrypted = cipher.encrypt(cardJson)
    # Return the encrypted data as a Base64-encoded string
    return base64.b64encode(encrypted).decode('utf-8')

# Full usage 
data = {
   "card_number": "5123450000000008",
   "cvv": "100",
   "pin": "1234",
   "expiry_date": "0139",
   "transaction_reference": "ERCS|20241216191025|1734372625377"
}

payload = encryptCard(data["card_number"], data["cvv"], data['pin'], data["expiry_date"])

def initiate_card_transaction(payload, transaction_ref):
   try:
      response = client.initiate_card_transaction(payload=payload, transaction_ref=transaction_ref)
      print(response)
   except APIError as e:
      print(f"An error occurred while initiating card transaction: {e}")

initiate_card_transaction(payload=payload, transaction_ref=data['transaction_reference'])

Visit the official doc for full details.

# Submit OTP
It depends on the response code of your card transaction, check the official doc for more details.

client.submit_otp

```python
def submit_otp(otp, transaction_ref, gateaway_ref):
   try:
      response = client.submit_otp(otp=otp, transaction_ref=transaction_ref, gateaway_ref=gateaway_ref)
      print(response)
   except APIError as e:
      print(f"An error occurred while submitting OTP: {e}")

# Resend OTP
def resend_otp(transaction_ref, gateaway_ref):
   try: 
      response = client.resend_otp(transaction_ref, gateaway_ref)
      print(response)
   except APIError as e:
      print(f"An error occurred while resending OTP: {e}")

# Verify card transaction
Note: It is recommended to use webhook for payment transaction.

Call the client.verify_card_payment to verify your card transaction or use the direct_payment_status.

# Usage

```python
payment_method = "card"
transaction_ref = "Transaction ref generated by initiate ussd transaction"
def verify_payment(transaction_ref, payment_method):
   try:
      response = client.check_direct_payment_status(transaction_ref=f"{transaction_ref}", payment_method=payment_method)
      print(response)
   except APIError as e:
      print(f"An error occurred while verifying payment status: {e}")

# or 

```python
def verify_card_transaction(reference):
   try:
      response = client.verify_card_transaction(reference)
      print(response)
   except APIError as e:
      print(f"An error occurred while verifying card transaction: {e}")

# Get Card details
You can always get card transaction details using client.get_card_details.

# Usage

```python
def get_card_details(transaction_ref):
   try: 
      response = client.get_card_details(transaction_ref)
      print(response)

   except APIError as e:
      print(f"An error occurred while getting card details: {e}")

# Cancel Transaction

client.cancel_transaction

Note: You can only cancel a transaction that has not been successful.

# Thanks
Developed and written by Sheden Bright | shedenbright@gmail.com
Visit my resume: www.sheden-resume.netlify.app
