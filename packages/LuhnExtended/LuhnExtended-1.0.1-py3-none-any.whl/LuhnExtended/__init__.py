# LuhnExtended/__init__.py

"""
LuhnExtended - A library for advanced Luhn algorithm operations.
This library provides functions to generate, verify, and append Luhn check digits,
with support for user-defined checksum values.
"""

__version__ = '1.0.0'
__author__ = 'Luhn Extended'
__license__ = 'MIT'

def checksum(string):
    """
    Compute the Luhn checksum for the provided string of digits. Note this
    assumes the check digit is in place.
    """
    digits = list(map(int, string))
    odd_sum = sum(digits[-1::-2])
    even_sum = sum([sum(divmod(2 * d, 10)) for d in digits[-2::-2]])
    return (odd_sum + even_sum) % 10

def verify(string, checksum_expected=0):
    """
    Check if the provided string of digits satisfies the Luhn checksum.
    
    :param string: The string of digits to verify.
    :param checksum_expected: Expected checksum (default is 0).
    :return: True if valid, False otherwise.
    """
    return checksum(string) == checksum_expected

def generate(string, checksum_desired=0):
    """
    Generate the Luhn check digit to append to the provided string.
    
    :param string: The string of digits to generate a check digit for.
    :param checksum_desired: Desired checksum value (default is 0).
    :return: The generated check digit.
    """
    cksum = checksum(string + '0')
    return (10 - cksum + checksum_desired) % 10

def append(string, checksum_desired=0):
    """
    Append Luhn check digit to the end of the provided string.
    
    :param string: The string of digits to append a check digit to.
    :param checksum_desired: Desired checksum value (default is 0).
    :return: The string with the appended check digit.
    """
    return string + str(generate(string, checksum_desired))

__all__ = [
    'checksum',
    'verify',
    'generate',
    'append'
]
