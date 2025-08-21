import base64

# Predefined key for XOR operations (as a constant integer value)
XOR_KEY = 599914492823  # Example key, ensure it's consistent across both functions

def int_to_base36(num: int) -> str:
    """Convert an integer to a Base36 encoded string."""
    chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if num == 0:
        return chars[0]
    base36 = []
    while num:
        num, i = divmod(num, 36)
        base36.append(chars[i])
    return ''.join(reversed(base36))

def base36_to_int(base36: str) -> int:
    """Convert a Base36 encoded string back to an integer."""
    return int(base36, 36)

def encrypt_id(value: int) -> str:
    """Encrypt an integer ID into a 12-character alphanumeric string."""
    # XOR with the predefined key
    masked_value = value ^ XOR_KEY
    # Convert to Base36 for alphanumeric result
    encrypted_value = int_to_base36(masked_value)
    return encrypted_value.zfill(12)  # Pad to ensure exactly 12 characters

def decrypt_id(encrypted_value: str) -> int:
    """Decrypt a 12-character alphanumeric string back to the original integer ID."""
    # Convert from Base36 to integer
    masked_value = base36_to_int(encrypted_value)
    # XOR with the same key to retrieve the original value
    original_value = masked_value ^ XOR_KEY
    return original_value