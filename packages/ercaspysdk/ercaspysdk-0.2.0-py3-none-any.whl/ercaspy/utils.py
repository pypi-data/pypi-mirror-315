import requests
import platform
import socket
import locale
import datetime
import json
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Hash import SHA1

def get_device_details():
    """
    Generate device details
    """
    
    #user_agent = f"Python/{platform.python_version()} ({platform.system()}; {platform.machine()})"
    user_agent ="Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0; Touch)"

    # Get IP address 
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    # Language/Locale
    language = locale.getlocale()[0]

    # Timezone offset in minutes
    time_zone_offset = -int(datetime.datetime.now().astimezone().utcoffset().total_seconds() / 60)

    # Static screen details (replace with client-side data if needed)
    screen_width = 1920
    screen_height = 1080
    color_depth = 24


    device_details = {
       
            "payerDeviceDto": {
                "device": {
                    "browser": user_agent,
                    "browserDetails": {
                        "3DSecureChallengeWindowSize": "FULL_SCREEN",
                        "acceptHeaders": "application/json",
                        "colorDepth": color_depth,
                        "javaEnabled": True, 
                        "language": language,
                        "screenHeight": screen_height,
                        "screenWidth": screen_width,
                        "timeZone": time_zone_offset
                    },
                    "ipAddress": ip_address
                }
            }
        
    }
    return device_details








def encryptCard(card_number:str, cvv:str, pin:str, expiry_date:str):
    """
    Encrypt data
    """
    # Read the public key
    with open('key/rsa_public_key.pub', 'rb') as key_file:
        public_key_data = key_file.read()
    public_key = RSA.import_key(public_key_data)
    # Card details
    cardParams = {
        'cvv' : cvv,
        'pin' : pin,
        'expiryDate' : expiry_date,
        'pan' : card_number
    }
    # Convert card details to JSON
    cardJson = json.dumps(cardParams).encode('utf-8')
    # Encrypt the card details using PKCS1_v1_5 padding
    cipher = PKCS1_v1_5.new(public_key)
    encrypted = cipher.encrypt(cardJson)
    # Return the encrypted data as a Base64-encoded string
    return base64.b64encode(encrypted).decode('utf-8')


