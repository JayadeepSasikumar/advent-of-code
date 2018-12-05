import os
import string

from config import DATA_DIR


def _get_input_data(input_file_name):
    input_data_file = os.path.join(DATA_DIR, input_file_name)
    with open(input_data_file, 'r') as fp:
        input_data = fp.read()
    return input_data

def react(units):
    """
    Takes in the ASCII value of the units as a list, iterates and
    eliminates all units of same type and different polarity
    (difference of 32), and returns the resultant reduced list. ASCII
    values of a - z are 97 - 122, and those of A - Z are 65 - 90. So,
    units that can react with each other will be having a difference
    of 32 between them.

    Inputs -
        units - a list of the ASCII value of all the units in a
            polymer.

    Returns -
        reduced_form - a list of ASCII value of all the polymer units
            where no consecutive units can react with each other.
    """
    def _merge_units(left_half, right_half):
        """
        Takes two lists of units and club them together to form a list
        of units that cannot react further.

        Inputs -
            left_half - list of units, short for left units.
            right_half - list of units, short for right units.

        Returns -
            merged_units - list of units that cannot react within
                themselves further.
        """
        if not right_half:
            return left_half
        if not left_half:
            return right_half
        merged_units = []
        left_half_len = len(left_half)
        right_half_len = len(right_half)
        reversed_left_half = left_half.copy()
        reversed_left_half.reverse()
        merge_point = 0
        try:
            for i in range(right_half_len):
                if abs(right_half[i] - reversed_left_half[i]) != 32:
                    merged_units = left_half[0: left_half_len - i] + \
                                    right_half[i: right_half_len]
                    break
                merge_point += 1
        except IndexError:
            pass
        finally:
            first_part = reversed_left_half[merge_point:]
            first_part.reverse()
            second_part = right_half[merge_point:]
            merged_units = first_part + second_part
        return merged_units

    if len(units) < 2:
        return units
    else:
        mid = len(units) // 2
        left_half = units[: mid]
        right_half = units[mid:]
        return _merge_units(react(left_half), react(right_half))

def one():
    polymer = _get_input_data('day_five.txt')
    units = [ord(char) for char in polymer]
    units = react(units)
    return len(units)

def two():
    polymer = _get_input_data('day_five.txt')
    reduced_polymer_lengths = {}
    for i in range(26):
        lowercase_unit = string.ascii_letters[i]
        uppercase_unit = string.ascii_letters[i + 26]
        new_polymer = polymer.replace(lowercase_unit, '')
        new_polymer = new_polymer.replace(uppercase_unit, '')
        units = [ord(char) for char in new_polymer]
        reduced_polymer_lengths[string.ascii_letters[i]] = len(react(units))
    return min(reduced_polymer_lengths.values())
