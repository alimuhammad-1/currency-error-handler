"""
Command-line interface for the Safe Currency Converter.
"""

import logging
from converter import user_friendly_convert, RATES_TO_NGN


def configure_logging():
    logging.basicConfig(
        filename="app.log",
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def main():
    configure_logging()

    print("\nSafe Currency Converter")
    print("Supported currencies:", ", ".join(RATES_TO_NGN.keys()))
    print("This app uses fixed local rates. No internet connection is used.\n")

    amount = input("Amount: ")
    from_currency = input("From currency: ")
    to_currency = input("To currency: ")

    success, message = user_friendly_convert(
        amount, from_currency, to_currency
    )

    print("\n" + message)

    if not success:
        print("Please correct the input and try again.")


if __name__ == "__main__":
    main()
