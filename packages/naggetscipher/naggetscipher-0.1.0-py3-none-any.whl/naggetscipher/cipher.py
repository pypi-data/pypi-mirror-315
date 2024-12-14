class NaggetsCipher:
    """
    Класс для шифрования и дешифрования текста с использованием шифра "Наггетс".
    """

    VOWELS = 'аеёиоуыэюяАЕЁИОУЫЭЮЯ'
    CIPHER_WORD = 'Наггетс'

    @staticmethod
    def is_vowel(char: str) -> bool:
        """
        Проверяет, является ли символ гласной буквой.

        :param char: Символ для проверки
        :return: True, если символ гласная, иначе False
        """
        return char in NaggetsCipher.VOWELS

    @classmethod
    def encrypt(cls, text: str) -> str:
        """
        Шифрует текст, добавляя "Наггетс" после каждой гласной буквы.

        :param text: Текст для шифрования
        :return: Зашифрованный текст
        """
        result = []
        for char in text:
            result.append(char)
            if cls.is_vowel(char):
                result.append(cls.CIPHER_WORD)
        return ''.join(result)

    @classmethod
    def decrypt(cls, text: str) -> str:
        """
        Дешифрует текст, удаляя "Наггетс" после каждой гласной буквы.

        :param text: Текст для дешифрования
        :return: Расшифрованный текст
        """
        result = []
        i = 0
        while i < len(text):
            result.append(text[i])
            if cls.is_vowel(text[i]):
                i += len(cls.CIPHER_WORD)
            i += 1
        return ''.join(result)

    @classmethod
    def encrypt_file(cls, input_file: str, output_file: str) -> None:
        """
        Шифрует содержимое файла и записывает результат в новый файл.

        :param input_file: Путь к входному файлу
        :param output_file: Путь к выходному файлу
        """
        with open(input_file, 'r', encoding='utf-8') as infile, \
             open(output_file, 'w', encoding='utf-8') as outfile:
            for line in infile:
                encrypted_line = cls.encrypt(line.strip())
                outfile.write(encrypted_line + '\n')

    @classmethod
    def decrypt_file(cls, input_file: str, output_file: str) -> None:
        """
        Дешифрует содержимое файла и записывает результат в новый файл.

        :param input_file: Путь к входному файлу
        :param output_file: Путь к выходному файлу
        """
        with open(input_file, 'r', encoding='utf-8') as infile, \
             open(output_file, 'w', encoding='utf-8') as outfile:
            for line in infile:
                decrypted_line = cls.decrypt(line.strip())
                outfile.write(decrypted_line + '\n')


# Пример использования
if __name__ == "__main__":
    original_text = "Привет, мир!"
    print(f"Оригинальный текст: {original_text}")

    encrypted_text = NaggetsCipher.encrypt(original_text)
    print(f"Зашифрованный текст: {encrypted_text}")

    decrypted_text = NaggetsCipher.decrypt(encrypted_text)
    print(f"Расшифрованный текст: {decrypted_text}")

    # Пример использования с файлами
    NaggetsCipher.encrypt_file("input.txt", "encrypted.txt")
    NaggetsCipher.decrypt_file("encrypted.txt", "decrypted.txt")