import unittest
from utils import regex


class TestRegexPhone(unittest.TestCase):

    def test_check_phone_when_10_digits_should_be_ok(self):
        phone = "0935552211"
        self.assertTrue(regex.check_phone(phone))

    def test_check_phone_when_9_digits_should_fail(self):
        phone = "093555221"
        self.assertFalse(regex.check_phone(phone))

    def test_check_phone_when_11_digits_should_fail(self):
        phone = "09355522111"
        self.assertFalse(regex.check_phone(phone))

    def test_check_phone_when_chars_shout_fail(self):
        phone = "093555221A"
        self.assertFalse(regex.check_phone(phone))

    def test_check_phone_when_puncts_should_fail(self):
        phone = "093555221-"
        self.assertFalse(regex.check_phone(phone))

    def test_check_phone_when_empty_should_fail(self):
        phone = ""
        self.assertFalse(regex.check_phone(phone))

    def test_check_phone_when_not_string_should_fail(self):
        phone = 9935552211
        self.assertFalse(regex.check_phone(phone))


if __name__ == '__main__':
    unittest.main()
