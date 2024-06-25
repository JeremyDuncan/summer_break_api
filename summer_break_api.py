from flask import Flask, request, jsonify
import pandas as pd
from io import StringIO

app = Flask(__name__)
all_transactions_df = pd.DataFrame(columns=["Date", "Type", "Amount", "Memo"])

################################################################################
##  ENDPOINTS  ##
#################
# ==============================================================================
# POST Endpoint: handles uploading of transactions (CSV File)
# -----------------------------------------------------------
@app.route('/transactions', methods=['POST'])
def upload_transactions():
    global all_transactions_df
    if 'data' not in request.files:
        return "No file part", 400
    
    file = request.files['data']
    if file.filename == '':
        return "No selected file", 400
    
    if file:
        # Read uploaded file into a StringIO object
        data = StringIO(file.stream.read().decode("UTF8"), newline=None)
        # Clean raw CSV data
        cleaned_data = clean_csv_data(data.getvalue())
        # Read cleaned data into a DataFrame, specifying column names
        all_transactions_df = pd.read_csv(StringIO(cleaned_data), sep=",", names=["Date", "Type", "Amount", "Memo"])
        # Filter out columns with no data from new_transactions_df
        all_transactions_df = all_transactions_df.dropna(axis=1, how='all')
        print_transaction_results(all_transactions_df)      

        return "File uploaded successfully", 200

# ==============================================================================
# GET Endpoint: generates a report from the transactions
# ------------------------------------------------------
@app.route('/report', methods=['GET'])
def get_report():
    global all_transactions_df
    gross_revenue = all_transactions_df[all_transactions_df['Type'] == 'Income']['Amount'].sum()
    expenses = all_transactions_df[all_transactions_df['Type'] == 'Expense']['Amount'].sum()
    net_revenue = gross_revenue - expenses

    return jsonify({
        "gross-revenue": f"${gross_revenue:.2f}",
        "expenses": f"${expenses:.2f}",
        "net-revenue": f"${net_revenue:.2f}"
    })


################################################################################
##  HELPER FUNCTIONS  ##
########################
# ==============================================================================
# Cleans CSV data. Removes comments and whitespace
# ------------------------------------------------
def clean_csv_data(data):
    cleaned_data = []
    for line in data.splitlines():
        # Ignore lines that are empty or start with '#'
        if line.strip() and not line.startswith('#'):
            try:
                # Split up data and strip whitespace
                date, type_, amount, memo = line.split(',', 3)
                cleaned_data.append(f"{date.strip()},{type_.strip()},{amount.strip()},{memo.strip()}")
            except ValueError:
                # Skip lines that don't have correct number of columns
                pass
    return "\n".join(cleaned_data)

# ==============================================================================
# Prints output of transactional data in API
# ------------------------------------------
def print_transaction_results(all_transactions_df):
    print('  ')
    print('All Transactions: ')
    print('===============================================================')
    print(all_transactions_df)
    print('  ')

    
################################################################################
## Execute Flask App  ##
########################
if __name__ == '__main__':
    # Run server in debug mode
    app.run(debug=True)
