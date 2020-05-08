#!/usr/bin/python3

# Written by Michael Gillett, 2020
# github.com/gillettmi

# A simple morse code conversion program

import time
import winsound as ws

# frequency of tone (Hz)
fq = 600

morse = {
    'a': '.-',
    'b': '-...',
    'c': '-.-.',
    'd': '-..',
    'e': '.',
    'f': '..-.',
    'g': '--.',
    'h': '....',
    'i': '..',
    'j': '.---',
    'k': '-.-',
    'l': '.-..',
    'm': '--',
    'n': '-.',
    'o': '---',
    'p': '.--.',
    'q': '--.-',
    'r': '.-.',
    's': '...',
    't': '-',
    'u': '..-',
    'v': '..-',
    'w': '.--',
    'x': '-..-',
    'y': '-.--',
    'z': '--..',
    '1': '.----',
    '2': '..---',
    '3': '...---',
    '4': '....-',
    '5': '.....',
    '6': '-....',
    '7': '--...',
    '8': '---..',
    '9': '----.',
    '0': '-----'
}

output = ''
errors = ''


# PROGRAM BEGINS HERE
def main(text_file, output_file):

    # import the text file
    with open(text_file, 'r') as raw_input:

        # for each line in text file, save it to message variable as a list
        message = raw_input.readlines()
        print('Input message: {0}'.format(message))

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
    print('Output message:', output)
    with open(output_file, 'w') as o:
        o.write(output)
    for t in output:
        if t == '.':
            ws.Beep(fq, 100)
        elif t == '-':
            ws.Beep(fq, 200)
        else:
            time.sleep(.3)


if __name__ == '__main__':
    # runs the main Morse Code converter /// var 0 = input file, var 1 = output file
    main('input.txt', 'output.txt')
