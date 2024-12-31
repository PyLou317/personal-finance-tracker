# Personal Finance Tracker - Bank Statement Processor

## Overview

This application processes CSV bank statements, reformats the data, categorizes transactions, and uploads them to a Google Sheet for personal finance tracking.

## Features

- Bank Statement Compatibility: Processes bank statements from CIBC and Scotia Bank.
- Automated Categorization: Assigns transactions to categories using a categories.json file with customizable keywords.
- Google Sheets Integration: Automatically uploads transactions to a specified Google Sheet, creating a streamlined financial
tracking process.
- Dynamic File Handling: Handles monthly bank statement files dynamically, supporting different file formats for each bank.

## Prerequisites
- Python 3.8+
- Required Python libraries:
	- os
	- csv
	- json
	- gspread
- Google Service Account credentials JSON file for accessing Google Sheets.
- A categories.json file with transaction categories and associated keywords.

### Installation

1. Clone the repository:
   ```bash
    git clone https://github.com/yourusername/finance-tracker.git
    cd finance-tracker
   ```

2. Install required Python packages:
   ```bash
   pip install gspread
   ```

3.	Place your Google Sheets service account credentials file in a secure location. By default, the app looks for this file at:
    ```
    ~/.config/gspread/service_account.json
    ```

4.	Create a categories.json file to define transaction categories and keywords:
    ```
    {
    "Food": ["restaurant", "grocery"],
    "Transport": ["uber", "gas"],
    "Entertainment": ["netflix", "cinema"],
    "Misc": []
    }
    ```

5. Set up a Google Cloud Service Account
   - Create a service account in Google Cloud Console
   - Generate and download a JSON key file
   - Share your Google Sheet with the service account email

### Configuration

1. Modify the files in Bank Statements to include your own bank and credit card transactions
2. Edit sort_cibc and sort_scotia functions to match your bank statements
3. Ensure your Google Sheet is named "Personal Finances" with a worksheet matching the month

## Usage

```bash
python main.py
```

## Customization

### Adding Categories
Modify the `categories` .json file to add or update transaction categories. Each category is defined with a list of keywords that trigger the categorization.

```
categories = {
    "Food: restaurants": ["tim hortons", "starbucks", "mcdonald's", ...],
    "Groceries": ["walmart", "costco", ...],
    # Add more categories as needed
}
```

## Example Output

### Sample console output during execution:
```
Processing files for January...
Processing file: Bank Statements/cibc_January.csv
('2024-01-10', 'Grocery Store', 50.75, 'Food')
('2024-01-15', 'Gas Station', 30.00, 'Transport')
Successfully uploaded 2 transactions.

Processing files for February...
No files found for February. Skipping...
```

## Error Handling

- Missing Files: Skips months with no corresponding bank statement files.
- Invalid Transactions: Transactions without a description or amount are categorized as “uncategorized.”
- Google API Errors: Errors during upload are logged, and the process continues with other transactions.

## Security Notes

- Never commit your Google Cloud service account JSON key to version control
- Use environment variables or a secure configuration management system for sensitive credentials

## Limitations

- Currently supports only CIBC and Scotia Bank CSV formats
- Requires manual monthly updates
- Assumes a specific Google Sheets structure

## Contact

Lucas Patriquin: lucas.patriquin@gmail.com
