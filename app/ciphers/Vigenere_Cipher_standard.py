# Alfabet yang digunakan
alphabets = "abcdefghijklmnopqrstuvwxyz"

class VigenereCipher:
    def __init__(self, key: str, plaintext: str = "", ciphertext: str = "") -> None:
        if (plaintext != "" and ciphertext != ""):
            raise Exception("Either plaintext or ciphertext must be empty")
        if (plaintext == "" and ciphertext == ""):
            raise Exception("Either plaintext or ciphertext must be filled")
        if (key == ""):
            raise Exception("Key must be filled!")

        self.plaintext = plaintext
        if plaintext:
            self.plaintext = self.normalizeText(plaintext)

        self.ciphertext = ciphertext.lower()
        if ciphertext:
            self.ciphertext = self.normalizeText(ciphertext)

        key = key.lower()
        self.key = key
        if key:
            if self.plaintext:
                self.key = self.normalizeKey(self.plaintext, key)
            else:
                self.key = self.normalizeKey(self.ciphertext, key)

    def encrypt(self) -> str:
        if self.plaintext == "" or self.ciphertext != "":
            raise Exception("Plaintext must be filled and ciphertext must be empty")

        ciphertext = ""
        for p, k in zip(self.plaintext, self.key):
            ciphertext += alphabets[(alphabets.find(p) + alphabets.find(k)) % 26]

        self.ciphertext = ciphertext
        return ciphertext.upper()

    def decrypt(self) -> str:
        if self.plaintext != "" and self.ciphertext == "":
            raise Exception("Plaintext must be empty and ciphertext must be filled")

        plaintext = ""
        for c, k in zip(self.ciphertext, self.key):
            plaintext += alphabets[(alphabets.find(c) - alphabets.find(k)) % 26]

        self.plaintext = plaintext
        return plaintext

    @staticmethod
    def generateBasicVigenereTable() -> list[str]:
        table = []
        for i in range(26):
            row = alphabets[i:] + alphabets[:i]
            table.append(row)
        return table

    @staticmethod
    def normalizeText(text: str) -> str:
        return "".join(filter(str.isalpha, text)).lower()

    @staticmethod
    def normalizeKey(text: str, key: str) -> str:
        key = "".join(filter(str.isalpha, key)).lower()
        return (key * (len(text) // len(key) + 1))[:len(text)]

    # Opsional: jika ingin tetap menyimpan fungsi acak tanpa random
    @staticmethod
    def generateRandomVigenereTable() -> list[str]:
        raise NotImplementedError("Fungsi random di-nonaktifkan karena tidak boleh menggunakan modul 'random'.")
