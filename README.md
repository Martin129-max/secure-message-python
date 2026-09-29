# SecureMessage: Encryption and Decryption Project

## Introduction and background

SecureMessage protects short text messages with **AES-256-GCM**, a standard authenticated encryption algorithm. Encryption makes the message unreadable without the password. Authentication detects a wrong password or changes to the encrypted data. The program is written in Java and uses only the standard Java library.

## Real-world application

The same kind of authenticated encryption is used to protect private data in applications, backups, and network services. This classroom program demonstrates the core method for one-line messages. For real deployment, use a reviewed application with a suitable password policy, secure password sharing, and a tested backup and recovery process.

## Algorithm and code breakdown

1. `encrypt` generates a fresh random **16-byte salt** and **12-byte IV** for every message. Even if the message and password repeat, the encrypted output changes.
2. `deriveKey` uses **PBKDF2-HMAC-SHA-256** with **200,000 iterations** to turn the password and salt into a 256-bit AES key. This makes password guessing more costly, although a weak password remains vulnerable.
3. AES-GCM encrypts the UTF-8 message and adds a **128-bit authentication tag**. The tag makes unauthorized changes detectable.
4. The program combines a one-byte format version, salt, IV, ciphertext, and tag, then converts the result to Base64 so it can be copied as text. The salt and IV are public; the password and derived key are not included.
5. `decrypt` decodes the Base64 text, validates its length and version, derives the same key, then checks the tag while decrypting. A wrong password or changed data produces an error.

The key derivation and authenticated encryption are the more complex parts of the program. Java's standard cryptography library performs them; the program handles input, output, formatting, and errors.

### Error handling

- Invalid menu choice: asks for `E` or `D`.
- Empty password: reports that a nonempty password is required.
- Invalid Base64, truncated data, or unsupported version: reports an input error.
- Wrong password or altered ciphertext: reports that decryption failed.
- Unexpected end of input or unavailable cryptography support: reports an error without printing a stack trace.

## How to run

**Requirement:** Java 8 or newer. On Windows, double-click **Run SecureMessage.bat**. On other systems, open a terminal in this folder and run `java -jar SecureMessage.jar`.

1. Enter `E` to encrypt or `D` to decrypt.
2. For `E`, enter one line of ordinary text. For `D`, paste the complete Base64 text from a previous encryption.
3. Enter the password. On a normal terminal it is hidden; in some development consoles it may be visible.
4. Copy the `Encrypted:` output to share or save. The receiver runs the program with `D` and enters the same password to get `Decrypted:` output. Share the password through a separate trusted channel.

The program accepts one-line messages. Base64 output varies on each encryption because the salt and IV are random.

## Sample input and output

Encryption example:

```text
Choose E to encrypt or D to decrypt: E
Message: Hello, class!
Password: correct horse battery staple
Encrypted: AePUBeO6CIQi9E9bAvQoualhTif6KkKoujB/kK0uAiBj8HAkQJWpAtBCtsDJGh8HU9XAadl0ZSyWyA==
```

The password line may appear as `Password (visible in this terminal):` in consoles that cannot hide input. A new encryption of the same message will produce different Base64 text.

Decryption of that exact sample:

```text
Choose E to encrypt or D to decrypt: D
Encrypted Base64: AePUBeO6CIQi9E9bAvQoualhTif6KkKoujB/kK0uAiBj8HAkQJWpAtBCtsDJGh8HU9XAadl0ZSyWyA==
Password: correct horse battery staple
Decrypted: Hello, class!
```

Wrong-password example:

```text
Error: wrong password or encrypted data was changed.
```

## Build from source

With a JDK installed, run `javac --release 8 SecureMessage.java`, then `jar --create --file SecureMessage.jar --main-class SecureMessage SecureMessage.class`. The included JAR is already built. The launcher needs Java installed; it is not a standalone native `.exe`.

## Learning and insights from each member

Complete these with each member's **own** work and reflection before submission:

| Member | Contribution | Learning or insight | Challenge and how it was resolved |
|---|---|---|---|
| Name 1 |  |  |  |
| Name 2 |  |  |  |
| Name 3 |  |  |  |

## Peer rating

Agree on a scale with your instructor, then fill this out individually:

| Reviewer | Member rated | Contribution rating | Communication rating | Evidence or comment |
|---|---|---|---|---|
|  |  |  |  |  |
|  |  |  |  |  |

Do not invent ratings for classmates; each reviewer should provide their own assessment.
