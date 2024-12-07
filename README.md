# Personal Finance Transaction Processor

## Overview

This Python script automates the process of categorizing and uploading bank transactions from CSV files to a Google Sheets spreadsheet. It supports multiple bank file formats and provides an intelligent transaction categorization system.

## Features

- 🏦 Supports multiple bank CSV files (currently CIBC and Scotia)
- 🏷️ Intelligent transaction categorization
- 📊 Automatic upload to Google Sheets
- 💡 Customizable transaction categories
- 🔒 Secure service account authentication

## Prerequisites

### Dependencies
- Python 3.7+
- Required libraries:
  - `csv`
  - `gspread`
  - `time`

### Installation

1. Clone the repository:
   ```bash
   git clone https://your-repository-url.git
   cd your-project-directory
   ```

2. Install required Python packages:
   ```bash
   pip install gspread
   ```

3. Set up a Google Cloud Service Account
   - Create a service account in Google Cloud Console
   - Generate and download a JSON key file
   - Share your Google Sheet with the service account email

### Configuration

1. Update the `categories` dictionary in the script to match your spending patterns
2. Set the `month` variable to the current month
3. Modify the `files` list to include your bank CSV file names
4. Ensure your Google Sheet is named "Personal Finances" with a worksheet matching the month

## Usage

```bash
python transaction_processor.py
```

## Customization

### Adding Categories
Modify the `categories` dictionary to add or update transaction categories. Each category is defined with a list of keywords that trigger the categorization.

```python
categories = {
    "Food: restaurants": ["tim hortons", "starbucks", "mcdonald's", ...],
    "Groceries": ["walmart", "costco", ...],
    # Add more categories as needed
}
```

## Error Handling

The script includes basic error handling:
- Skips transactions with insufficient data
- Prints error messages for problematic transactions
- Includes a 2-second delay between Google Sheets updates to prevent rate-limiting

## Security Notes

- Never commit your Google Cloud service account JSON key to version control
- Use environment variables or a secure configuration management system for sensitive credentials

## Limitations

- Currently supports only CIBC and Scotia Bank CSV formats
- Requires manual monthly updates
- Assumes a specific Google Sheets structure

## Contact

Lucas Patriquin: lucas.patriquin@gmail.com
