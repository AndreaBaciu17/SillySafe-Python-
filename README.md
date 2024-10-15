# 🔒 SillySafe 🔒  
**Date:** 10/7/24  
**Author:** Andrea B.  
**Contact:** baciuandrea04@gmail.com

## Description  
SillySafe is a fun and easy-to-use password manager! Store your accounts behind a PIN key, and access them whenever needed. SillySafe helps you add new passwords, view your saved accounts, and ensures your data stays protected! 🔒

## Features  
- **PIN Protection:** Set up a custom PIN to lock your password vault, ensuring that only you can access your data.
- **Password Encryption:** All stored passwords are encrypted using the Fernet encryption module.
- **View and Add Accounts:** Easily add new passwords to your vault and view them whenever needed.

### Example Demo
```
1. Enter PIN: [user enters correct PIN to access accounts]

2. Would you like to add a new password (add)?
3. Or view previous account(view)?
4. Press 'q' or enter to quit
[User presses v or "view" to view]

Username Key: User1
Password Key: password1

# Password view in sillySafe_key.key file:
q7vFRb5Jt5vSNTRnL6Ud1r_Nw4mQvBS9BsIUOEZ8Dy4=

# Password view in Passwords.txt file:
Username Key: User1
Password Key: gAAAAABnBXMXA_exzkld7XyHB_gCa_fHLlzwckeW93WCoR4W0zzJ0BMjB_v
 ```

## How to Run the Code  
1. Clone the Repository:
 ```
   git clone https://github.com/AndreaBaciu17/SillySafe-Python.git
   cd SillySafe
 ```
2. Install the Cryptography Module:
 ```
   pip install cryptography
