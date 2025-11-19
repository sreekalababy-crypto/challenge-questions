import sqlite3
from datetime import datetime
import sys 


conn = sqlite3.connect('bank.db')
cursor = conn.cursor()
cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers(
                       customer_id VARCHAR(10) PRIMARY KEY,
                       name VARCHAR(20) NOT NULL,
                       email_id VARCHAR(30),
                       date_of_birth VARCHAR(20),
                       password VARCHAR(20) NOT NULL)
            ''')
        
cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts(
                       account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       customer_id VARCHAR(10),
                       account_type VARCHAR(20),
                       balance INTEGER DEFAULT 0,
                       status VARCHAR(20) DEFAULT 'Active',
                       FOREIGN KEY(customer_id) REFERENCES customers(customer_id))  
            ''')
        
cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions(
                       transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       account_id INTEGER,
                       transaction_type VARCHAR(20),
                       amount INTEGER,
                       transaction_date VARCHAR(20),
                       FOREIGN KEY(account_id)
                       REFERENCES accounts(account_id))
            ''')

cursor.execute('''
            CREATE TABLE IF NOT EXISTS loans(
                       loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       customer_id VARCHAR(10),
                       loan_amount INTEGER,
                       interest_rate FLOAT,
                       status VARCHAR(20),
                       approved_date VARCHAR(20),
                       FOREIGN KEY(customer_id) REFERENCES customers(customer_id))
                ''')
conn.commit()
conn.close()


# ------------------------------------------------------------
#                     CUSTOMER REGISTRATION
# -----------------------------------------------------------

def register_customer() :
    try :
        conn = sqlite3.connect('bank.db')
        cursor = conn.cursor()

        cid = input('Enter new customer ID : ')

        name = input('Enter name : ')

        email = input('Enter Email : ')

        date_of_birth = input('Enter Date of birth : ')
        
        password = input('Enter password: ')

        cursor.execute(
            '''INSERT INTO customers VALUES (?,?,?,?,?)''',(cid,name,email,date_of_birth,password)
            )
        conn.commit()

        print('✅Registration successful.')

    except Exception as error:
        print('⚠Customer ID already exists.',error)

    except Exception as e :
        print('❌Error: ',e) 

    finally :
        conn.close()


# ------------------------------------------------------------
#                       CUSTOMER LOGIN
# ------------------------------------------------------------

def customer_login() :
    try :
        conn = sqlite3.connect('bank.db')
        cursor = conn.cursor()

        cid = input('Enter customer ID : ')
        password = input('Enter password : ')

        cursor.execute('''
            SELECT * FROM customers WHERE customer_id = ? AND password = ? ''', (cid,password)
                        )
        
        if cursor.fetchone() :
            print('✅ Login successful.')

        # customer menu selection

            customer_menu(cid)
        else :
            print('❌Invalid credentials.')

    except Exception as e :
        print('Error : ',e)

    finally :
        conn.close()

# --------------------------------------------------------------
#                      CUSTOMER MENU
# --------------------------------------------------------------

def customer_menu(cid) :
    while True :
        print('\n------CUSTOMER MENU------')
        print('1. Open Account')
        print('2. Deposit')
        print('3. Withdraw')
        print('4. View Transactions')
        print('5. Apply for Loan')
        print('6. Logout')

        choice = input('Enter the choice : ')

        if choice == '1' :
            open_account(cid)
        elif choice == '2' :
            deposit(cid)
        elif choice == '3' :
            withdraw(cid) 
        elif choice == '4' :
            view_transactions(cid)
        elif choice == '5' :
            loan_application(cid)
        elif choice == '6' :
            break
        else :
            print('⚠  Invalid option.')
            
# ---------------------------------------------------------------
#                      ACCOUNT FUNCTIONS
# ---------------------------------------------------------------

def open_account(cid) :
    try :
        conn = sqlite3.connect('bank.db')
        cursor = conn.cursor()

        acc_type = input('Enter account type (Savings/Current) : ')

        cursor.execute('''
                         INSERT INTO accounts (customer_id , account_type , balance , status)
                    VALUES(?,?,?,?)''',(cid ,acc_type,0,'Active')
                           )
        conn.commit()

        print('✅ Account created successfully.')

    except Exception as e :
        print('❌ Error : ,e')    
    finally :
        conn.close()

# ---------------------------------------------------------------
#                           DEPOSIT
# ---------------------------------------------------------------

def deposit(cid) :
    try :
        conn = sqlite3.connect('bank.db')
        cursor = conn.cursor()

        acc_id = input('Enter your account ID : ')
        amount = float(input('Enter deposit amount : '))

        cursor.execute('''
                       SELECT balance,status FROM accounts WHERE account_id = ? AND customer_id = ?''',(acc_id,cid)
                       )
        acc = cursor.fetchone()

        if not acc :
            print('❌ Account not found.')
            return
        if acc[1] != 'Active' :
            print('⚠ Account is not active(Freezed/Closed).Deposit denied.')
            return
       
        new_balance = acc[0] + amount

        cursor.execute('''
                           UPDATE accounts SET balance = ? WHERE account_id = ?''',(new_balance,acc_id)
                           )
        cursor.execute('''
                           INSERT INTO transactions (account_id,transaction_type,amount,transaction_date) 
                           VALUES (?,'Deposit',?,?)''',(acc_id,amount,datetime.now())
                           )
        conn.commit()
        print('✅ Deposit successful.')
        
    except Exception as e :
        print('❌ Error : ',e)
    finally :
        conn.close()

# ----------------------------------------------------------------
#                         WITHDRAW
# ----------------------------------------------------------------

def withdraw(cid) :
    try :
        conn = sqlite3.connect('bank.db')
        cursor = conn.cursor()

        acc_id = input('Enter your account ID : ')
        amount = float(input('Enter withdrawal amount : '))

        cursor.execute('''
                       SELECT balance,status FROM accounts WHERE account_id = ? AND customer_id = ? ''',(acc_id,cid)
                       )
        acc = cursor.fetchone()
        if not acc :
            print('❌ Account not found.')
            return
        if acc[1] != 'Active' :
            print('⚠ Account is not active (Freezed/Closed). Withdraw denied.')
            return
        if acc[0] >= amount :
            new_balance = acc[0] - amount
            cursor.execute('''
                               UPDATE accounts SET balance = ? WHERE account_id = ?''',(new_balance,acc_id)
                               )
            cursor.execute('''
                               INSERT INTO transactions(account_id,transaction_type,amount,transaction_date)
                               VALUES(?,'Withdraw',?,?)''',(acc_id,amount,datetime.now())
                               )
            conn.commit()
            print('✅ Withdrawal successful.')
        else :
            print('⚠ Insufficient funds.')

    except Exception as e :
        print('❌ Error : ',e)
    
    finally :
        conn.close()

# ---------------------------------------------------------------
#                      VIEW TRANSACTIONS
# ---------------------------------------------------------------

def view_transactions(cid) :
    try :
        conn = sqlite3.connect('bank.db')
        cursor = conn.cursor()

        acc_id = input('Enter your account ID : ')

        cursor.execute('''
                       SELECT transaction_id,transaction_type,amount,transaction_date FROM transactions WHERE account_id = ?''',(acc_id,)
                       )
        
        rows = cursor.fetchall()
        if rows :
            print('\n----TRANSACTION HISTORY----')
            for row in rows :
                print(f'Transaction ID : {row[0]}   Transaction Type : {row[1]}   Amount  :  {row[2]}   Transaction Date  :  {row[3]} ')
        else :
            print('⚠ No transactions found.')

    except Exception as e :
        print('❌ Error : ',e)
    finally :
        conn.close()

# ----------------------------------------------------------------
#                       LOAN APPLICATION
# ----------------------------------------------------------------

def loan_application(cid) :
    try :
        conn = sqlite3.connect('bank.db')
        cursor = conn.cursor()

        cibil = int(input('Enter your CIBIL score (300 - 900) : '))

        # COUNT ALL TRANSACTIONS OF CUSTOMER
        cursor.execute('''
                       SELECT COUNT(*) FROM transactions WHERE account_id IN ( SELECT 
                       account_id FROM accounts WHERE customer_id = ?)
                       ''',(cid,))
        trans_count = cursor.fetchone()[0]
        
        print(f'Total Transactions : {trans_count}')

        eligible = False
        amount = 0
        rate = 0

        if cibil >= 750 :
            eligible = True
            amount = 500000
            rate = 7.5
        elif 650 <= cibil < 750 and trans_count >= 5 :
            eligible = True
            amount = 250000
            rate = 8.5
        elif 550 <= cibil < 650 and trans_count >= 10 :
            eligible = True 
            amount = 100000
            rate = 10.0

        if eligible :
            cursor.execute('''
                           INSERT INTO loans(customer_id , loan_amount , interest_rate , status , approved_date)
                           VALUES(?,?,?,'Approved',?)''',(cid,amount,rate,datetime.now())
                           )
            conn.commit()
            print(f'✅ Loan Approved for Rs.{amount} at {rate}% Interest!')
        else :
            print('❌ Sorry, you are not eligible for a loan based on your current score/transactions.')

    except Exception as e :
        print('Error : ',e)

    finally :
        conn.close()

# -----------------------------------------------------------------
#                          ADMIN LOGIN
# -----------------------------------------------------------------
        
def admin_login() :
    user = input('Enter admin username : ')
    password = input('Enter admin password : ' )

    if user == 'admin' and password == 'admin123' :
        print('✅ Admin login successful.')

        # admin menu selection

        admin_menu()
    else :
        print('❌ Invalid Admin Credentials.')

# -----------------------------------------------------------------
#                    ADMIN MENU(NO CRUD ACCESS)
# -----------------------------------------------------------------


def admin_menu() :
    while True :
        print('\n------ADMIN MENU------')
        print('1. View All Customers ')
        print('2. Logout')
        
        choice = input('Enter the choice : ')

        if choice == '1' :
            view_all_customers()
        elif choice == '2' :
            break
        else :
            print('⚠ Invalid option.')

def view_all_customers() :
    try :
        conn = sqlite3.connect('bank.db')
        cursor = conn.cursor()
        
        cursor.execute('''
                       SELECT customer_id,name FROM customers '''
                       )
        customers = cursor.fetchall()

        print('\n----ALL CUSTOMERS----')
        for c in customers :
            print(f'Customer ID : {c[0]}   Name : {c[1]}')

    except Exception as e :
        print('❌ Error : ',e)
    finally :
        conn.close()

# ------------------------------------------------------------------
#                           MAIN MENU
# ------------------------------------------------------------------

def main() :
    while True :
        print('\n===== BANK ACCOUNT MANAGEMENT SYSTEM =====')
        print('1. Register Customer')
        print('2. Customer Login')
        print('3. Admin Login')
        print('4. Exit')

        choice = input('Enter the choice : ')

        if choice == '1' :
            register_customer()
        elif choice == '2' :
            customer_login()
        elif choice == '3' :
            admin_login() 
        elif choice == '4' :
            print('Goodbye 👋')
            sys.exit()
        else :
            print('⚠ Invalid Choice.')
main()