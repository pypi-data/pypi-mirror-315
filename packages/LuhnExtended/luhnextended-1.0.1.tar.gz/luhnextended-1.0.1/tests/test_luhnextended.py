# tests/test_luhnextended.py

import unittest
from LuhnExtended import checksum, verify, generate, append

class TestLuhnExtended(unittest.TestCase):
    
    def test_checksum(self):
        self.assertEqual(checksum('356938035643806'), 7)

    def test_verify(self):
        self.assertTrue(verify('356938035643806', 7))
        self.assertFalse(verify('356938035643806', 0))
        self.assertFalse(verify('534618613411236', 7))

    def test_generate(self):
        self.assertEqual(generate('35693803564380', 7), 6)

    def test_append(self):
        self.assertEqual(append('35693803564380', 7), '356938035643806')

if __name__ == '__main__':
    unittest.main()