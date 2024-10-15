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
    
# Step 1: function that creates password key to encript
# Updated to correctly generate PIN key by encript with 'salt' key
'''  
def create_passkey():
    sillySafe_key = Fernet.generate_key()
    with open("sillySafe_key.key", "wb") as sillySafe_key_file:
        sillySafe_key_file.write(sillySafe_key)
    return sillySafe_key

if not os.path.exists("sillySafe_key.key"):
    create_passkey()
'''
def load_or_generate_salt():
    if os.path.exists('salt_key.key'):
        with open('salt_key.key', 'rb') as salt_key_file:
            return salt_key_file.read()
    else:
        salt = os.urandom(16)
        with open('salt_key.key', 'wb') as salt_key_file:
            salt_key_file.write(salt)
        return salt


# Step 2: Function to derive 'salt' key from PIN key
# Updated without salt key, devoted to own function
def derive_PIN_key(PIN, salt):
    # salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm = hashes.SHA256(),
        length = 32,
        # CONSTANTS
        salt = salt,
        iterations = 10000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(PIN.encode()))
    return key


# Step 3: Function to create a new PIN key and store the derived 'salt' key
def create_PIN():
    new_PIN = input("1. Enter new PIN: ")
    confirm_new_PIN = input("Confirm new PIN: ")

    # Retry if PIN confirmation does not match
    if new_PIN != confirm_new_PIN:
        print("PIN confirmation does not match. Retry. ")
        return create_PIN()
    else:
        print("\nNew PIN successful.\n")
    
    # calls 'salt' and 'PIN' key functions
    salt = load_or_generate_salt()
    PINcheck_key = derive_PIN_key(new_PIN, salt)

    with open('sillySafe_key.key', 'wb') as salt_key_file:
        salt_key_file.write(PINcheck_key)
    return PINcheck_key


# Step 4: function that retrieves key and loads password
# Updated to check existance of sillySafe key and calls 'create_PIN' function
def retreive_sillySafe_key():
    if not os.path.exists('sillySafe_key.key'):
        return create_PIN() #calls function
    with open('sillySafe_key.key', 'rb') as sillySafe_key_file:
        return sillySafe_key_file.read()


# Step 5: checks created PIN or create a new PIN if non-existant
def check_PIN(salt, create_PIN_run = False):
    if create_PIN_run:
        return True
    
    entered_PIN = input("1. Enter PIN: ")
    # Updated to call PIN and sillySafe keys
    PINcheck_key = derive_PIN_key(entered_PIN, salt)
    stored_sillySafe_key = retreive_sillySafe_key()

    # Updated to compare if user enters correct PIN
    if stored_sillySafe_key == PINcheck_key:
        return True
    else:
        return False

'''
# Calling functions to derive keys
# Abandoned to call 'retreive_sillySafe_key' in 'check_PIN' function
sillySafe_key = retreive_passkey() # set call function to variable
# Abandoned to call 'check_PIN' in main program
PINcheck_key = check_PIN().encode() #convert password into key by bytes
# Abandoned to call 'derive_PIN_key' for the 'new_PIN' in 'create_PIN' function and for the 'entered_PIN' in 'check_PIN' function
derive_PIN_key(PINcheck_key) # set call function to another function
# Abandoned to call Fernet through "main program
initialize_Fernet = Fernet(sillySafe_key)  # Initialize the Fernet module
'''

#  ENCRIPTS ACCOUNT PASSWORDS


# Step 1: add new password into new text file if password doesn to already exist
def add(initialize_Fernet):
    new_user = input("Username: ")
    new_password = input("Password: ")

    encrypted_password = initialize_Fernet.encrypt(new_password.encode()).decode()

    with open('Passwords.txt', 'a') as Passwords_txt_file:
        Passwords_txt_file.write(f"{new_user},{encrypted_password}\n")
    
    print(f"Account for {new_user} added successfully.\n")


# Step 2: opens the existing passwords stored in file
def view(initialize_fernet):
    # execute if 'Passwords.txt' file is empty or non-existant
    if not os.path.exists('Passwords.txt') or os.stat('Passwords.txt').st_size == 0:
        print("No passwords found.")
        return
    
    with open('Passwords.txt', 'r') as Passwords_txt_file:
        for line in Passwords_txt_file.readlines():
            lines = line.rstrip()  # strips character returns like \n, \t, etc
            if lines:  # Check if the line is not empty
                parts = lines.split(",")  # Split the line by comma
                if len(parts) == 2:  # Ensure there are exactly two parts to unpack
                    user_element1, password_element2 = parts
                    decrypted_password = initialize_fernet.decrypt(password_element2.encode()).decode()
                    print("\nUsername: " + user_element1 + "\nPassword: " + decrypted_password + "\n")
                else:
                    print(lines)  # Handle lines that don't have 2 values


# DISPLAYS MAIN PROGRAM

while True:
    salt = load_or_generate_salt() # calls 'salt' key

    if os.path.exists('sillySafe_key.key'):
        if check_PIN(salt):
            print("Access granted.\n")
        else:
            print("Incorrect PIN. Access denied.")
            break
    else:
        print("No existing PIN found. Create PIN now:\n")
        # calls function to execute step 4 and step 5 of encripting PIN
        retreive_sillySafe_key()
        check_PIN(salt, create_PIN_run = True)

    # calls 'sillySafe' key and initializes Fernet
    stored_sillySafe_key = retreive_sillySafe_key()
    initialized_Fernet = Fernet(stored_sillySafe_key)
    
    # Main menu
    while True:
        options = input("2. Would you like to add a new password (add)?\n3. Or view previous account(view)? \n4. Press 'q' or enter to quit: ").lower()
        if options in ("q", "", "4"):
            break
        elif options in ("add", "a", "2"):
            add(initialized_Fernet) #preforms add function made, updated to have Fernet parameter initialized
        elif options in ("view", "v", "3"):
            view(initialized_Fernet) #preforms view function made, updated to have Fernet parameter initialized
        else:
            print("Invalid option.")
            continue
