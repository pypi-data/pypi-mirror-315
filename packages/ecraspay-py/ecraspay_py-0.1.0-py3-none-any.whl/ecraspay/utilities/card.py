import json
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from typing import Union


def load_public_key(public_key: Union[str, bytes]) -> RSA.RsaKey:
    """
    Load a public key for RSA encryption.

    Args:
        public_key (Union[str, bytes]): The public key as a string, bytes, or a path to a .pub file.

    Returns:
        RSA.RsaKey: The RSA public key object.

    Raises:
        ValueError: If the provided public key format is invalid.

    Notes:
        - If a string is provided, the function first attempts to treat it as a file path.
        - If the file path is invalid, the function assumes the input is the key data itself.
        - If bytes are provided, they are decoded to a UTF-8 string.
    """
    if isinstance(public_key, str):
        try:
            # Attempt to load from file
            with open(public_key, "r") as key_file:
                key_data = key_file.read()
        except FileNotFoundError:
            # Treat the input as a direct key string
            key_data = public_key
    elif isinstance(public_key, bytes):
        key_data = public_key.decode("utf-8")
    else:
        raise ValueError(
            "Invalid public key format. Provide a string or a .pub file path."
        )

    return RSA.importKey(key_data)


def encrypt_card(
    card_number: str,
    expiration_date: str,
    cvv: str,
    pin: str,
    public_key: Union[str, bytes],
) -> str:
    """
    Encrypt card details using the provided RSA public key.

    Args:
        card_number (str): The card number (PAN) to be encrypted.
        expiration_date (str): The expiration date of the card in MM/YY format.
        cvv (str): The CVV security code of the card.
        pin (str): The PIN associated with the card.
        public_key (Union[str, bytes]): The RSA public key as a string,
        bytes, or file path.

    Returns:
        str: The encrypted card details as a Base64-encoded string.

    Raises:
        ValueError: If the public key format is invalid.

    Notes:
        - The card details are serialized into a JSON object before encryption.
        - RSA encryption is performed using the PKCS#1 v1.5 standard.
        - The encrypted data is Base64-encoded for safe transmission.
    """
    card_data = {
        "pan": card_number,
        "expiryDate": expiration_date,
        "cvv": cvv,
        "pin": pin,
    }

    card_json = json.dumps(card_data).encode("utf-8")
    rsa_public_key = load_public_key(public_key)

    cipher = PKCS1_v1_5.new(rsa_public_key)
    encrypted_data = cipher.encrypt(card_json)

    return base64.b64encode(encrypted_data).decode("utf-8")
