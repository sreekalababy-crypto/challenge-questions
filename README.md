miniproject01.py 
README FILE
Bank Management System – Python + SQLite3
A command-line banking application written in Python using SQLite3.
This system supports customer registration, login, multi-account management, transactions, loan processing, and admin access.

📌 Features
👤 Customer Module
Customer Registration
Customer Login
Customer Menu:
Open new bank account (Savings / Current)
Deposit money
Withdraw money
View all transaction history
Apply for loans based on:
CIBIL Score
Total number of transactions
💰 Account Management
A customer can hold multiple accounts
Account Status:
Active
Freezed (admin-controlled; frozen accounts block transactions)
Balance updates on every deposit/withdrawal
All transactions recorded with timestamp
🏦 Loan System
Loan approval depends on:

CIBIL Score	Transactions Required	Loan Amount	Interest Rate
≥ 750	0	₹5,00,000	7.5%
650–749	≥ 5	₹2,50,000	8.5%
550–649	≥ 10	₹1,00,000	10%
All approved loans are stored in the loans table.

🛡️ Admin Module
Admin Login (Username: admin, Password: admin123)
View all customer details
(You can add account freeze/activate features if needed)
🗄️ Database Structure
customers
Field	Type	Description
customer_id	TEXT	Primary Key
name	TEXT	Customer name
password	TEXT	Login password
accounts
Field	Type	Description
account_id	INTEGER	Primary Key
customer_id	TEXT	Foreign Key
account_type	TEXT	Savings / Current
balance	REAL	Account balance
status	TEXT	Active / Freezed
transactions
Field	Type	Description
transaction_id	INTEGER	Primary Key
account_id	INTEGER	Foreign Key
transaction_type	Deposit / Withdraw	
amount	REAL	
transaction_date	TEXT	
loans
Field	Type	Description
loan_id	INTEGER	Primary Key
customer_id	TEXT	Foreign Key
loan_amount	REAL	
interest_rate	REAL	
status	Approved / Rejected	
approved_date	TEXT	
▶️ How to Run the Program
1. Install Python 3
Make sure Python is installed:

python --version
2. Run the Script
python bank_system.py
3. Main Menu Options
==== BANK SYSTEM ====
1. Register
2. Login
3. Admin Login
4. Exit
🧪 Testing the System
Customer Registration
Enter new customer ID: C101
Enter name: Rahul
Enter password: rahul123
Login
Enter customer ID: C101
Enter password: rahul123
Admin Login
Admin username: admin
Admin password: admin123
📂 File Included
bank_system.py – Main application
bank.db – SQLite database (auto-created)
README.md – Documentation (this file)
📌 Notes
Do not delete bank.db, it stores all customers, accounts, and loans.
Account status control (freeze/activate) can be added to the admin menu.
All database queries use exception handling to prevent crashes.
