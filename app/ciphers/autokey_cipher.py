class AutoKeyVigenereCipher:
    def __init__(self, key, plaintext=None, ciphertext=None):
        if not key:
            raise ValueError("Key tidak boleh kosong.")
        
        self.key = key.upper()
        self.plaintext = plaintext.upper() if plaintext else ''
        self.ciphertext = ciphertext.upper() if ciphertext else ''
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.result = ''

    def generate_keystream(self, text):
        return (self.key + text)[:len(text)]

    def encrypt(self):
        if not self.plaintext:
            raise ValueError("Plaintext tidak boleh kosong untuk proses enkripsi.")

        keystream = self.generate_keystream(self.plaintext)
        result = []

        for p_char, k_char in zip(self.plaintext, keystream):
            if p_char in self.alphabet:
                p_idx = self.alphabet.index(p_char)
                k_idx = self.alphabet.index(k_char)
                c_idx = (p_idx + k_idx) % 26
                result.append(self.alphabet[c_idx])
            else:
                result.append(p_char)

        self.result = ''.join(result)
        return self.result

    def decrypt(self):
        if not self.ciphertext:
            raise ValueError("Ciphertext tidak boleh kosong untuk proses dekripsi.")

        key = self.key
        result = []

        for c_char in self.ciphertext:
            if c_char in self.alphabet:
                k_char = key[0]
                k_idx = self.alphabet.index(k_char)
                c_idx = self.alphabet.index(c_char)
                p_idx = (c_idx - k_idx + 26) % 26
                p_char = self.alphabet[p_idx]
                result.append(p_char)
                key += p_char  # extend key with plaintext
                key = key[1:]  # remove first character
            else:
                result.append(c_char)

        self.result = ''.join(result)
        return self.result
