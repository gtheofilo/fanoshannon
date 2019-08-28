import json
import base64
import random
import math
from collections import Counter


def character_frequencies(text):
    """Calculates the occuring frequency of each
    caracter"""
    number_of_characters = len(text)
    c = Counter(text)

    frequencies = []
    for character, occurence in c.most_common():
        frequencies.append((character, occurence / number_of_characters))

    return frequencies


def shannon_fano(list_of_characters, encoded=[], prefix=''):
    """An implementation of the shannon fano encoding using recursion

    Args:
    list_of_characters: A list of tuples with the occuring characters and
    their frequency. Example: [(a, 0.3), (b, 0.3), (c, 0.3)]

    encoded: The list that is used as memory to hold the encoding characters.
    It is updated after each run of the algorithm

    prefix: Like the encoded argument it is updated at each step of the
    algorithm

    Returns:
        A dictionary variable with keys the characters and values their
        encoded string
    """
    frequencies_sum = 0
    isFirstIteration = True

    left_list = []
    right_list = []

    for position, character in enumerate(list_of_characters):
        frequencies_sum = frequencies_sum + character[1]

    local_frequency = 0

    for position, character in enumerate(list_of_characters):

        local_frequency = local_frequency + character[1]
        if local_frequency <= frequencies_sum / 2 or isFirstIteration:
            left_list.append(character)
            isFirstIteration = False
        else:
            right_list.extend(list_of_characters[position::])
            break

    if len(left_list) > 1:
        shannon_fano(left_list, encoded, prefix + '0')
    else:
        prefix = prefix + '0'
        encoded.append((left_list[0], prefix))
        prefix = prefix[:-1]

    if len(right_list) > 1:
        shannon_fano(right_list, encoded, prefix + '1')
    else:
        prefix = prefix + '1'
        encoded.append((right_list[0], prefix))
        prefix = prefix[:-1]

    coding_dictionary = {}

    for character, coding in encoded:
        coding_dictionary[character[0]] = coding

    return coding_dictionary


def compression(text, coding_dictionary):
    "Calculates the encoded string for each character of the text file"
    encoded_text = []
    encoded_word = ''
    text = text + ' '

    for character in text:
        encoded_word = encoded_word + coding_dictionary[character]
        if character == ' ':
            encoded_text.append(encoded_word)
            encoded_text.append(coding_dictionary[' '])
            encoded_word = ''

    encoded_text.pop()

    return encoded_text


def entropy_calculator(character_frequencies):
    """Calculates the entropy given the frequencies of the characters"""
    entropy = 0
    for i in character_frequencies:
        entropy = entropy + i[1] * math.log(1 / i[1], 2)

    return entropy

def xor(a, b):
    """Computes the XOR operation between A and B"""
    result = []
    for i in range(1, len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')
    return ''.join(result)


def mod2div(divident, divisor):
    pick = len(divisor)
    tmp = divident[0: pick]
    while pick < len(divident):
        if tmp[0] == '1':
            tmp = xor(divisor, tmp) + divident[pick]
        else:
            tmp = xor('0' * pick, tmp) + divident[pick]
        pick += 1
    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0' * pick, tmp)
    checkword = tmp
    return checkword


def encodeData(data, key):
    l_key = len(key)
    appended_data = data + '0' * (l_key - 1)
    remainder = mod2div(appended_data, key)
    codeword = data + remainder
    return codeword


class colors:
    """Colors for printing the results"""""
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'

    ENDC = '\033[0m'


def color_print(string, color_code, *args):
    """Custom color printing for CLI"""
    if len(args) > 0:
        print(color_code, string, colors.ENDC, end=args[0])
    else:
        print(color_code, string, colors.ENDC)


def print_title(string, *args):
    color_print(string, colors.OKBLUE, *args)


def print_process(string, *args):
    color_print(string, colors.OKGREEN, *args)




# Configuration of the Python Script using text file's name, noise level and
# code lenght
filename = input('Provide the filename to be compressed(must be in the same '
                 'folder with the .py file): ')
filename = filename + '.txt'
file = open(filename, 'r')
if file.mode == 'r':
    text_file = file.read()

text_size = len(text_file) * 8
length = int(input('Provide the code length: '))
noise = int(input('Provide the noise level: '))

# First Question
print_process('1. Generating the code table...', '')
char_freq = character_frequencies(text_file)
code_table = shannon_fano(char_freq)
print_process('✓\n')
print_process(f'Code Table: {code_table}', '\n\n')


# Second Question
print_process('2. Compressing the input...', '')
compressed_text = compression(text_file, code_table)
print_process('✓\n')
print_process(f'Compressed Text: {compressed_text}', '\n\n')
comp_bits = 0
for i in compressed_text:
    for bit in i:
        comp_bits = comp_bits + 1

key = '1001'  # g(x) synarthsh pou ginetai h diairesh

# Third Question
print_process('3. Applying the cyclic encoding...', '')
cyclic_encoded = []
for word in compressed_text:
    cyclic_encoded.append(encodeData(word, key))
print_process('✓\n')
print_process(f'Cyclic Encoded: {cyclic_encoded}', '\n\n')
added_bits = 0
for i in cyclic_encoded:
    for bit in i:
        added_bits = added_bits + 1

# Fourth Question
code_with_noise = []
print_process('4. Applying noise...', '')
for word in cyclic_encoded:
    randint = random.randint(0, noise)
    temp = list(word)
    for i in range(0, randint + 1):
        if temp[i] == 0:
            temp[i] = str(1)
        else:
            temp[i] = str(0)
    temp = ''.join(temp)
    code_with_noise.append(temp)
print_process('✓\n')
print_process(f'Noise Result: {code_with_noise}', '\n\n')

# Fifth Question
print_process('5. Generating the Base64 string...', '')
b_64 = base64.b64encode(
    ''.join(str(e) for e in compressed_text).encode('ascii'))
print_process('✓\n')
print_process(f'Base64 String: {b_64}', '\n\n')

# Sixth Question
print_process('6. Generating the JSON...', '')
j = {

    "compression_algorithm": "Fano-Shannon",

    "code": {

        "name": "cyclic code",
        "noise_level": noise,
        "code lenght": length,

        "P": code_with_noise,
        "base64": b_64.decode("utf-8")

    }

}
j = json.dumps(j, indent=4)
print_process('✓\n')

# Seventh Question
print_process('7. Sending the message...', '')
print_process('✓\n')
print_process(f'JSON: {j}', '\n\n')

compressed_size = 5
print_process('8. Generating statistics...', '')
print_process('✓\n')
print_process(f'Size: {text_size} bits', '\n\n')
print_process(f'Compressed Size: {comp_bits} bits', '\n\n')
print_process(f'Final Size: {added_bits} bits', '\n\n')
print_process(f'Entropy: {entropy_calculator(char_freq)}', '\n\n')
print_process(f'Added Bits: {added_bits - comp_bits} bits', '\n\n')
