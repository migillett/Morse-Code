#!/usr/bin/python3

# Written by Michael Gillett, 2020
# github.com/gillettmi

# A simple morse code conversion program

import time
import winsound as ws
# import os

# output_file = os.path.join(os.getcwd(), 'output.txt')
encrypted_message = ''
encryption_key = 0

morse = {
    'a': '.-',      'b': '-...',    'c': '-.-.',
    'd': '-..',     'e': '.',       'f': '..-.',
    'g': '--.',     'h': '....',    'i': '..',
    'j': '.---',    'k': '-.-',     'l': '.-..',
    'm': '--',      'n': '-.',      'o': '---',
    'p': '.--.',    'q': '--.-',    'r': '.-.',
    's': '...',     't': '-',       'u': '..-',
    'v': '...-',     'w': '.--',     'x': '-..-',
    'y': '-.--',    'z': '--..',

    '1': '.----',   '2': '..---',   '3': '...---',
    '4': '....-',   '5': '.....',   '6': '-....',
    '7': '--...',   '8': '---..',   '9': '----.',
    '0': '-----',

    # '.': '.-.-.-',  ',': '--..--',  '?': '..--..',
    # '!': '-.-.--',  '&': '.-...',   ':': '---...',
    # ';': '-.-.-.',  '@': '.--.-.',  '$': '...-..-'
}

menu = '''
================================
      MORSE CODE GENERATOR
================================
1. Convert and Transmit
2. Convert, Encrypt, and Transmit
3. Deconvert Morse Message
4. Quit
'''

output = ''
errors = ''


def press_enter():
    input('Press enter to continue.')


def error(error_message):
    print(error_message)
    press_enter()


# PROGRAM BEGINS HERE
def morse_code(message, encrypt=False, key=0):
    # loop through each line in the message
    for line in message:

        # split the words sand save to line list
        line = line.split(' ')

        # convert each word in line list
        for word in line:
            for letter in list(word):
                # make each letter lowercase
                letter = letter.lower()

                # If encrypt == True : encrypt input
                if encrypt:
                    letter = chr((ord(letter) + key - 97) % 26 + 97)

                # convert the letter to morse and add to global output string
                if letter in morse:
                    global output
                    output += morse[letter] + ' '

                # if the character is unrecognized, print it
                else:
                    global errors
                    errors += letter
    # print all of the errors
    if errors != '':
        print('Unrecognized characters omitted: {0}'.format(errors))
    # write_file(output, output_file)
    transmit(output)


def decrypt_morse(m='', encrypted=False, decrypt_key=0):
    output_message = ''
    decrypted_message = ''
    morse_letters = m.split(' ')
    for letter in morse_letters:
        try:
            output_message += (list(morse.keys())[list(morse.values()).index(letter.lower())])
        except ValueError:
            print('Unable to convert letter:', letter)
            continue
    print('Your message:', output_message)
    # write_file(output_message, output_file)

    if encrypted:
        for l in output_message:
            decrypted_message += chr((ord(l) - decrypt_key - 97) % 26 + 97)
        print('Your decrypted message:', decrypted_message)
        # write_file(decrypted_message, output_file)


def write_file(message_output, save_location):
    # write output file
    with open(save_location, 'w') as o:
        o.write(message_output)


def transmit(input_morse, tempo=100, fq=600):
    print('Transmitting message:', input_morse)
    for t in input_morse:
        if t == '.':
            ws.Beep(fq, tempo)
        elif t == '-':
            ws.Beep(fq, tempo*3)
        else:
            time.sleep(tempo/250)
    print('\nTransmission complete')


if __name__ == '__main__':
    while True:
        print(menu)
        try:
            choice = input('Input:')
            choice = int(choice)
        except ValueError:
            error()

        # Convert input from text to morse code (no encryption)
        if choice == 1:
            input_message = input('Message:')
            morse_code(input_message)

        # Convert and encrypt input
        elif choice == 2:
            input_message = input('Message:')
            try:
                encryption_key = int(input('Encryption Key:'))
                morse_code(input_message, encrypt=True, key=encryption_key)
            except ValueError:
                error('Invalid input. Please input an integer for the Encryption Key.')

        # Decrypt input
        elif choice == 3:
            is_it_encrypted = str(input('Is the message encrypted? (Y/N)'))
            is_it_encrypted = is_it_encrypted.lower()
            if is_it_encrypted == 'y':
                try:
                    encryption_key = int(input('Encryption Key:'))
                    encrypted_message = input('Message:')
                    try:
                        decrypt_morse(m=encrypted_message, encrypted=True, decrypt_key=encryption_key)
                    except ValueError:
                        error('Error decrypting letter in message.')
                except ValueError:
                    error('Please input an integer for the Encryption Key.')
            elif is_it_encrypted == 'n':
                message = input('Message:')
                decrypt_morse(message, encrypted=False)
            else:
                error('Please input Y or N')

        # Quit
        elif choice == 4:
            break

        # Error
        else:
            error()
