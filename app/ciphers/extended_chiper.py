class ExtendedVigenereCipher:
    """
    A class representing Extended Vigenere Cipher using 256 ASCII characters.

    Attributes:
    ----------
    plaintext : str
        Original text to encrypt or decrypted result.
    ciphertext : str
        Text to decrypt or encrypted result.
    key : str
        Key for encryption/decryption.
    """

    def __init__(self, key:str, plaintext: any ="", ciphertext:any="") -> None:
        """
        Constructor for VigenereCipher class. Either plaintext or ciphertext must be empty at 
        creation.

        Parameters
        ----------
        key : str
            Text you want to encrypt or ciphertext after decrypted.
        plaintext : str, optional
            Text you want to decrypt or plaintext after encrypted.
        cipherthex : int, optional
            Key for encrypting or decrypting a text.
        """
         # Input validation.
        if (plaintext != "" and ciphertext != ""):
            raise Exception("Either plaintext or ciphertext must be empty")
        if (plaintext == "" and ciphertext == ""):
            raise Exception("Either plaintext or ciphertext must be filled")
        if (key ==""):
            raise Exception("Key must be filled!")

        self.plaintext = plaintext
        self.ciphertext = ciphertext
        self.key = key
        if (key != ""):
            if (self.plaintext != ""):
                self.key = self.normalizeKey(self.plaintext, key)
            else:
                self.key = self.normalizeKey(self.ciphertext, key)

    @staticmethod
    def normalizeKey(text: str, key: str) -> str:
        """
         Method to normalize key by repeat the key until it have same length with text. 
        Text can be plaintext or ciphertext.

        Return the normalized key. 
        
        Parameters
        ----------
        text : str
            Normalized text (can be plaintext or ciphertext).
        key : str 
            Key you want to normalize
        """
        # Variable declaration.
        normalizedKey:str

        # Repeat key until it has same length with plaintext.
        normalizedKey = (key*(len(text)//len(key)+1))[:len(text)]
        return normalizedKey
    
    def encrypt(self) -> str:
        """
        Method to encrypt current plaintext with current key. Modify ciphertext attribute also
        
        Return the ciphertext. 

        """
      # Class validation. 
        if (self.plaintext == "" or self.ciphertext != ""):
            raise Exception("Plaintext must be filled and ciphertext must be empty")


        # Variable declaration.
        ciphertext:str = ""

        # Encrypt the plaintext. 
        for (p,k) in zip(self.plaintext, self.key):
            ciphertext = ciphertext + chr((ord(p) + ord(k)) % 256)
        
        self.ciphertext = ciphertext
        return ciphertext
    
    def encryptByte(self) -> bytes:
        if not isinstance(self.plaintext, (bytes, bytearray)):
            raise TypeError("Plaintext harus dalam bentuk bytes untuk mode byte.")

        key = self.key.encode() if isinstance(self.key, str) else self.key
        key_normalized = (key * ((len(self.plaintext) // len(key)) + 1))[:len(self.plaintext)]

        ciphertext = bytes((p + k) % 256 for p, k in zip(self.plaintext, key_normalized))
        self.ciphertext = ciphertext
        return ciphertext

    def decrypt(self) -> str:
        """
        Decrypt the ciphertext using Extended Vigenere Cipher.

        Returns:
        -------
        str
            The decrypted plaintext.
        """
        if not self.ciphertext or self.plaintext:
            raise Exception("Ciphertext must be filled and plaintext must be empty.")
        
        self.plaintext = "".join(
            chr((ord(c) - ord(k)) % 256) for c, k in zip(self.ciphertext, self.key)
        )
        return self.plaintext
    
    def decryptByte(self) -> bytes:
        if not isinstance(self.ciphertext, (bytes, bytearray)):
            raise TypeError("Ciphertext harus dalam bentuk bytes untuk mode byte.")

        key = self.key.encode() if isinstance(self.key, str) else self.key
        key_normalized = (key * ((len(self.ciphertext) // len(key)) + 1))[:len(self.ciphertext)]

        plaintext = bytes((c - k) % 256 for c, k in zip(self.ciphertext, key_normalized))
        self.plaintext = plaintext
        return plaintext