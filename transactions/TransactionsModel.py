
import os
import random
from datetime import datetime, timedelta

import pandas as pd

# ---------------------
# Configurations
# ---------------------
INPUT_FILE = os.path.expanduser("~/TEMP/junction_data/final_transaction_table.csv")

CATEGORY_LIST = [
    "Housing", "Transportation", "Food", "Utilities", "Clothing",
    "Insurance", "Household Items/Supplies", "Education", 
    "Savings", "Gifts/Donations", "Entertainment", "Pension"
]

POSITIVE_MOOD_MSG = [
    "Well done!",
    "Keep the good work"
]

NEGATIVE_MOOD_MSG = [
    "We can do better. Let's remind our goals!",
    "Not so good, we need to improve or savings"
]
# ---------------------


class TransactionsModel:

    def __init__(self):
        print("- loading model ...")
        # Load Transactions
        _data_df = pd.read_csv(INPUT_FILE, sep=";")
        # Adjust time to year 2020
        _data_df['timestamp'] = _data_df.timestamp.apply(pd.to_datetime)
        _data_df['timestamp'] = _data_df.timestamp.apply(lambda x: x.date().replace(year = x.year + 4))
        # Add category to past transactions
        _data_df['category'] = _data_df.amount.apply(lambda x: random.choice(CATEGORY_LIST))
        # Get only outcome transactions
        self.data_df = _data_df[_data_df.amount < 0]
        self.data_df['amount'] = - self.data_df.amount
        print("... done ...")
        
    def get_valid_categories(self):
        return CATEGORY_LIST

    def get_random_bank_account(self):
        # Returns random iban account
        return self.data_df.accountIban.sample().values[0]
    
    def get_report_data(self, user_iban, buckets, goals, current_date):
        report_data = {}
        # User transactions
        sel_transactions = self.data_df[self.data_df.accountIban == user_iban].copy().reset_index()
        sel_transactions['week_date'] = sel_transactions.timestamp.apply(lambda x: x - timedelta(days=x.weekday()))
        # Get past transactions        
        week_reference = current_date - timedelta(days=current_date.weekday())
        past_transactions = sel_transactions[sel_transactions.timestamp < current_date].copy()
        # Fiil missing days
        ref_days = pd.Series(pd.date_range(start=current_date - timedelta(days=200), end=current_date)).rename('timestamp').to_frame().set_index('timestamp')
        past_transactions = ref_days.join(past_transactions.set_index('timestamp')).reset_index()
        # Week date
        past_transactions['week_date'] = past_transactions.timestamp.apply(lambda x: x - timedelta(days=x.weekday()))
        # Weekly results
        week_results = past_transactions.groupby(['week_date']).amount.sum().to_frame()
        week_results['trend'] = week_results.rolling(window=4).mean()
        # Plot data - last 6 weeks + trend
        report_data['week_plot'] = week_results.iloc[-6:].copy()
        # Buckets
        oldest_week = min(sorted(past_transactions.week_date.unique())[-6:])
        _df = past_transactions[past_transactions.week_date > oldest_week]
        # Buckets score
        report_data['buckets'] = buckets
        report_data['bucket_transactions'] = _df.groupby('category').amount.sum().to_dict()
        report_data['buckets_score'] = {}
        for k in buckets:
            if k in report_data['bucket_transactions']:
                report_data['buckets_score'][k] = 1 if report_data['bucket_transactions'][k] < buckets[k] else -1
        # Report mood
        report_data['mood'] = sum(report_data['buckets_score'].values()) / len(report_data['buckets_score'].values())
        # Msg from mood
        if report_data['mood'] > 0:
            report_data['mood_msg'] = random.choice(POSITIVE_MOOD_MSG)
        else:
            report_data['mood_msg'] = random.choice(NEGATIVE_MOOD_MSG)
        # Reminder
        report_data['goal_reminder'] = random.choice([x['description'] for x in goals])

        return report_data
