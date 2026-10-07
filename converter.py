"""
Core logic for the Safe Currency Converter.

The exchange rates are fixed and local. No live service or internet
connection is used.
"""

from decimal import Decimal, InvalidOperation
import logging

logger = logging.getLogger(__name__)

# Fixed local rates. Each value represents NGN per unit of currency.
RATES_TO_NGN = {
    "NGN": Decimal("1"),
    "USD": Decimal("1500"),
    "EUR": Decimal("1750"),
    "GBP": Decimal("2000"),
}


class ConversionError(Exception):
    """Base exception for expected user-input errors."""


class EmptyInputError(ConversionError):
    pass


class InvalidAmountError(ConversionError):
    pass


class NegativeAmountError(ConversionError):
    pass


class AmountTooLongError(ConversionError):
    pass


class UnsupportedCurrencyError(ConversionError):
    pass


class InvalidTypeError(ConversionError):
    pass


def _validate_text(value, field_name):
    """Validate a text input without exposing internal details to users."""
    if not isinstance(value, str):
        logger.error("Unexpected type for %s: %s", field_name, type(value).__name__)
        raise InvalidTypeError("Invalid input type.")

    if not value.strip():
        logger.warning("Empty %s received.", field_name)
        raise EmptyInputError(f"{field_name.capitalize()} is required.")

    return value.strip().upper()


def _parse_amount(amount):
    """Convert a user amount to Decimal after validating it."""
    if not isinstance(amount, (str, int, float, Decimal)) or isinstance(amount, bool):
        logger.error("Unexpected type for amount: %s", type(amount).__name__)
        raise InvalidTypeError("Invalid input type.")

    amount_text = str(amount).strip()

    if not amount_text:
        logger.warning("Empty amount received.")
        raise EmptyInputError("Amount is required.")

    if len(amount_text) > 30:
        logger.warning("Amount input exceeded 30 characters.")
        raise AmountTooLongError("Amount is too long.")

    try:
        value = Decimal(amount_text)
    except (InvalidOperation, ValueError):
        logger.warning("Non-numeric amount received.")
        raise InvalidAmountError("Please enter a valid number.")

    if not value.is_finite():
        logger.warning("Non-finite amount received.")
        raise InvalidAmountError("Please enter a valid number.")

    if value < 0:
        logger.warning("Negative amount received.")
        raise NegativeAmountError("Amount must be greater than or equal to zero.")

    return value


def convert_currency(amount, from_currency, to_currency):
    """
    Convert an amount using the fixed local exchange-rate table.

    Returns a Decimal rounded to two decimal places.
    Raises ConversionError for expected bad inputs.
    """
    value = _parse_amount(amount)
    source = _validate_text(from_currency, "source currency")
    target = _validate_text(to_currency, "target currency")

    if source not in RATES_TO_NGN:
        logger.warning("Unsupported source currency received: %s", source)
        raise UnsupportedCurrencyError("Source currency is not supported.")

    if target not in RATES_TO_NGN:
        logger.warning("Unsupported target currency received: %s", target)
        raise UnsupportedCurrencyError("Target currency is not supported.")

    # Convert source -> NGN -> target.
    result = value * RATES_TO_NGN[source] / RATES_TO_NGN[target]
    return result.quantize(Decimal("0.01"))


def user_friendly_convert(amount, from_currency, to_currency):
    """
    Safe wrapper for UI/CLI use.

    Returns (success, message). Internal exception details are logged,
    while the user receives a clear message.
    """
    try:
        result = convert_currency(amount, from_currency, to_currency)
        return True, f"{amount} {str(from_currency).upper()} = {result} {str(to_currency).upper()}"
    except ConversionError as exc:
        logger.info("Handled user input error: %s", type(exc).__name__)
        return False, str(exc)
    except Exception:
        logger.exception("Unexpected internal error during conversion.")
        return False, "Something went wrong. Please try again."
