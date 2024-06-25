
# Summer Break API

## Introduction

This app uses Python and Flask which provides a simple web service API to help report income and expenses. 

Provides endpoints to: 
-  Upload transaction data via a CSV file 
-  Retrieve summary reports of transactions.

## Requirements

- Python 3.8+
- Flask
- pandas

## Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone git@github.com:JeremyDuncan/summer_break_api.git
   cd summer_break_api
   ```

2. **Install Flask and pandas:**

   ```bash
   pip install Flask pandas
   ```

3. **Run Flask app:**

   ```bash
   python summer_break_api.py
   ```

   The app will be available at `http://127.0.0.1:5000`.

## Executing API

### test.sh
To run all API endpoints to demonstrate API functionality, run:

 ```bash
   bash test.sh
```

## Endpoint Descriptions

### Upload Transactions

**Endpoint:** `POST /transactions`

**Description:** Accepts CSV files containing transaction data and stores the data in memory.

**Request:**

- Method: POST
- File: A CSV file with columns: `Date, Type, Amount($), Memo`

**Example using `curl`:**

```bash
curl -X POST -F 'data=@transactions.csv' http://127.0.0.1:5000/transactions
```

### Get Report

**Endpoint:** `GET /report`

**Description:** Returns a JSON document with the tally of gross revenue, expenses, and net revenue.

**Response:**

```json
{
    "gross-revenue": "$<amount>",
    "expenses": "$<amount>",
    "net-revenue": "$<amount>"
}
```

**Example using `curl`:**

```bash
curl http://127.0.0.1:5000/report
```

## CSV Format Instructions

CSV data formatted as follows:

`Date, Type, Amount($), Memo`

Where `Type` is one of "Income" or "Expense" and `Memo` is either an expense category or job address (both just strings).

For example:

```
2020-07-01, Expense, 18.77, Gas
2020-07-04, Income, 40.00, 347 Woodrow
2020-07-06, Income, 35.00, 219 Pleasant
2020-07-12, Expense, 49.50, Repairs
```

## Additional Context

### Assumptions

- The input CSV file is correctly formatted.
- The application data is ephemeral in memory, and not stored in a database.

### Shortcomings

- No data validation is performed on the CSV input.
- No error handling for incorrect CSV formats.
- Data is stored in memory and not stored permanently.

### Possible refinements in the future

- Add data validation for CSV data.
- Use a database such as MySQL or PostgreSQL for storing transactional data.
- Add authentication for security purposes.
- Add unit tests for the application.
