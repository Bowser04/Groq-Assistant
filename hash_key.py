from cryptography.fernet import Fernet
import base64
import os
import hashlib

# Set your API key
api_key = input("groq api key (https://console.groq.com/keys) : ")
# Set your password
password = input("enter a password for your api key: ")


# Generate a key from the password
password_key = hashlib.sha256(password.encode()).digest()
key = base64.urlsafe_b64encode(password_key)

# Encrypt the API key
f = Fernet(key)
encrypted_api_key = f.encrypt(api_key.encode())

# Store the encrypted API key in a file
with open("apikey", "wb") as file:
    file.write(encrypted_api_key)

# Remove sensitive variables from memory
password = None
api_key = None
password_key = None
key = None