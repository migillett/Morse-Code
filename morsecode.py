import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav

# Morse Code Dictionary (International Morse Code Standard)
MORSE_CODE_DICT = {
    'A': '.-',     'B': '-...',   'C': '-.-.',   'D': '-..',    'E': '.',
    'F': '..-.',   'G': '--.',    'H': '....',   'I': '..',     'J': '.---',
    'K': '-.-',    'L': '.-..',   'M': '--',     'N': '-.',     'O': '---',
    'P': '.--.',   'Q': '--.-',   'R': '.-.',    'S': '...',    'T': '-',
    'U': '..-',    'V': '...-',   'W': '.--',    'X': '-..-',   'Y': '-.--',
    'Z': '--..',   '0': '-----',  '1': '.----',  '2': '..---',  '3': '...--',
    '4': '....-',  '5': '.....',  '6': '-....',  '7': '--...',  '8': '---..',
    '9': '----.',  ' ': ' '  # Space between words
}

def text_to_morse(text):
    """Convert text to Morse code."""
    return ' '.join(MORSE_CODE_DICT.get(char.upper(), '') for char in text)

def generate_morse_audio(text, frequency=600, dot_length=0.07, sample_rate=44100, output_file="morse.wav"):
    """Generate a Morse code WAV file from text."""
    morse_code = text_to_morse(text)
    print(f"Morse Code: {morse_code}")

    # Define time durations
    unit = dot_length  # Dot duration
    dash_length = 3 * unit
    space_between_symbols = unit  # Space between dots and dashes
    space_between_letters = 3 * unit  # Space between letters
    space_between_words = 7 * unit  # Space between words

    # Generate waveform
    signal = np.array([], dtype=np.float32)

    def generate_tone(duration):
        """Generate a sine wave tone for the given duration."""
        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        return 0.5 * np.sin(2 * np.pi * frequency * t)

    def generate_silence(duration):
        """Generate silence for the given duration."""
        return np.zeros(int(sample_rate * duration))

    for char in morse_code:
        if char == '.':  # Dot
            signal = np.append(signal, generate_tone(unit))
            signal = np.append(signal, generate_silence(space_between_symbols))
        elif char == '-':  # Dash
            signal = np.append(signal, generate_tone(dash_length))
            signal = np.append(signal, generate_silence(space_between_symbols))
        elif char == ' ':  # Space (between words or letters)
            signal = np.append(signal, generate_silence(space_between_words if signal[-1] != 0 else space_between_letters))

    # Convert to 16-bit PCM format and save to WAV file
    wave_int16 = np.int16(signal * 32767)
    wav.write(output_file, sample_rate, wave_int16)
    print(f"Morse Code audio saved to {output_file}")

    # Play the generated Morse code
    sd.play(signal, samplerate=sample_rate)
    sd.wait()

# Example: Generate Morse Code Audio for "HELLO WORLD"
generate_morse_audio("HELLO WORLD")
