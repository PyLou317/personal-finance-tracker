import csv
import gspread
import time

month = 'January'
files = [f'cibc_{month}.csv', f'scotia_{month}.csv']

transactions = []

# Dictionary of categories and their corresponding keywords
categories = {
    "Food: restaurants": ["tim hortons", "starbucks", "mcdonald's", "nando's", "starbucks", "cactus", "earls", "table bistro", "chipotle",
                          "NOVO PIZZERIA", "skobi", "sushi", "kisoji", "a&w", "restaurant", "wendy's", "joey", "boathouse", "barely merchant",],
    "Groceries": ["walmart", "wal-mart", "costco wholesale", "save on foods", "meridian", "lepp farm", "freshco", "fresh st", "core culture",
                  "superstore",],
    "Car: gas": ["husk", "shell", "petro canada", "chevron", "7-eleven", "circle k", "costco gas"],
    "Car: maintenance": ["mobile 1", "perfection auto",],
    "Car: Parking": ["parking",],
    "Car: payment": ["ia auto",],
    "Insurance": ["bcca", "bcca-membership"],
    "Shopping": ["golf town", "home depot", "amzn", "ikea", "under armour", "canadian tire", "shoppers drug mart", "amazon", "rona",
                 "seven oaks", "WINNERSHOMESENSE", "LULULEMON", ],
    "Personal Care": ["barber", "haides",],
    "Fitness/Health": ["supplement king", "gym", "momentous", "goodlife", ],
    "Subscriptions": ["apple.com", "equifax", "spotify", "beamjobs",],
    "Phone": ["telus mobility"],
    "Travel": ["air can", "airbnb", "uber"],
    "Entertainment": ["cineplex"],
    "Credit Card Payment": ["payment", "mb-cibc",],
    "Credit Card Interest": ["interest"],
    "Interac E-transfer": ["e-transfer", ],
    "Income": ["aerotek", "school district no 35",],
    "Savings": ["bank the rest", ],
    "Strata Fees": ["itf bcs2236"],
    "Investments": ["wealthsimple"],
    "Bank Fees": ["monthly fees"]
    }

def categorize_transaction(name):
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword.lower() in name.lower():
                return category
    return "uncategorized"  # Default category if no keyword matches
    
    
def sort_transactions(file):
    transactions.clear()
    with open(file, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)

        for row in csv_reader:
            date = row[0]
            name = row[3]
            amount = float(row[1])
            
            # Check if the file is CIBC and invert the amount if necessary
            if 'cibc' in file.lower():
                if amount > 0:
                    amount = -amount
                else:
                    amount = abs(amount)  # Make negative amounts positive
                 
            category = categorize_transaction(name)            
            transaction = ((date, name, amount, category))
            print(transaction)
            transactions.append(transaction)
    return transactions
    

# Authenticate and open the Google Sheet
sa = gspread.service_account()
sh = sa.open("Personal Finances")
wks = sh.worksheet(f"{month}")


# Process each CSV file and upload to Google Sheets
row_number = 7  # Starting row number
for file in files:
    transactions = sort_transactions(file)
    for transaction in transactions:
        try:
            # Validate data before updating
            if len(transaction) == 4:
                print(f"Updating row {row_number} with data: {transaction}")
                wks.update(values=[[transaction[0], transaction[1], transaction[3], transaction[2]]], range_name=f'A{row_number}:D{row_number}')
                row_number += 1
                time.sleep(2)
            else:
                print(f"Skipping transaction due to insufficient data: {transaction}")
        except Exception as e:
            print(f"Error updating row {row_number} with data {transaction}: {e}")