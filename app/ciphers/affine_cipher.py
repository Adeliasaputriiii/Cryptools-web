class AffineCipher:
    def __init__(self, a, b, plaintext=None, ciphertext=None):
        if self.gcd(a, 26) != 1 or a == 1:
            raise ValueError("Kunci a harus coprime dengan 26 dan tidak boleh 1.")
        
        self.a = a
        self.b = b
        self.plaintext = plaintext
        self.ciphertext = ciphertext
        self.result = ""

    def gcd(self, a, b):
        while b != 0:
            a, b = b, a % b
        return a

    def mod_inverse(self, a, m):
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        raise ValueError("Modular inverse tidak ditemukan")

    def encrypt(self):
        if not self.plaintext:
            raise ValueError("Plaintext tidak boleh kosong untuk proses enkripsi.")

        result = ""
        for char in self.plaintext:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                pos = ord(char) - base
                encrypted = (self.a * pos + self.b) % 26
                result += chr(encrypted + base)
            else:
                result += char
        self.result = result
        return self.result

    def decrypt(self):
        if not self.ciphertext:
            raise ValueError("Ciphertext tidak boleh kosong untuk proses dekripsi.")

        result = ""
        a_inv = self.mod_inverse(self.a, 26)
        for char in self.ciphertext:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                pos = ord(char) - base
                decrypted = (a_inv * (pos - self.b)) % 26
                result += chr(decrypted + base)
            else:
                result += char
        self.result = result
        return self.result
