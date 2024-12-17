import string
import pandas as pd

def generate_row() -> str:
    """Generates a row for the Vigenère table.\n

    Returns:
        str: A string containing letters, digits, special characters, whitespace, and letters with diacritics.
    """

    letters = string.ascii_letters
    digits = string.digits
    special_characters = string.punctuation
    whitespace = string.whitespace
    unicode_characters = "ÀÁÂÃÄÅàáâãäåÈÉÊËèéêëÌÍÎÏìíîïÒÓÔÕÖØòóôõöøÙÚÛÜùúûüÝŸýÿ"

    return letters + digits + special_characters + whitespace + unicode_characters



def generate_table(row: str, public_key: str) -> pd.DataFrame:
    """Generates a Vigenère table.\n

    Args:
        row (str): the row to be used in the table.
        public_key (str): the public key to be used in the table.

    Returns:
        pd.DataFrame: the Vigenère table.
    """

    row_no_dupe = "".join(dict.fromkeys(row))
    public_key_no_dupe = "".join(dict.fromkeys(public_key))

    row_without_key = "".join([char for char in row_no_dupe if char not in public_key_no_dupe])

    

    df_row = list(public_key_no_dupe + row_without_key)

    df = pd.DataFrame(columns=list(df_row), index=list(df_row))

    # Create the first row
    df.loc[df_row[0]] = df_row

    # Create the following rows
    for i in range(1, len(row)):
        df_row = df_row[1:] + df_row[:1]

        df.loc[
            df.index.tolist()[i]
        ] = df_row


    print(df)

    return df



def vigenere_encode(row: str, message: str, public_key: str, private_key: str) -> str:
    """Encodes a message using the Vigenère cipher.\n

    Args:
        row (str): the row to be used in the table.
        message (str): the message to be encoded.
        public_key (str): the public key to be used in the table.
        private_key (str): the private key to be used in the table.

    Returns:
        str: the encoded message.
    """

    table = generate_table(row, public_key)
    encoded_message = ""

    # Ensure len(private_key) is at least len(message)
    private_key = (private_key * ((len(message) // len(private_key)) + 1))[:len(message)]

    for m,k in zip(message, private_key):
        encoded_message += table.loc[m][k]
    
    return encoded_message



def vigenere_decode(row: str, encoded_message: str, public_key: str, private_key: str) -> str:
    """Decodes a message using the Vigenère cipher.\n

    Args:
        row (str): the row to be used in the table.
        encoded_message (str): the message to be decoded.
        public_key (str): the public key to be used in the table.
        private_key (str): the private key to be used in the table.

    Returns:
        str: the decoded message.
    """
    
    table = generate_table(row, public_key)

    decoded_message = ""

    # Ensure len(private_key) is at least len(encoded_message)
    private_key = (private_key * ((len(encoded_message) // len(private_key)) + 1))[:len(encoded_message)]

    for m,k in zip(encoded_message, private_key):
        # Find the column (public_key) and look for the original row (message character)
        decoded_message += table[table[k] == m].index[0]
    
    return decoded_message

# Code by NilsMT on GitHub