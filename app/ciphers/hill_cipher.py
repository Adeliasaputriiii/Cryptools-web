import numpy as np
import string

ALPHABET = string.ascii_uppercase
ALPHABET_SIZE = len(ALPHABET)

class HillCipher:
    def __init__(self, key_string):
        self.key_matrix = self.parse_key_matrix(key_string)
    
    def parse_key_matrix(self, key_string):
        try:
            rows = key_string.strip().split(',')
            matrix = []
            for row in rows:
                numbers = list(map(int, row.strip().split()))
                matrix.append(numbers)

            size = len(matrix)
            if any(len(r) != size for r in matrix):
                raise ValueError("Matrix harus berbentuk persegi, contoh: '3 3, 2 5'")
            return np.array(matrix)
        except Exception:
            raise ValueError("Format matrix salah. Gunakan format: '3 3, 2 5'")
    
    def text_to_numbers(self, text):
        return [ALPHABET.index(c) for c in text.upper() if c in ALPHABET]

    def numbers_to_text(self, numbers):
        return ''.join(ALPHABET[n % ALPHABET_SIZE] for n in numbers)

    def pad_text(self, text, size):
        pad_len = (-len(text)) % size
        return text + ('X' * pad_len)

    def encrypt(self, plain_text):
        size = self.key_matrix.shape[0]
        plain_text = self.pad_text(plain_text.upper().replace(" ", ""), size)
        plain_numbers = self.text_to_numbers(plain_text)
        cipher_numbers = []

        for i in range(0, len(plain_numbers), size):
            block = np.array(plain_numbers[i:i+size])
            encrypted = self.key_matrix.dot(block) % ALPHABET_SIZE
            cipher_numbers.extend(encrypted)

        return self.numbers_to_text(cipher_numbers)

    def decrypt(self, cipher_text):
        try:
            size = self.key_matrix.shape[0]
            cipher_numbers = self.text_to_numbers(cipher_text.upper())

            det = int(round(np.linalg.det(self.key_matrix))) % ALPHABET_SIZE
            det_inv = pow(det, -1, ALPHABET_SIZE)

            matrix_mod_inv = (
                det_inv * np.round(det * np.linalg.inv(self.key_matrix)).astype(int)
            ) % ALPHABET_SIZE

            plain_numbers = []
            for i in range(0, len(cipher_numbers), size):
                block = np.array(cipher_numbers[i:i+size])
                decrypted = matrix_mod_inv.dot(block) % ALPHABET_SIZE
                plain_numbers.extend(decrypted)

            return self.numbers_to_text(plain_numbers)
        except Exception:
            return "Dekripsi gagal. Pastikan matrix bisa diinvers dan input benar."
