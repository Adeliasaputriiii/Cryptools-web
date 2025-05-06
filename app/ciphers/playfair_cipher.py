class PlayfairCipher:
    def __init__(self, key, plaintext=None, ciphertext=None):
        if not key:
            raise ValueError("Key tidak boleh kosong.")
        
        self.key = self.to_lowercase(self.remove_spaces(key))
        self.plaintext = self.to_lowercase(self.remove_spaces(plaintext)) if plaintext else ''
        self.ciphertext = self.to_lowercase(self.remove_spaces(ciphertext)) if ciphertext else ''
        self.key_table = []
        self.result = ''

    def to_lowercase(self, text):
        return text.lower()

    def remove_spaces(self, text):
        return ''.join(c for c in text if c != ' ')

    def generate_key_table(self):
        n = len(self.key)
        hash_map = [0] * 26

        for char in self.key:
            if char != 'j':
                hash_map[ord(char) - 97] = 2

        hash_map[ord('j') - 97] = 1

        i = j = 0
        self.key_table = [['' for _ in range(5)] for _ in range(5)]

        for k in range(n):
            if hash_map[ord(self.key[k]) - 97] == 2:
                hash_map[ord(self.key[k]) - 97] -= 1
                self.key_table[i][j] = self.key[k]
                j += 1
                if j == 5:
                    i += 1
                    j = 0

        for k in range(26):
            if hash_map[k] == 0:
                self.key_table[i][j] = chr(k + 97)
                j += 1
                if j == 5:
                    i += 1
                    j = 0

    def search(self, a, b):
        arr = [0] * 4
        if a == 'j':
            a = 'i'
        if b == 'j':
            b = 'i'

        for i in range(5):
            for j in range(5):
                if self.key_table[i][j] == a:
                    arr[0], arr[1] = i, j
                elif self.key_table[i][j] == b:
                    arr[2], arr[3] = i, j
        return arr

    def prepare(self, text):
        if len(text) % 2 != 0:
            text += 'z'
        return text

    def encrypt(self):
        if not self.plaintext:
            raise ValueError("Plaintext tidak boleh kosong untuk proses enkripsi.")

        self.generate_key_table()
        self.plaintext = self.prepare(self.plaintext)
        result = []
        n = len(self.plaintext)

        for i in range(0, n, 2):
            arr = self.search(self.plaintext[i], self.plaintext[i + 1])
            if arr[0] == arr[2]:  # same row
                result.append(self.key_table[arr[0]][(arr[1] + 1) % 5])
                result.append(self.key_table[arr[0]][(arr[3] + 1) % 5])
            elif arr[1] == arr[3]:  # same column
                result.append(self.key_table[(arr[0] + 1) % 5][arr[1]])
                result.append(self.key_table[(arr[2] + 1) % 5][arr[1]])
            else:  # rectangle
                result.append(self.key_table[arr[0]][arr[3]])
                result.append(self.key_table[arr[2]][arr[1]])

        self.result = ''.join(result)
        return self.result

    def decrypt(self):
        if not self.ciphertext:
            raise ValueError("Ciphertext tidak boleh kosong untuk proses dekripsi.")

        self.generate_key_table()
        result = []
        n = len(self.ciphertext)

        for i in range(0, n, 2):
            arr = self.search(self.ciphertext[i], self.ciphertext[i + 1])
            if arr[0] == arr[2]:  # same row
                result.append(self.key_table[arr[0]][(arr[1] - 1 + 5) % 5])
                result.append(self.key_table[arr[0]][(arr[3] - 1 + 5) % 5])
            elif arr[1] == arr[3]:  # same column
                result.append(self.key_table[(arr[0] - 1 + 5) % 5][arr[1]])
                result.append(self.key_table[(arr[2] - 1 + 5) % 5][arr[1]])
            else:  # rectangle
                result.append(self.key_table[arr[0]][arr[3]])
                result.append(self.key_table[arr[2]][arr[1]])

        self.result = ''.join(result)
        return self.result