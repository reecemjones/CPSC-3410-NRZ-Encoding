import wave
import struct
from bitarray import bitarray
import sys

def wav_values(wavfile):
    """ Implements a generator to return raw waveform values from a wav file

    Raw values will be yielded as a floating-point value from -1 to 1

    >>> f"{next(wav_values('message.wav')):0.2f}"
    '-0.09'

    >>> f"{list(wav_values('message.wav'))[320]:0.2f}"
    '0.83'
    """
    
    with wave.open(wavfile, 'rb') as w:
        for pos in range(0, sys.maxsize):
            frame = w.readframes(1)
            if not frame:
                break
            yield struct.unpack('<h', frame)[0] / 2 ** 15

def decode_bits(wavfile):
    """ Implements a generator to return a decoded bitstream from wavfile

    >>> next(decode_bits('message.wav'))
    0
    
    >>> list(decode_bits('message.wav'))[0:10]
    [0, 0, 1, 1, 1, 0, 0, 1, 0, 1]

    Hint: enumerate can be used to iterate over the values in the file including a numeric index
    """
    for i, element in enumerate(wav_values(wavfile)):
        if (i + 1) % 147 == 0:
            if element > 0:
                yield 1
            else:
                yield 0

def bits_to_string(bits):
    """ Generator to map an iterator of bits to an iterator of characters

    >>> next(bits_to_string(iter([0, 0, 1, 1, 1, 0, 0, 1, 0, 1])))
    'N'

    >>> next(bits_to_string(iter([1, 0, 1, 1, 1, 0, 0, 1, 0, 1])))
    Traceback (most recent call last):
    ...
    ValueError: Invalid start bit

    >>> next(bits_to_string(iter([0, 0, 1, 1, 1, 0, 0, 1, 0, 0])))
    Traceback (most recent call last):
    ...
    ValueError: Invalid stop bit

    Hint: bitarray can be used to convert bits to bytes
        https://pypi.org/project/bitarray/
    Hint2: Raw byte values can be converted to strings using `bytes.decode`:
        https://docs.python.org/3/library/stdtypes.html#bytes.decode
    """
    arr = []
    string = ""

    # append generator element to arr
    for i in bits:
        if len(arr) != 10:
            arr.append(i)
        else:
            break

    # exceptions for invalid start/stop bits
    if arr[0] != 0:
        raise ValueError("Invalid start bit")
    if arr[9] != 1:
        raise ValueError("Invalid stop bit")

    # append middle 8 bits to string variable
    for i in range(len(arr)):
        if i == 0 or i == 9:
            i += 1
        else:
            string += str(arr[i])

    # convert to char
    yield chr(int(string, 2)).upper()

def decode(wavfile):
    """ Decode a wav file containing an NRZ encoded message

    >>> ''.join(decode('message.wav'))
    'Now you know how to decode messages transmitted using non-return-to-zero encoding!'
    """
    bits = decode_bits(wavfile)
    bits_to_string(bits)

if __name__ == '__main__':
    print(''.join(decode(sys.argv[1])))
