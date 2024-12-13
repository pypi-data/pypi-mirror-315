# Altikrity - Python Encryption Library

Altikrity is a powerful library that provides multi-layer encryption techniques for securing Python code.

## Installation

To install Altikrity, use pip:

pip install altikrity


## Usage

### Encrypting Code

```python
from altikrity import encrypt_multiple_layers, decrypt_and_execute

# Encrypting your code
code = "print('Hello from encrypted code!')"
encrypted_code = encrypt_multiple_layers(code)

# Executing encrypted code
decrypt_and_execute(encrypted_code)
