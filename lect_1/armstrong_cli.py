import argparse

parser = argparse.ArgumentParser(description='Find and calculate sum of Armstrong numbers!.')

parser.add_argument('--start_number', type=int)
parser.add_argument('--end_number', type=int)

args = parser.parse_args()
start_number = args.start_number
end_number = args.end_number

armstrong_numbers = []

# start_number = 9
# end_number = 9999

for number in range(start_number, end_number):
    str_number = str(number)
    str_number_len = len(str_number)
    sum_of_digits = 0

    for digit in str_number:
        sum_of_digits += int(digit) ** str_number_len

    if sum_of_digits == number:
        armstrong_numbers.append(number)


def sum_of(list_of):
    if len(list_of) == 1:
        return list_of[0]
    else:
        return list_of[0] + sum_of(list_of[1:])


sum_of_armstrong_numbers = sum_of(armstrong_numbers)

print("Armstrong numbers: {} \nSum of Armstrong numbers: {}".format(armstrong_numbers, sum_of_armstrong_numbers))
