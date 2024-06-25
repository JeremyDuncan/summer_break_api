import unittest
from flask import Flask
import pandas as pd
from io import BytesIO
import json
from summer_break_api import app, all_transactions_df 

################################################################################
##  TEST CSV DATA  ##
#####################
csv_data = """2020-07-01, Expense, 18.77, Fuel
              2020-07-04, Income, 40.00, 347 Woodrow
              2020-07-06, Income, 35.00, 219 Pleasant
              2020-07-12, Expense, 27.50, Repairs
              2020-07-15, Income, 25.00, Blackburn St.
              2020-07-16, Expense, 12.45, Fuel
              2020-07-22, Income, 35.00, 219 Pleasant
              2020-07-22, Income, 40.00, 347 Woodrow
              2020-07-25, Expense, 14.21, Fuel
              2020-07-25, Income, 50.00, 19 Maple Dr."""


################################################################################
##  API TEST CLASS  ##
######################
class APITestCase(unittest.TestCase):
    # ==========================================================================
    # Set up the test client
    # ---------------------- 
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        global all_transactions_df

    # ==========================================================================
    # Test uploading transactions
    # ---------------------------
    def test_upload_transactions(self):
        global csv_data
        response = self.app.post('/transactions', data={'data': (BytesIO(csv_data.encode('utf-8')), 'transactions.csv')}, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'File uploaded successfully', response.data)

    # ==========================================================================
    # Test getting report after uploading transactions
    # ------------------------------------------------
    def test_get_report_after_transactions(self):
        global csv_data
        
        self.app.post('/transactions', data={'data': (BytesIO(csv_data.encode('utf-8')), 'transactions.csv')}, content_type='multipart/form-data')
        response = self.app.get('/report')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("gross-revenue", data)
        self.assertIn("expenses", data)
        self.assertIn("net-revenue", data)
        self.assertEqual(data["gross-revenue"], "$225.00")
        self.assertEqual(data["expenses"], "$72.93")
        self.assertEqual(data["net-revenue"], "$152.07")


################################################################################
##  Execute Test  ##
####################
if __name__ == '__main__':
    unittest.main()
