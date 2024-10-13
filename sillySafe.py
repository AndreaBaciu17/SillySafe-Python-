# Date: 10/7/24
# Name: SillySafe (Python)
# Author: Andrea B.
# Contact: baciuandrea04@gmail.com
# Description: This was a password hiding tool I made (that isn't too secure) that taught me to learn about the Fernet encryption module

#import to encript text
from cryptography.fernet import Fernet
import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# ENCRIPTS PIN
    
    
# function that creates password key to encript
def create_passkey():
    sillySafe_key = Fernet.generate_key()
    with open("sillySafe_key.key", "wb") as sillySafe_key_file:
        sillySafe_key_file.write(sillySafe_key)
    return sillySafe_key

if not os.path.exists("sillySafe_key.key"):
    create_passkey()

#function that retrieves key and loads password
def retreive_passkey():
    with open("sillySafe_key.key", "rb") as sillySafe_key_file:
        sillySafe_key = sillySafe_key_file.read()
    return sillySafe_key

# Function to derive key from PIN
def derive_PIN_key(PIN):
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm = hashes.SHA256(),
        length = 32,
        # CONSTANTS
        salt = salt,
        iterations = 10000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(PIN))
    return key

# DISPLAYS PROGRAM
def check_PIN():
    return input("1. Enter PIN: ")

# Calling functions to derive keys
sillySafe_key = retreive_passkey() # set call function to variable
PINcheck_key = check_PIN().encode() #convert password into key by bytes
derive_PIN_key(PINcheck_key) # set call function to another function
initialize_Fernet = Fernet(sillySafe_key)  # Initialize the Fernet module

# opens the existing passwords stored in file
def view():
    with open('Passwords.txt', 'r') as passwords_file:
        for line in passwords_file.readlines():
            lines = line.rstrip()  # strips character returns like \n, \t, etc
            if lines:  # Check if the line is not empty
                parts = lines.split(",")  # Split the line by comma
                if len(parts) == 2:  # Ensure there are exactly two parts to unpack
                    user_element1, new_password_element2 = parts
                    print("Username: ", user_element1, "\nPassword: ", initialize_Fernet.decrypt(new_password_element2.encode()).decode())
                else:
                    print(lines)  # Handle lines that don't have 2 values


# add new password into new text file if password doesn to already exist
def add():
    # get user info
    user = input("Username: ")
    new_password = input("Password: ")

    # create or open file to add password
    with open("Passwords.txt", 'a') as passwords_file: # 'with' function automatically closes file after execution of options, using 'a' mode, or appending the file
        # then, add user into into 'account'
        passwords_file.write("\n\nUsername Key: " + user + "\n")
        passwords_file.write("Password Key: " + initialize_Fernet.encrypt(new_password.encode()).decode()) #takes bytes of string, decode the string instead of initializing

# DISPLAYS PROGRAM
if PINcheck_key:
    print("Access granted.\n")
    while True:
        options = input("2. Would you like to add a new password (add)?\n3. Or view previous account(view)? \n4. Press 'q' or enter to quit ").lower()
        if options in ("q", "", "4"):
            break
        if options in ("add", "a", "2"):
            add() #preforms add function made
        elif options in ("view", "v", "3"):
            view() #preforms view function made
        else:
            print("Invalid option.")
            continue
else:
    print("Incorrect PIN. Access denied.")
