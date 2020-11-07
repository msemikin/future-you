# Transactions Model

This module utilizes the synthetic data from "Junction 2020 - OP (Financial advisory)" challenge:
https://sandbox.apis.op-palvelut.fi/junction/v2020/datasets/transactions


# Model setup

1) copy the data synthetic data to the data folder
```
mkdir ~/TEMP/junction_data/
curl -o ~/TEMP/junction_data/transactions.zip https://sandbox.apis.op-palvelut.fi/junction/v2020/datasets/transactions
unzip ~/TEMP/junction_data/transactions.zip -d ~/TEMP/junction_data/
```

2) adjust configuration in TransactionsModel file, if needed. From the step above the following file is expected to exist:
```
~/TEMP/junction_data/final_transaction_table.csv
```