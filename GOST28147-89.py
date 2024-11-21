# Таблица подстановок (S-блоки) для ГОСТ 28147-89
SBOX = [
    [4, 10, 9, 2, 13, 8, 0, 14, 6, 11, 1, 12, 7, 15, 5, 3],
    [14, 11, 4, 12, 6, 13, 15, 10, 2, 3, 8, 1, 0, 7, 5, 9],
    [5, 8, 1, 13, 10, 3, 4, 2, 14, 15, 12, 7, 6, 0, 9, 11],
    [7, 13, 10, 1, 0, 8, 9, 15, 14, 4, 6, 12, 11, 2, 5, 3],
    [6, 12, 7, 1, 5, 15, 13, 8, 4, 10, 9, 14, 0, 3, 11, 2],
    [4, 11, 10, 0, 7, 2, 1, 13, 3, 6, 8, 5, 9, 14, 15, 12],
    [13, 11, 4, 1, 3, 15, 5, 9, 0, 10, 14, 7, 6, 8, 2, 12],
    [1, 15, 13, 0, 5, 7, 10, 4, 9, 2, 3, 14, 6, 11, 8, 12]
]


def substitute(value, sbox):
    result = 0
    for i in range(8):
        result |= (sbox[i][(value >> (4 * i)) & 0xF] << (4 * i))
    return result

#Шифрование блока
def encrypt_block(block, key, rounds=32):
    n1, n2 = block >> 32, block & 0xFFFFFFFF
    for i in range(rounds):
        subkey = key[i % 8]  # Циклический выбор ключа
        result = (n1 + subkey) % (2 ** 32)
        result = substitute(result, SBOX)
        result = ((result << 11) | (result >> (32 - 11))) & 0xFFFFFFFF  # Ротация на 11 бит
        n1, n2 = n2 ^ result, n1
    return (n2 << 32) | n1

#Расшифрование блока
def decrypt_block(block, key, rounds=32):
    n1, n2 = block >> 32, block & 0xFFFFFFFF
    for i in range(rounds - 1, -1, -1):
        subkey = key[i % 8]  # Циклический выбор ключа
        result = (n1 + subkey) % (2 ** 32)
        result = substitute(result, SBOX)
        result = ((result << 11) | (result >> (32 - 11))) & 0xFFFFFFFF  # Ротация на 11 бит
        n1, n2 = n2 ^ result, n1
    return (n2 << 32) | n1

def process_files(input_file, encrypted_file, decrypted_file, key):
    with open(input_file, "rb") as f:
        data = f.read()

    padding = 8 - (len(data) % 8)
    data += bytes([padding] * padding)

    encrypted_data = b""
    for i in range(0, len(data), 8):
        block = int.from_bytes(data[i:i + 8], byteorder="big")
        encrypted_block = encrypt_block(block, key)
        encrypted_data += encrypted_block.to_bytes(8, byteorder="big")

    with open(encrypted_file, "wb") as f:
        f.write(encrypted_data)

    decrypted_data = b""
    for i in range(0, len(encrypted_data), 8):
        block = int.from_bytes(encrypted_data[i:i + 8], byteorder="big")
        decrypted_block = decrypt_block(block, key)
        decrypted_data += decrypted_block.to_bytes(8, byteorder="big")

    decrypted_data = decrypted_data[:-decrypted_data[-1]]

    with open(decrypted_file, "wb") as f:
        f.write(decrypted_data)


if __name__ == "__main__":
    key = [0x12345678, 0x23456789, 0x34567890, 0x45678901,
           0x56789012, 0x67890123, 0x78901234, 0x89012345]

    input_file = "input.txt"
    encrypted_file = "encrypted.txt"
    decrypted_file = "decrypted.txt"
    process_files(input_file, encrypted_file, decrypted_file, key)