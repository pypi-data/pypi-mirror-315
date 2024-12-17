# int_encoder/__init__.py
#
#

from .config import INT_ENCODE_KEY, INT_ENCODED_MAX

####################################################################################################

# Internal flag to track if the values were validated
_validation_done = False

def _validate_config():
    """Validates that INT_ENCODE_KEY and INT_ENCODED_MAX are properly configured."""
    global _validation_done
    if not _validation_done:
        if INT_ENCODED_MAX % INT_ENCODE_KEY == 0:
            raise ValueError("INT_ENCODE_KEY must not divide INT_ENCODED_MAX without a remainder.")
        _validation_done = True

####################################################################################################

def encode(to_encode: int) -> int:
    """
    Encodes an integer using INT_ENCODE_KEY and INT_ENCODED_MAX.
    
    Args:
        to_encode (int): The integer to encode.
    
    Returns:
        int: The encoded integer.
    """
    _validate_config()
    int_encoded = (to_encode * INT_ENCODE_KEY) % INT_ENCODED_MAX
    return int_encoded

def decode(to_decode: int) -> int:
    """
    Decodes an encoded integer using INT_ENCODE_KEY and INT_ENCODED_MAX.
    
    Args:
        to_decode (int): The encoded integer to decode.
    
    Returns:
        int: The decoded integer.
    """
    _validate_config()
    try:
        key_inverse = pow(INT_ENCODE_KEY, -1, INT_ENCODED_MAX)
    except ValueError:
        raise ValueError("No modular inverse exists for the current values of INT_ENCODE_KEY and INT_ENCODED_MAX.")
    int_decoded = (to_decode * key_inverse) % INT_ENCODED_MAX
    return int_decoded
