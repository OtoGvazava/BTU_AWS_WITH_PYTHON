import re

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('text', type=str)

args = parser.parse_args()
text = args.text


def extract_float_numbers(txt):
    float_list = re.findall(r"[-+]?\d+\.\d+", txt)
    return [float(x) for x in float_list]


def extract_integer_numbers(txt):
    integer_list = re.findall(r"[-+]?\d+", txt)
    return [int(x) for x in integer_list]


def find_odd_numbers(list_of_integers):
    return [num for num in list_of_integers if num % 2 != 0]


def find_even_numbers(list_of_integers):
    return [num for num in list_of_integers if num % 2 == 0]


float_numbers = extract_float_numbers(text)
integer_numbers = extract_integer_numbers(text)
odd_numbers = find_odd_numbers(integer_numbers)
even_numbers = find_even_numbers(integer_numbers)

print("""
Float numbers: {}
Odd Numbers: {}
Even Numbers: {}
""".format(float_numbers, odd_numbers, even_numbers))
