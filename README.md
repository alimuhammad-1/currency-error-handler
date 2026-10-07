# Safe Currency Converter

A small Python application built for the ORBIT Software Engineering task:

**Handle errors like the user is watching**

The application converts currencies using a fixed local exchange-rate table. It does not call a live API or any external service.

## Features

- Fixed local currency rates
- Clear validation errors
- Graceful handling of bad input
- Internal logging
- No sensitive implementation details shown to users
- Automated tests for valid and invalid cases
- No external Python packages required

## Supported currencies

- NGN
- USD
- EUR
- GBP

The rates are demonstration rates stored locally in `converter.py`.

## Project structure

```text
currency-error-handler/
├── app.py
├── converter.py
├── test_converter.py
├── requirements.txt
├── README.md
├── .gitignore
└── app.log              # Created after the application runs
```

## How to run

### 1. Open the project in VS Code

Open the project folder:

```text
currency-error-handler
```

### 2. Open the VS Code terminal

Use:

```text
Terminal > New Terminal
```

### 3. Check Python

Run:

```bash
python --version
```

If that does not work on Windows, try:

```bash
py --version
```

### 4. Run the application

```bash
python app.py
```

Or on Windows:

```bash
py app.py
```

### 5. Run the tests

```bash
python -m unittest -v
```

Or:

```bash
py -m unittest -v
```

All tests should pass.

## Failure cases

| Failure case | Example | What the user sees | What is logged |
|---|---|---|---|
| Empty amount | `""` | `Amount is required.` | Empty amount received |
| Non-numeric amount | `five thousand` | `Please enter a valid number.` | Non-numeric amount received |
| Negative amount | `-500` | `Amount must be greater than or equal to zero.` | Negative amount received |
| Very long amount | 31+ characters | `Amount is too long.` | Amount exceeded 30 characters |
| Unsupported source currency | `XYZ` | `Source currency is not supported.` | Unsupported source currency |
| Unsupported target currency | `XYZ` | `Target currency is not supported.` | Unsupported target currency |
| Empty currency | `""` | `Source currency is required.` | Empty source currency |
| Unexpected amount type | list/object | `Invalid input type.` | Unexpected type |
| Unexpected currency type | `None` | `Invalid input type.` | Unexpected type |

## Why the errors are handled this way

The program separates user-facing errors from internal logging.

For example, the user should not see a Python traceback or implementation details such as:

```text
decimal.InvalidOperation
```

Instead, the user receives:

```text
Please enter a valid number.
```

The application records useful information in `app.log` for debugging.

## Logging

After running the application, handled errors are recorded in:

```text
app.log
```

Example:

```text
WARNING | __main__ | Non-numeric amount received.
WARNING | __main__ | Negative amount received.
WARNING | __main__ | Unsupported target currency received: XYZ
```

The log helps a developer diagnose problems without exposing internal details to the user.

The log file is excluded from GitHub through `.gitignore` because logs are runtime files and might contain information from real users in a production application.

## Testing

The test suite covers:

1. Valid conversion
2. Empty amount
3. Invalid amount
4. Negative amount
5. Very long amount
6. Unsupported source currency
7. Unsupported target currency
8. Empty currency
9. Unexpected amount type
10. Unexpected currency type
11. Friendly user-facing error
12. Zero amount

Run:

```bash
python -m unittest -v
```

## Example

Input:

```text
Amount: 3000
From currency: NGN
To currency: USD
```

Output:

```text
3000 NGN = 2.00 USD
```

## Security and reliability considerations

- No live service is contacted.
- No API key is required.
- User input is validated before conversion.
- Expected errors are handled without a traceback.
- Unexpected errors are caught by the final safety handler and logged.
- Runtime logs are excluded from version control.

## GitHub submission

Create a new GitHub repository named:

```text
currency-error-handler
```

Then run these commands from the project folder:

```bash
git init
git add .
git commit -m "Build graceful currency converter error handling"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with the URL GitHub gives you for your new repository.

Example:

```bash
git remote add origin https://github.com/YOUR-USERNAME/currency-error-handler.git
```

After pushing, submit the GitHub repository URL to ORBIT.
