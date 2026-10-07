import unittest
from decimal import Decimal

from converter import (
    convert_currency,
    user_friendly_convert,
    EmptyInputError,
    InvalidAmountError,
    NegativeAmountError,
    AmountTooLongError,
    UnsupportedCurrencyError,
    InvalidTypeError,
)


class TestCurrencyConverter(unittest.TestCase):

    def test_valid_conversion(self):
        result = convert_currency("3000", "NGN", "USD")
        self.assertEqual(result, Decimal("2.00"))

    def test_empty_amount(self):
        with self.assertRaises(EmptyInputError):
            convert_currency("", "NGN", "USD")

    def test_invalid_amount(self):
        with self.assertRaises(InvalidAmountError):
            convert_currency("five thousand", "NGN", "USD")

    def test_negative_amount(self):
        with self.assertRaises(NegativeAmountError):
            convert_currency("-500", "NGN", "USD")

    def test_very_long_amount(self):
        with self.assertRaises(AmountTooLongError):
            convert_currency("9" * 31, "NGN", "USD")

    def test_unsupported_source_currency(self):
        with self.assertRaises(UnsupportedCurrencyError):
            convert_currency("5000", "XYZ", "USD")

    def test_unsupported_target_currency(self):
        with self.assertRaises(UnsupportedCurrencyError):
            convert_currency("5000", "NGN", "XYZ")

    def test_empty_currency(self):
        with self.assertRaises(EmptyInputError):
            convert_currency("5000", "", "USD")

    def test_unexpected_amount_type(self):
        with self.assertRaises(InvalidTypeError):
            convert_currency(["5000"], "NGN", "USD")

    def test_unexpected_currency_type(self):
        with self.assertRaises(InvalidTypeError):
            convert_currency("5000", None, "USD")

    def test_user_gets_friendly_error(self):
        success, message = user_friendly_convert(
            "not-a-number", "NGN", "USD"
        )
        self.assertFalse(success)
        self.assertEqual(message, "Please enter a valid number.")

    def test_zero_is_allowed(self):
        result = convert_currency("0", "NGN", "USD")
        self.assertEqual(result, Decimal("0.00"))


if __name__ == "__main__":
    unittest.main()
