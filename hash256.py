def custom_hash(data: str, block_size: int = 8, init_vector: int = 0x12345678) -> str:
    """
    Простая хеш-функция на основе XOR и блочного шифрования.

    :param data: Исходная строка для хеширования.
    :param block_size: Размер блока (в байтах).
    :param init_vector: Начальный вектор (IV) для хеширования.
    :return: Хеш в виде шестнадцатеричной строки.
    """
    # Преобразуем данные в байты
    data_bytes = data.encode('utf-8')

    # Инициализируем хеш начальным вектором
    hash_value = init_vector

    # Разделяем данные на блоки
    for i in range(0, len(data_bytes), block_size):
        block = data_bytes[i:i + block_size]

        # Дополняем блок до размера block_size
        if len(block) < block_size:
            block = block.ljust(block_size, b'\x00')

        # Преобразуем блок в целое число
        block_int = int.from_bytes(block, byteorder='big')

        # Хеширование: XOR и циклический сдвиг
        hash_value ^= block_int
        hash_value = ((hash_value << 3) | (hash_value >> (32 - 3))) & 0xFFFFFFFF

    # Возвращаем хеш в шестнадцатеричной строке
    return f"{hash_value:08x}"


input_data = input("Введите строку для хеширования: ")
hash_result = custom_hash(input_data)
print(f"Хеш строки: {hash_result}")