# Date: 10/7/24
# Name: SillySafe (Python)
# Author: Andrea B.
# Contact: baciuandrea04@gmail.com
# Description: This was a password hiding tool I made (that isn't too secure) that taught me to learn about the Fernet encryption module

#import to encript text
from cryptography.fernet import Fernet

# Encripts password

'''
# function that creates password key to encript
def create_passkey():
    sillySafe_key = Fernet.generate_key()
    with open("sillySafe_key.key", "wb") as sillySafe_key_file:
        sillySafe_key_file.write(sillySafe_key)
create_passkey()
'''

#function that retrieves key and loads password
def retreive_passkey():
    sillySafe_key_file = open("sillySafe_key.key", "rb")
    sillySafe_key = sillySafe_key_file.read()
    sillySafe_key_file.close()
    return sillySafe_key


PIN_key = input("1. Enter PIN: ")

sillySafe_key = retreive_passkey() + PIN_key.encode() #convert password into key by bytes
initialize_Fernet = Fernet(sillySafe_key) #initializes the Fernet module

    

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


# Displays program
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
