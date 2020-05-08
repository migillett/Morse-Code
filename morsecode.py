#!/usr/bin/python3

# Written by Michael Gillett, 2020
# github.com/gillettmi

# A simple morse code conversion program

import time
import winsound as ws

morse = {
    'a': '.-',      'b': '-...',    'c': '-.-.',
    'd': '-..',     'e': '.',       'f': '..-.',
    'g': '--.',     'h': '....',    'i': '..',
    'j': '.---',    'k': '-.-',     'l': '.-..',
    'm': '--',      'n': '-.',      'o': '---',
    'p': '.--.',    'q': '--.-',    'r': '.-.',
    's': '...',     't': '-',       'u': '..-',
    'v': '..-',     'w': '.--',     'x': '-..-',
    'y': '-.--',    'z': '--..',

    '1': '.----',   '2': '..---',   '3': '...---',
    '4': '....-',   '5': '.....',   '6': '-....',
    '7': '--...',   '8': '---..',   '9': '----.',
    '0': '-----',

    '.': '.-.-.-',  ',': '--..--',  '?': '..--..',
    '!': '-.-.--',  '&': '.-...',   ':': '---...',
    ';': '-.-.-.',  '@': '.--.-.',  '$': '...-..-'
}

output = ''
errors = ''


# PROGRAM BEGINS HERE
# var 0 = input file, var 1 = output file, var 2 = tempo, var 3 = frequency
def morse_code(text_file='input.txt', output_file='output.txt', tempo=100, fq=600):

    # import the text file
    try:
        with open(text_file, 'r') as raw_input:

            # for each line in text file, save it to message variable as a list
            message = raw_input.readlines()
            print('Input message:', message)

            # loop through each line in the message
            for line in message:

                # split the words sand save to line list
                line = line.split(' ')

                # convert each word in line list
                for word in line:
                    for letter in list(word):
                        # make each letter lowercase
                        letter = letter.lower()

                        # convert the letter to morse and add to global output string
                        if letter in morse:
                            global output
                            output += morse[letter] + ' '

                        # if the text is '\n', skip it
                        elif letter == '\n':
                            continue

                        # if the character is unrecognized, print it
                        else:
                            global errors
                            errors += letter

        # print all of the errors
        if errors != '':
            print('Unrecognized characters omitted: {0}'.format(errors))

        # write output file
        with open(output_file, 'w') as o:
            o.write(output)
        print('Transmitting message:', output)
        for t in output:
            if t == '.':
                ws.Beep(fq, tempo)
            elif t == '-':
                ws.Beep(fq, tempo*3)
            else:
                time.sleep(tempo/250)
        print('Transmission complete')

    except FileNotFoundError:
        print('Warning: input file {0} not found'.format(text_file))


if __name__ == '__main__':
    # runs the main Morse Code converter
    morse_code()
