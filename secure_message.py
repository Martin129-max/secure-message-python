"""Encrypt and decrypt one-line messages with a password and AES-256-GCM."""

import base64
import binascii
import getpass
import os
import sys

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


VERSION = 1
SALT_SIZE = 16
NONCE_SIZE = 12
KEY_SIZE = 32
ITERATIONS = 200_000
MIN_PACKET_SIZE = 1 + SALT_SIZE + NONCE_SIZE + 16  # Includes the GCM tag.


def make_key(password: str, salt: bytes) -> bytes:
    """Turn a password into a 256-bit key using PBKDF2-HMAC-SHA-256."""
    if not password:
        raise ValueError("Password cannot be empty.")
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=ITERATIONS,
    )
    return kdf.derive(password.encode("utf-8"))


def encrypt(message: str, password: str) -> str:
    """Return Base64 text containing version, salt, nonce, and ciphertext."""
    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)
    key = make_key(password, salt)
    encrypted = AESGCM(key).encrypt(nonce, message.encode("utf-8"), None)
    # security: never reuse a nonce with the same key; fresh salt and nonce are generated.
    packet = bytes([VERSION]) + salt + nonce + encrypted
    return base64.b64encode(packet).decode("ascii")


def decrypt(encoded: str, password: str) -> str:
    """Check the authentication tag, then return the original message."""
    try:
        packet = base64.b64decode(encoded.strip(), validate=True)
    except (binascii.Error, ValueError) as exc:
        raise ValueError("Encrypted message must be valid Base64.") from exc
    if len(packet) < MIN_PACKET_SIZE:
        raise ValueError("Encrypted message is incomplete.")
    if packet[0] != VERSION:
        raise ValueError("Unsupported encrypted message version.")
    salt = packet[1 : 1 + SALT_SIZE]
    nonce = packet[1 + SALT_SIZE : 1 + SALT_SIZE + NONCE_SIZE]
    encrypted = packet[1 + SALT_SIZE + NONCE_SIZE :]
    key = make_key(password, salt)
    try:
        return AESGCM(key).decrypt(nonce, encrypted, None).decode("utf-8")
    except (InvalidTag, UnicodeDecodeError) as exc:
        raise ValueError("Wrong password or encrypted data was changed.") from exc


def main() -> None:
    try:
        choice = input("Choose E to encrypt or D to decrypt: ").strip().upper()
        if choice not in {"E", "D"}:
            print("Error: enter E or D.")
            return
        prompt = "Message: " if choice == "E" else "Encrypted Base64: "
        message = input(prompt)
        password = (getpass.getpass("Password: ") if sys.stdin.isatty()
                    else input("Password (visible in this terminal): "))
        if choice == "E":
            print("Encrypted:", encrypt(message, password))
        else:
            print("Decrypted:", decrypt(message, password))
    except (EOFError, KeyboardInterrupt):
        print("\nInput cancelled.")
    except ValueError as exc:
        print("Error:", exc)


if __name__ == "__main__":
    main()
