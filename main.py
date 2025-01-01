import os
import csv
import gspread
import os
import json

# Global Variables
MONTHS = [
    "January", "February", "March", "April", "May", "June", 
    "July", "August", "September", "October", "November", "December"
    ]
FOLDER = 'Bank Statements'

# Load categories only once 
def load_categories():
    with open('categories.json', 'r') as f:
        return json.load(f)

CATEGORIES = load_categories() 

# (Helper function) Load category json file and categorize transaction based on description
def categorize_transaction(name):
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword.lower() in name.lower():
                return category
    return "uncategorized"  # Default category if no keyword matches

# Reformat CIBC credit card statements to align with Google Sheets upload
def format_cibc(file):
    transactions = []
    with open(file, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)

        for row in csv_reader:
            date = row[0]
            
            # Check for no description in row index 3
            if row[1] == '':
                name = "No Description"
            else:
                name = row[1]
                
            # Use index 3 if there is a 6th column
            if len(row) == 5:
                if row[2] == '':
                    amount = 0 
                # Return amount as a negative
                else:   
                    amount = -float(row[2])
            else:
                amount = -float(row[3])
                 
            category = categorize_transaction(name)            
            transaction = ((date, name, amount, category))
            print(transaction)
            transactions.append(transaction)
    return transactions

# Reformat Scotia bank statements to align with Google Sheets upload
def format_scotia(file):
    transactions = []
    with open(file, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)

        for row in csv_reader:
            if len(row) < 4:  # Skip rows with fewer than 4 columns
                print(f"Skipping malformed row: {row}")
                continue

            date = row[0]
            name = row[3] if row[3] != '' else "No Description"
            amount = float(row[1])
            category = categorize_transaction(name)
            transaction = (date, name, amount, category)
            print(f"Parsed transaction: {transaction}")
            transactions.append(transaction)
    return transactions

def sort_transactions(file):
    transactions = []
    
    if "scotia" in file.lower():
        transactions.extend(format_scotia(file))  # Use `extend` to add flat transactions
    elif "cibc" in file.lower():
        transactions.extend(format_cibc(file))
    
    return transactions

# Authenticate and open the Google Sheet
def auth_gsheets(month):
    try:
        credentials_path = os.getenv("GOOGLE_SHEETS_CREDENTIALS", "/Users/lucaspatriquin/.config/gspread/service_account.json")
        sa = gspread.service_account(filename=credentials_path)
        sh = sa.open("Personal Finances")
        
        try:
            wks = sh.worksheet(month)
            return wks
        except gspread.exceptions.WorksheetNotFound:
            print(f"Worksheet for {month} not found.")
            return None
    
    except Exception as e:
        print(f"Error: {e}")
        raise

# Process each CSV file and batch upload to Google Sheets to work around Google API limits
def upload_to_gsheets(worksheet, transactions):
    starting_row = 7  # Starting row number

    # Prepare data for batch update
    data = [
        [transaction[0], transaction[1], transaction[3], transaction[2]]
        for transaction in transactions if len(transaction) == 4
    ]

    if not data:
        print("No valid transactions to upload.")
        return

    # Determine the range for the batch update
    range_name = f"A{starting_row}:D{starting_row + len(data) - 1}"

    try:
        worksheet.update(range_name, data)
        print(f"Successfully uploaded {len(data)} transactions.")
    except Exception as e:
        print(f"Failed to upload transactions: {e}")

def main():
    for month in MONTHS:
        print(f"Processing files for {month}...")  # Log progress
        
        # Create file paths dynamically
        files = [f'{FOLDER}/cibc_{month}.csv', f'{FOLDER}/scotia_{month}.csv']
        
        # Check if any files exist for this month
        existing_files = [file for file in files if os.path.exists(file)]
        
        if not existing_files:
            print(f"No files found for {month}. Skipping...")
            continue  # Skip to the next month
        
        # Authenticate Google Sheets for the current month
        worksheet = auth_gsheets(month)
        
        # Process and upload transactions for existing files
        for file in existing_files:
            print(f"Processing file: {file}")
            transactions = sort_transactions(file)
            upload_to_gsheets(worksheet, transactions)

        
if __name__ == "__main__":
    main()