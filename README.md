# SecureMessage: Python Encryption and Decryption

SecureMessage encrypts and decrypts one-line text messages using a password. It uses AES-256-GCM to keep messages private and detect changes to encrypted data.

## Files

- `secure_message.py` — Python source code
- `requirements.txt` — required Python package
- `SecureMessage-Python.exe` — Windows application

## How the algorithm works

1. The program generates a random salt and nonce for each message.
2. PBKDF2-HMAC-SHA-256 turns the password and salt into a 256-bit key.
3. AES-GCM encrypts the message and adds an authentication tag.
4. The version number, salt, nonce, and encrypted data are combined into Base64 text.
5. During decryption, the program checks the authentication tag. A wrong password or changed data produces an error.

The `cryptography` library handles the complex encryption operations. The Python code handles input, output, formatting, and errors. The password is never stored in the encrypted message.

## Run the Windows application

Download `SecureMessage-Python.exe` and double-click it. No separate Python installation is needed.

1. Enter `E` to encrypt or `D` to decrypt.
2. Enter a one-line message or paste the complete encrypted Base64 text.
3. Enter the password.
4. Read the `Encrypted:` or `Decrypted:` result.

Use the same password for encryption and decryption. Share the password separately from the encrypted message.

## Run from Python source

Install Python 3.9 or newer. In a terminal inside the project folder, run:

```text
python -m pip install -r requirements.txt
python secure_message.py
```

## Sample input and output

Encryption:

```text
Choose E to encrypt or D to decrypt: E
Message: Hello, class!
Password: correct horse battery staple
Encrypted: AfSEwukkoOWB33yZtcdFENUev5ezvMIJHZau8wxvepVAcqofpvNzhqLw02EPPaPvvbeORiu7U430Ow==
```

Decryption of that exact result:

```text
Choose E to encrypt or D to decrypt: D
Encrypted Base64: AfSEwukkoOWB33yZtcdFENUev5ezvMIJHZau8wxvepVAcqofpvNzhqLw02EPPaPvvbeORiu7U430Ow==
Password: correct horse battery staple
Decrypted: Hello, class!
```

A new encryption of the same message will produce different Base64 text because the salt and nonce are random.

## Error handling

The program reports invalid menu choices, empty passwords, malformed Base64 text, incomplete messages, unsupported versions, wrong passwords, changed encrypted data, and cancelled input.
