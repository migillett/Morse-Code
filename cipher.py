def caesar_cypher(letter, mode, key=0):
    if mode == 'encrypt':
        letter = chr((ord(letter) + key - 97) % 26 + 97)
        return letter
    elif mode == 'decrypt':
        letter = chr((ord(letter) - key - 97) % 26 + 97)
        return letter
