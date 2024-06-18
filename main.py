# Import sys for system operations and colorama for colored output.
import sys
from colorama import init, Fore


init()



def vigenere_encrypt(plain_text, key):
    encrypted_text = ''


    key_repeated = (key * (len(plain_text) // len(key))) + key[:len(plain_text) % len(key)]

    for i in range(len(plain_text)):

        if plain_text[i].isalpha():

            shift = ord(key_repeated[i].upper()) - ord('A')


            if plain_text[i].isupper():
                encrypted_text += chr((ord(plain_text[i]) + shift - ord('A')) % 26 + ord('A'))
            else:
                encrypted_text += chr((ord(plain_text[i]) + shift - ord('a')) % 26 + ord('a'))
        else:

            encrypted_text += plain_text[i]


    return encrypted_text



def vigenere_decrypt(cipher_text, key):
    decrypted_text = ''


    key_repeated = (key * (len(cipher_text) // len(key))) + key[:len(cipher_text) % len(key)]


    for i in range(len(cipher_text)):

        if cipher_text[i].isalpha():

            shift = ord(key_repeated[i].upper()) - ord('A')


            if cipher_text[i].isupper():
                decrypted_text += chr((ord(cipher_text[i]) - shift - ord('A')) % 26 + ord('A'))
            else:
                decrypted_text += chr((ord(cipher_text[i]) - shift - ord('a')) % 26 + ord('a'))
        else:

            decrypted_text += cipher_text[i]


    return decrypted_text


key = "KEY"

plaintext = input('[!] Введите свое сообщение : ')

cipher_text = vigenere_encrypt(plaintext, key)


print(f"[+] Plaintext: {plaintext}")
print(f"{Fore.GREEN}[+] Ciphertext: {cipher_text}")


ask_to_decrypt = input('\n\n[?] Вы хотите расшифровать сообщение?\n[?] Да или Нет: ').lower()


if ask_to_decrypt == 'y':

    decrypted_text = vigenere_decrypt(cipher_text, key)
    print(f"{Fore.GREEN}[+] Decrypted text: {decrypted_text}")


elif ask_to_decrypt == 'n':
    sys.exit()

else:
    print(f"{Fore.RED}[-] Invalid input.")
