import numpy as np

MOD = 256  # Menggunakan rentang ASCII byte

def parse_key(key_str):
    rows = key_str.strip().split('\n')
    matrix = [list(map(int, row.strip().split())) for row in rows]
    return np.array(matrix)

def mod_inv_matrix(matrix, modulus):
    det = int(round(np.linalg.det(matrix))) % modulus
    det_inv = pow(det, -1, modulus)
    adj = np.round(det * np.linalg.inv(matrix)).astype(int) % modulus
    return (det_inv * adj) % modulus

def prepare_text(text, size):
    data = text.encode('utf-8')
    if len(data) % size != 0:
        pad_len = size - (len(data) % size)
        data += bytes([0] * pad_len)
    return data

def encrypt_text(plaintext, key_str, format_mode='nospace'):
    key_matrix = parse_key(key_str)
    size = key_matrix.shape[0]
    data = prepare_text(plaintext, size)

    result = bytearray()
    for i in range(0, len(data), size):
        block = np.array(list(data[i:i+size]), dtype=int)
        encrypted = np.dot(key_matrix, block) % MOD
        result.extend(encrypted.astype(np.uint8))

    output = result.decode('latin1')
    if format_mode == 'grouped':
        output = ' '.join([output[i:i+5] for i in range(0, len(output), 5)])
    else:
        output = output.replace(' ', '')
    return output

def decrypt_text(ciphertext, key_str):
    key_matrix = parse_key(key_str)
    inv_matrix = mod_inv_matrix(key_matrix, MOD)
    data = ciphertext.replace(' ', '').encode('latin1')

    size = key_matrix.shape[0]
    result = bytearray()
    for i in range(0, len(data), size):
        block = np.array(list(data[i:i+size]), dtype=int)
        decrypted = np.dot(inv_matrix, block) % MOD
        result.extend(np.round(decrypted).astype(np.uint8))

    try:
        return result.decode('utf-8').rstrip('\x00')  # hapus padding null
    except UnicodeDecodeError:
        return result.decode('latin1').rstrip('\x00')