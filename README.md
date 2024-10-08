# Account Transfer

Account Transfer

## Description

small web app using Django that handles fund transfers between two accounts support importing a list of accounts with opening balances, querying these accounts, and transferring funds between any two accounts.

## Features

- Import accounts from CSV files
- List all accounts 
- Get account information
- Transfer funds between two accounts

## Extra Features

- list all Transfers page and API
- API Swagger documention
- Deployed on server (pythonanywhere.com)
- Added RESTFUL APIs
  
## Unit Testing Coverage report :
![Screenshot (63)](https://github.com/user-attachments/assets/6a24f049-49bb-47b5-a11c-08dd136fa9b8)
![Screenshot (64)](https://github.com/user-attachments/assets/b2192fcf-9b0f-47b5-a7b1-467810056877)

## Installation

1. Clone the repository: `git clone https://github.com/EslamQadri/Account-Transfer.git `
2. Navigate into the project directory: `cd Account-Transfer `
3. Install dependencies: `pip install -r requirements.txt`

## Admin 
### User Name : ESLAM
### Password :   1234 

# Endpoints

# the base URL on server is  and that is the swagger docs : https://eslamqadr1.pythonanywhere.com/ 

- `https://eslamqadr1.pythonanywhere.com/api/import_accounts_api` :  POST : That Import CSV files and insert it in database 
- `https://eslamqadr1.pythonanywhere.com/api/list_accounts_api`:     GET : get List of all accounts 
- `https://eslamqadr1.pythonanywhere.com/api/account_info_api/uuid/`:GET : get account info based on ID
- `https://eslamqadr1.pythonanywhere.com/api/send_money_api`:        POST : get List of all accounts
- `https://eslamqadr1.pythonanywhere.com/api/transaction_list_api`   GET : get List of all Transfers


# or in loaclhost the swaager docs is : http://127.0.0.1:8000/

- `http://127.0.0.1:8000/api/import_accounts_api `:  POST : That Import CSV files and insert it in database 
- `http://127.0.0.1:8000/api/list_accounts_api`:     GET : get List of all accounts 
- `http://127.0.0.1:8000/api/account_info_api/uuid/`:GET : get account info based on ID
- `http://127.0.0.1:8000/api/send_money_api`:        POST : get List of all accounts 
- `http://127.0.0.1:8000/api/transaction_list_api`   GET : get List of all Transfers


## Pages 

# In Server 

- `https://eslamqadr1.pythonanywhere.com/import` :     That Import CSV files and insert it in database 
- `https://eslamqadr1.pythonanywhere.com/list_accounts`:      : get List of all accounts 
- `https://eslamqadr1.pythonanywhere.com/account_info/uuid` :   get account info based on ID
- `https://eslamqadr1.pythonanywhere.com/send_money`:         : List of all accounts
- `https://eslamqadr1.pythonanywhere.com/list_transaction`    : List of all Transfers

  
# in localhost 

- `http://127.0.0.1:8000/import` :     That Import CSV files and insert it in database 
- `http://127.0.0.1:8000/list_accounts`:      : get List of all accounts 
- `http://127.0.0.1:8000/account_info/uuid` :   get account info based on ID
- `http://127.0.0.1:8000/send_money`:         : List of all accounts
- `http://127.0.0.1:8000/list_transaction`    : List of all Transfers





