# Ercaspay SDK Documentation

Ercaspay SDK provides an easy and efficient way to interact with the Ercaspay payment gateway. This SDK simplifies the process of making payments, verifying transactions, and handling various payment methods.

## Installation

To install the SDK, run:

```bash
pip install ercaspysdk
```

---

## **Checkout Payment**

Checkout payments allow your customers to make payments using the standard Ercaspay checkout page.

### **Usage**

```python
from ercaspy.client import Ercaspy
from ercaspy.exceptions import APIError

client = Ercaspy(api_key="Your_Api_Key")

payment_data = {
   "amount": "1500",
   "paymentReference": "unique_transaction_code",
   "customerName": "Sheden",
   "customerEmail": "shedenbright@gmail.com",
   "currency": "NGN",
   "redirectUrl": "https://frontendurl.com",
   "paymentMethods": "card, ussd, bank-transfer"
}

def initiate_payment():
    try:
        response = client.initiate_payment(payment_data=payment_data)
        print(response)
    except APIError as e:
        print(f"An error occurred while initiating payment: {e}")
```

**Sample Response:**

```json
{
    "requestSuccessful": True,
    "responseCode": "success",
    "responseMessage": "success",
    "responseBody": {
        "paymentReference": "olamide123456",
        "transactionReference": "ERCS|20241216193301|1734373981563",
        "checkoutUrl": "https://sandbox-checkout.ercaspay.com/ERCS|20241216193301|1734373981563"
    }
}
```

Redirect the user to the `checkoutUrl`. After a successful payment, the user will be redirected back to the specified `redirectUrl`.

---

## **Verify Checkout Transaction**

Call the `verify_transaction` method to verify a transaction.

### **Usage**

```python
transaction_ref = "transaction_reference_from_checkout"

def verify_transaction(transaction_ref):
    try:
        response = client.verify_transaction(transaction_ref)
        print(response)
    except APIError as e:
        print(f"An error occurred while verifying the transaction: {e}")
```

---

## **Direct Integration**

### **Bank Transfer**

The bank transfer method generates dynamic bank details for your customers to make payments. The account number can only be used once by the customer.

### **Usage**

```python
payment_data = {
   "amount": "1500",
   "paymentReference": "unique_transaction_ref",
   "customerName": "Sheden",
   "customerEmail": "shedenbright@gmail.com",
   "currency": "NGN",
   "redirectUrl": "https://frontendurl.com",
   "paymentMethods": "bank-transfer"
}

def bank_transfer(payment_data):
    try:
        response = client.initiate_bank_transfer(data=payment_data)
        print(response)
    except APIError as e:
        print(f"An error occurred while initiating bank transfer: {e}")
```

---

### **Verify Direct Integration Payment**

Call the `check_direct_payment_status` method to verify the payment status. 

### **Usage**

```python
transaction_ref = "unique_transaction_ref"
payment_method = "bank-transfer"

def verify_direct_payment(transaction_ref, payment_method):
    try:
        response = client.check_direct_payment_status(transaction_ref, payment_method)
        print(response)
    except APIError as e:
        print(f"An error occurred while verifying payment status: {e}")
```

---

## **USSD Payment**

USSD payment allows customers to pay using their phone without internet access. The endpoint generates a USSD code for the payment.

### **Usage**

```python
payment_data = {
   "amount": "1500",
   "paymentReference": "unique_transaction_ref",
   "customerName": "Sheden",
   "customerEmail": "shedenbright@gmail.com",
   "currency": "NGN",
   "paymentMethods": "ussd"
}

def ussd_transaction(payment_data):
    try:
        response = client.initiate_ussd_transaction(data=payment_data, bank_name="fcmb")
        print(response)
    except APIError as e:
        print(f"An error occurred while initiating USSD transaction: {e}")
```

Verify the payment using `check_direct_payment_status` as shown in the **Verify Direct Integration Payment** section.

---

## **Card Payment**

Card payment allows customers to pay with their debit or credit card. 

### **Encrypt Card Details**

Use the following function to encrypt card details before initiating the transaction:

```python
def encrypt_card(card_number, cvv, pin, expiry_date):
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_v1_5
    import base64
    import json

    # Load public key
    with open('key/rsa_public_key.pub', 'rb') as key_file:
        public_key_data = key_file.read()
    public_key = RSA.import_key(public_key_data)

    # Card details
    card_params = {
        'cvv': cvv,
        'pin': pin,
        'expiryDate': expiry_date,
        'pan': card_number
    }

    # Encrypt details
    cipher = PKCS1_v1_5.new(public_key)
    encrypted = cipher.encrypt(json.dumps(card_params).encode('utf-8'))
    return base64.b64encode(encrypted).decode('utf-8')
```

---

### **Initiate Card Transaction**

```python
data = {
   "card_number": "5123450000000008",
   "cvv": "100",
   "pin": "1234",
   "expiry_date": "0139",
   "transaction_reference": "ERCS|20241216191025|1734372625377"
}

encrypted_payload = encrypt_card(
    card_number=data["card_number"],
    cvv=data["cvv"],
    pin=data["pin"],
    expiry_date=data["expiry_date"]
)

def initiate_card_transaction(encrypted_payload, transaction_ref):
    try:
        response = client.initiate_card_transaction(payload=encrypted_payload, transaction_ref=transaction_ref)
        print(response)
    except APIError as e:
        print(f"An error occurred while initiating card transaction: {e}")
```

---

## **OTP Management**

### **Submit OTP**

```python
def submit_otp(otp, transaction_ref, gateway_ref):
    try:
        response = client.submit_otp(otp, transaction_ref, gateway_ref)
        print(response)
    except APIError as e:
        print(f"An error occurred while submitting OTP: {e}")
```

### **Resend OTP**

```python
def resend_otp(transaction_ref, gateway_ref):
    try:
        response = client.resend_otp(transaction_ref, gateway_ref)
        print(response)
    except APIError as e:
        print(f"An error occurred while resending OTP: {e}")
```

---

## **Utilities**

### **Get Supported Banks**

Fetch the list of supported banks:

```python
banks = client.get_bank_list()
print(banks)
```

---

## **Cancel Transaction**

To cancel a transaction that has not been completed:

```python
client.cancel_transaction(transaction_ref="transaction_reference")
```

---

**Developed by:** Shedenbright  
**Contact:** [shedenbright@gmail.com](mailto:shedenbright@gmail.com)  
**Resume:** [sheden-resume.netlify.app](https://sheden-resume.netlify.app)
```