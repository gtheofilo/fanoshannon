from collections import Counter
from functools import reduce

def character_frequencies(text):
    """Removes all spaces and calculates the occuring frequency of each
    caracter"""

    text = text.replace(' ', '')
    number_of_characters = len(text)
    c = Counter(text)

    frequencies = []
    for character, occurence in c.most_common():
        frequencies.append((character, occurence / number_of_characters))

    return frequencies

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
        if local_frequency <= frequencies_sum/2 or isFirstIteration:
            left_list.append(character)
            isFirstIteration = False
        else:
            right_list.extend(list_of_characters[position::])
            break






    if len(left_list) > 1:
        shannon_fano(left_list, encoded, prefix + '0')
    else:
        prefix =  prefix + '0'
        encoded.append((left_list[0], prefix))
        prefix = prefix[:-1]

    if len(right_list) > 1:
        shannon_fano(right_list, encoded, prefix + '1')
    else:
        prefix =  prefix + '1'
        encoded.append((right_list[0], prefix))
        prefix = prefix[:-1]

    return encoded









text = "AAAAAAbafwfa"
a = shannon_fano(character_frequencies(text))
print(a)
