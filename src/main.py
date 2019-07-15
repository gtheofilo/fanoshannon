import json
import base64
import random
from collections import Counter


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'

    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def color_print(string, color_code, *args):
    """Custom color printing for CLI"""
    if len(args) > 0:
        print(color_code, string, bcolors.ENDC, end=args[0])
    else:
        print(color_code, string, bcolors.ENDC)


def print_title(string, *args):
    color_print(string, bcolors.OKBLUE, *args)


def print_process(string, *args):
    color_print(string, bcolors.OKGREEN, *args)


def character_frequencies(text):
    """Removes all spaces and calculates the occuring frequency of each
    caracter"""

    # text = text.replace(' ', '')
    number_of_characters = len(text)
    c = Counter(text)

    frequencies = []
    for character, occurence in c.most_common():
        frequencies.append((character, occurence / number_of_characters))

    return frequencies


def xor(a, b):
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


def shannon_fano(list_of_characters, encoded=[], prefix=''):
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
    # text = text.replace(' ', '')
    encoded_text = []
    encoded_word = ''
    text = text + ' '
    for character in text:
        encoded_word = encoded_word + coding_dictionary[character]
        if character == ' ':
            encoded_text.append(encoded_word)
            encoded_word = ''

    return encoded_text


filename = input('Provide the filename to be compressed: ')
ext='.txt'
filename+=ext
f=open(filename,"r")
if f.mode=="r":
    text=f.read()


length = int(input('Provide the code length: '))

noise = int(input('Provide the noise level: '))

print_process('1. Generating the code table...', '')
code_table = shannon_fano(character_frequencies(text))
print_process('✓\n')
print_process(f'Code Table: {code_table}', '\n\n')

print_process('2. Compressing the input...', '')
compressed_text = compression(text, code_table)
print_process('✓\n')
print_process(f'Compressed Text: {compressed_text}', '\n\n')

key = '1001'  # g(x) synarthsh pou ginetai h diairesh
print_process('3. Applying the cyclic encoding...', '')
cyclic_encoded = []
for word in compressed_text:
    cyclic_encoded.append(encodeData(word, key))
print_process('✓\n')
print_process(f'Cyclic Encoded: {cyclic_encoded}', '\n\n')

code_with_noise = []
print_process('3. Applying noise...', '')
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

print_process('4. Generating the Base64 string...', '')
b_64 = base64.b64encode(
    ''.join(str(e) for e in compressed_text).encode('ascii'))
print_process('✓\n')
print_process(f'Base64 String: {b_64}', '\n\n')

print_process('4. Generating the JSON...', '')
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
j = json.dumps(j)
print_process('✓\n')
print_process(f'JSON: {j}', '\n\n')

# μέγεθος αρχείου, εντροπιία , τελικό μέγεθος αρχείου, εντροπία, πόσα bits προσθέθηκαν, πόσα bits διορθώθηκαν.


print_process('4. Generating statistics...', '')
b_64 = base64.b64encode(compressed_text.encode('ascii'))
print_process('✓\n')

print_process(f'Size: {b_64}', '\n\n')
print_process(f'Compressed Size: {b_64}', '\n\n')
print_process(f'Entropy: {b_64}', '\n\n')
print_process(f'Size: {b_64}', '\n\n')
print_process(f'Size: {b_64}', '\n\n')
