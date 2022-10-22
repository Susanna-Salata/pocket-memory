import unittest
from utils import regex


class TestRegexBirthday(unittest.TestCase):

    def test_check_birthday_when_should_be_ok(self):
        birthday = "1986-03-15"
        self.assertTrue(regex.check_birthday(birthday))

    def test_check_birthday_when_29_february_in_long_year_should_ok(self):
        birthday = "2000-02-29"
        self.assertTrue(regex.check_birthday(birthday))

    def test_check_birthday_when_elder_year_should_fail(self):
        birthday = "1886-03-15"
        self.assertFalse(regex.check_birthday(birthday))

    def test_check_birthday_when_young_year_should_fail(self):
        birthday = "2025-03-15"
        self.assertFalse(regex.check_birthday(birthday))

    def test_check_birthday_when_out_of_range_month_should_fail(self):
        birthday = "1986-13-15"
        self.assertFalse(regex.check_birthday(birthday))

    def test_check_birthday_when_1_digit_month_should_fail(self):
        birthday = "1986-3-15"
        self.assertFalse(regex.check_birthday(birthday))

    def test_check_birthday_when_out_of_range_day_should_fail(self):
        birthday = "1986-03-32"
        self.assertFalse(regex.check_birthday(birthday))

    def test_check_birthday_when_out_of_range_sort_month_should_fail(self):
        birthday = "1986-04-31"
        self.assertFalse(regex.check_birthday(birthday))

    def test_check_birthday_when_delimiter_should_fail(self):
        birthday = "2000.02.29"
        self.assertFalse(regex.check_birthday(birthday))

    def test_check_birthday_when_day_month_year_should_fail(self):
        birthday = "15-03-1985"
        self.assertFalse(regex.check_birthday(birthday))


if __name__ == '__main__':
    unittest.main()
