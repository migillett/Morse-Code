#!/usr/bin/python3

# Written by Michael Gillett, 2020
# github.com/gillettmi

# A simple morse code conversion program

import time
import os
from cipher import *
try:
    import winsound as ws
    audio_output = True
except ModuleNotFoundError:
    print('Winsound module not found. Audio output is disabled.\n')
    audio_output = False

morse = {
    'a': '.-',      'b': '-...',    'c': '-.-.',
    'd': '-..',     'e': '.',       'f': '..-.',
    'g': '--.',     'h': '....',    'i': '..',
    'j': '.---',    'k': '-.-',     'l': '.-..',
    'm': '--',      'n': '-.',      'o': '---',
    'p': '.--.',    'q': '--.-',    'r': '.-.',
    's': '...',     't': '-',       'u': '..-',
    'v': '...-',    'w': '.--',     'x': '-..-',
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

current_directory = os.getcwd()
input_file = os.path.join(current_directory, 'input.txt')
output_file = os.path.join(current_directory, 'output.txt')


def press_enter():
    input('Press enter to continue.')


def error(error_message):
    print(error_message)
    press_enter()


# PROGRAM BEGINS HERE
def encode_morse(message, encrypt=False, encrypt_key=0):
    global output, errors
    # split the words sand save to line list
    words = message.split(' ')

    # convert each word in line list
    for word in words:
        for letter in list(word):
            # make each letter lowercase
            letter = letter.lower()

            # If encrypt == True : encrypt input
            if encrypt:
                letter = caesar_cypher(letter=letter, mode='encrypt', key=encrypt_key)

            # convert the letter to morse and add to global output string
            if letter in morse:
                output += morse[letter] + ' '

            # if the character is unrecognized, print it
            else:
                errors += letter
    # print all of the errors
    if errors != '':
        print('Unrecognized characters omitted: {0}'.format(errors))
    write_file(output, output_file)
    transmit(output)


def decode_morse(message='', encrypted=False, decrypt_key=0):
    output_message = ''
    decrypted_message = ''
    morse_letters = message.split(' ')
    for letter in morse_letters:
        try:
            output_message += (list(morse.keys())[list(morse.values()).index(letter.lower())])
        except ValueError:
            print('Unable to convert letter:', letter)
            continue
    print('Your message:', output_message)
    write_file(output_message, output_file)

    if encrypted:
        for letter in output_message:
            decrypted_message += caesar_cypher(letter=letter,
                                               mode='decrypt',
                                               key=decrypt_key)
        print('Your decrypted message:', decrypted_message)
        write_file(decrypted_message, output_file)


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


def main():
    while True:

        print(menu)
        try:
            choice = int(input('Input:'))
        except ValueError:
            pass

        # Convert input from text to morse code (no encryption)
        if choice == 1:
            encode_morse(str(input('Message:')))

        # Convert and encrypt input
        elif choice == 2:
            try:
                encode_morse(str(input('Message:')),
                             encrypt=True,
                             encrypt_key=int(input('Encryption Key:')))
            except ValueError:
                error('Invalid input. Please input an integer for the Encryption Key.')

        # Decrypt input
        elif choice == 3:
            while True:
                # select if the message is encrypted or not
                is_it_encrypted = str(input('Is the message encrypted? (Y/N)')).lower()

                # if the message is encrypted:
                if is_it_encrypted == 'y':
                    try:
                        decode_morse(message=str(input('Message:')),
                                     encrypted=True,
                                     decrypt_key=int(input('Encryption Key:')))
                        break
                    except ValueError:
                        error('Please input an integer for the Encryption Key.')

                # if the image isn't encrypted:
                elif is_it_encrypted == 'n':
                    decode_morse(str(input('Message:')))
                    break

                # wrong input
                else:
                    error('Please input Y or N')

        # Quit
        elif choice == 4:
            break

        # Error
        else:
            error('Please input an integer from the menu.')


if __name__ == '__main__':
    main()
