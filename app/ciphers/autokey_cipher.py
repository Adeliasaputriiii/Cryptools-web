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
    # Ambil hanya huruf A-Z dari text
        filtered_text = ''.join(c for c in text if c in self.alphabet)
        return (self.key + filtered_text)[:len(filtered_text)]

    def encrypt(self):
        if not self.plaintext:
            raise ValueError("Plaintext tidak boleh kosong untuk proses enkripsi.")

        result = []
        keystream_index = 0
        keystream = self.generate_keystream(self.plaintext)

        for p_char in self.plaintext:
            if p_char in self.alphabet:
                k_char = keystream[keystream_index]
                p_idx = self.alphabet.index(p_char)
                k_idx = self.alphabet.index(k_char)
                c_idx = (p_idx + k_idx) % 26
                result.append(self.alphabet[c_idx])
                keystream_index += 1

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
                key = key[1:]

        self.result = ''.join(result)
        return self.result