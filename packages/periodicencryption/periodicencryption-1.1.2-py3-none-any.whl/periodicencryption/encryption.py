import re
import periodicencryption.vigenerecipher as vc
import periodicencryption.element as el

def generate_keys(string: str) -> tuple[str, str]:
    """Generates public and private keys from a string.

    Args:
        string (str): The string to generate the keys from.

    Raises:
        ValueError: If the element list is empty.

    Returns:
        tuple[str, str]: The public and private keys.
    """

    element_list = el.turn_str_into_el(string)

    if len(element_list) == 0:
        raise ValueError("Element list cannot be empty.")

    first_element = element_list[0]
    last_element = element_list[-1]

    # public key : last element mass + 1st element name + last element name + 1st element mass
    public_key = str(last_element.mass) + first_element.name.capitalize() + last_element.name.capitalize() + str(first_element.mass)
    # private key : 1st element name + last element symbol + 1st element symbol + last element name
    private_key = first_element.name.capitalize() + last_element.symbol + first_element.symbol + last_element.name.capitalize()

    return public_key, private_key

def encrypt_keys_manual(row: str, message: str, public_key: str, private_key: str) -> str:
    """Encrypts a message using the Vigenère cipher and the periodic table elements, with the specified keys.

    Args:
        row (str): the row of characters to use (i.e. which characters are allowed to be encrypted, like "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        message (str): the message to encrypt
        public_key (str): the public key
        private_key (str): the private key

    Raises:
        ValueError: If the message is empty.

    Returns:
        str: the encrypted message
    """
    
    if len(message) == 0:
        raise ValueError("Message cannot be empty.")
    
    # 1 - turn message into elements

    element_list = el.turn_str_into_el(message)

    # 2 - encode message using Vigenère cipher

    string_element = ''.join([e.symbol for e in element_list])

    encoded = vc.vigenere_encode(row, string_element,public_key, private_key)

    return encoded

def encrypt_keys_auto(row: str, message: str) -> tuple[str, str, str]:
    """Encrypts a message using the Vigenère cipher and the periodic table elements, with automatically generated keys.

    Args:
        row (str): the row of characters to use (i.e. which characters are allowed to be encrypted, like "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        message (str): the message to encrypt

    Raises:
        ValueError: If the message is empty.

    Returns:
        tuple[str, str, str]: the encrypted message, the public key, and the private key
    """   

    if len(message) == 0:
        raise ValueError("Message cannot be empty.")

    public_key, private_key = generate_keys(message)
    
    return encrypt_keys_manual(row, message, public_key, private_key), public_key, private_key


def decrypt(row: str, encoded: str, public_key: str, private_key: str) -> str:
    """Decrypts a message using the Vigenère cipher and the periodic table elements.

    Args:
        row (str): the row of characters to use (i.e. which characters are allowed to be encrypted, like "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        encoded (str): the encoded message
        public_key (str): the public key
        private_key (str): the private key

    Raises:
        ValueError: If the message is empty.

    Returns:
        str: the decrypted message
    """
    
    if len(encoded) == 0:
        raise ValueError("Message cannot be empty.")
    
    # 1 - decode message using Vigenère cipher

    decoded = vc.vigenere_decode(row, encoded, public_key, private_key)

    # 2 - turn elements into message

    sym_lst = re.findall(r'[A-Z][a-z]?\d*', decoded)

    #handle CounterElement
    for i, sym in enumerate(sym_lst):
        if sym == "Ct":
            sym_lst[i] = sym_lst[i] + sym_lst[i+1]
            sym_lst.pop(i+1)

    elements_list = [el.get_el_by_symbol(sym) for sym in sym_lst]

    message = el.turn_el_into_str(elements_list)

    return message

# Code by NilsMT on GitHub