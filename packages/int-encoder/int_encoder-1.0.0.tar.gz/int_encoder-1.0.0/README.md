# int_encoder

`int_encoder` is a Python library for encoding and decoding integers using modular arithmetic.

## Installation

To install the library from PyPI, simply run:

```bash
pip3 install int-encoder
```

## Configuration

The library uses two configuration constants, defined in `config.py`:

- `INT_ENCODE_KEY`: The key used for encoding and decoding integers.
- `INT_ENCODED_MAX`: The maximum value for the encoded integer.

These values can be modified in `config.py` to suit your needs.


## Usage

```python
import int_encoder

# Modify configuration constants (optional)
int_encoder.config.INT_ENCODE_KEY = 987654321  # New key for encoding
int_encoder.config.INT_ENCODED_MAX = 2 ** 16   # New maximum value for encoded integers

# Example usage
int_to_encode = 123456
encoded_value = int_encoder.encode(int_to_encode)
print(f"Encoded value: {encoded_value}")

decoded_value = int_encoder.decode(encoded_value)
print(f"Decoded value: {decoded_value}")
```
