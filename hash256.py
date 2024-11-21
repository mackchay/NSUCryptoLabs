import hashlib

def hash_file(file_path):
    """Создает SHA-256 хэш файла."""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def verify_files(original_file, decrypted_file):
    """Сравнивает хэши исходного и расшифрованного файлов."""
    original_hash = hash_file(original_file)
    decrypted_hash = hash_file(decrypted_file)

    print(f"Хэш оригинального файла:   {original_hash}")
    print(f"Хэш расшифрованного файла: {decrypted_hash}")

    if original_hash == decrypted_hash:
        print("Сообщение успешно расшифровано: файлы совпадают.")
        return True
    else:
        print("Ошибка: файлы не совпадают.")
        return False


if __name__ == "__main__":
    # Пути к файлам
    input_file = "input.txt"
    decrypted_file = "decrypted.txt"

    # Проверка
    verify_files(input_file, decrypted_file)