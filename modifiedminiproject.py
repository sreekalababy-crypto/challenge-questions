import sqlite3
from datetime import datetime
import sys

# ------------------------------------------
#       DATABASE INITIALIZATION
# ------------------------------------------
conn = sqlite3.connect("bank1.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers(
        customer_id VARCHAR(10) PRIMARY KEY,
        name VARCHAR(20) NOT NULL,
        password VARCHAR(20) NOT NULL,
        cibil_score INTEGER DEFAULT 650
)
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts(
        account_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id VARCHAR(10) NOT NULL,
        balance INTEGER DEFAULT 0,
        status VARCHAR(20) DEFAULT 'ACTIVE',
        FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
)
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions(
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_id INTEGER,
        type VARCHAR(20),
        amount FLOAT,
        date VARCHAR(20),
        FOREIGN KEY(account_id) REFERENCES accounts(account_id)
)
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS loan(
        loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id VARCHAR(10),
        amount FLOAT,
        status VARCHAR(20),
        FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
)
""")

conn.commit()



# ------------------------------------------
#              ADMIN FUNCTIONS
# ------------------------------------------
def admin_create_customer():
    try:
        conn = sqlite3.connect("bank1.db")
        cursor = conn.cursor()
        print("\n🆕 Creating New Customer 🧑‍💼")
        cid = input("Enter Customer ID: ")
        name = input("Enter Name: ")
        pwd = input("Enter Password: ")

        cursor.execute("INSERT INTO customers VALUES(?,?,?,?)",
                    (cid, name, pwd, 650))
        conn.commit()
        print("✅ Customer created successfully!")
    except:
        print("❌ Customer ID already exists!")
    finally :
        conn.close()

def admin_create_account():
    try:
        conn = sqlite3.connect("bank1.db")
        cursor = conn.cursor()
        print("\n🏦 Creating Bank Account")
        cid = input("Enter Customer ID: ")

        cursor.execute("SELECT * FROM customers WHERE customer_id=?", (cid,))
        if not cursor.fetchone():
            print("❌ Customer does not exist!")
            return

        cursor.execute("INSERT INTO accounts(customer_id) VALUES(?)", (cid,))
        conn.commit()
        print("🎉 Account created successfully!")
    except Exception as e:
        print("❌ Error:", e)
    finally :
        conn.close()

def admin_freeze_account():
    try:
        conn = sqlite3.connect("bank1.db")
        cursor = conn.cursor()
        print("\n❄️ Freeze Account")
        acc = input("Enter Account ID: ")
        cursor.execute("UPDATE accounts SET status='FROZEN' WHERE account_id=?", (acc,))
        conn.commit()
        print("🧊 Account Frozen Successfully!")
    except:
        print("❌ Error freezing account!")
    finally:
        conn.close()

def admin_activate_account():
    try:
        conn = sqlite3.connect("bank1.db")
        cursor = conn.cursor()
        print("\n🔓 Activate Account")
        acc = input("Enter Account ID: ")
        cursor.execute("UPDATE accounts SET status='ACTIVE' WHERE account_id=?", (acc,))
        conn.commit()
        print("✅ Account Activated Successfully!")
    except:
        print("❌ Error activating account!")
    finally:
        conn.close()

def admin_sanction_loans():
    try:
        conn = sqlite3.connect("bank1.db")
        cursor = conn.cursor()
        print("\n💰 Loan Approval Panel")
        cursor.execute("SELECT * FROM loan WHERE status='PENDING'")
        loans = cur.fetchall()

        if not loans:
            print("📭 No pending loan requests!")
            return

        for loan in loans:
            lid, cid, amount, status = loan
            print(f"\n Loan ID: {lid} |  Customer: {cid} |  Amount: {amount}")

            choice = input("Approve (A) / Reject (R): ").upper()
            if choice == "A":
                cur.execute("UPDATE loan SET status='APPROVED' WHERE loan_id=?", (lid,))
                print("✔ Loan Approved!")
            else:
                cur.execute("UPDATE loan SET status='REJECTED' WHERE loan_id=?", (lid,))
                print("❌ Loan Rejected!")

        conn.commit()
        print("📌 Loan processing completed!")
    except:
        print("❌ Error processing loans!")
    finally:
        conn.close()   


def admin_view_accounts():
    try:
        conn = sqlite3.connect("bank1.db")
        cursor = conn.cursor()
        print("\n📋 Viewing All Accounts (No Sensitive Details)")
        cursor.execute("SELECT account_id, customer_id, status FROM accounts")
        rows = cursor.fetchall()

        if not rows:
            print("📭 No accounts found!")
            return

        print("\nAccount ID   |   Customer ID   |   Status")
        print("-------------------------------------------")

        for r in rows:
            print(f"{r[0]:<13} | {r[1]:<14} | {r[2]}")

    except:
        print("❌ Error fetching accounts!")
    finally:
        conn.close()



# ------------------------------------------
#           CUSTOMER FUNCTIONS
# ------------------------------------------
def check_frozen(account_id):
    conn = sqlite3.connect("bank1.db")
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM accounts WHERE account_id=?", (account_id,))
    status = cursor.fetchone()[0]
    return status == "FROZEN"


def deposit(account_id):
    try :
        conn = sqlite3.connect("bank1.db")
        cursor = conn.cursor()
        if check_frozen(account_id):
            print("🧊 Account Frozen. Visit nearest branch to activate!")
            return

        amt = float(input("Enter amount to deposit: "))
        cursor.execute("UPDATE accounts SET balance = balance + ? WHERE account_id=?",
                (amt, account_id))

        cursor.execute("INSERT INTO transactions(account_id,type,amount,date) VALUES(?,?,?,?)",
                (account_id, "DEPOSIT", amt, str(datetime.now())))

        conn.commit()
        print("🎉 Deposit successful!")
    except Exception as e :
        print('❌ Error : ',e)
    finally :
        conn.close()

def withdraw(account_id):
    try :
        conn = sqlite3.connect("bank1.db")
        cursor = conn.cursor()
        if check_frozen(account_id):
           print("🧊 Account Frozen. Visit nearest branch!")
           return

        amt = float(input("Enter amount to withdraw: "))

        cursor.execute("SELECT balance FROM accounts WHERE account_id=?", (account_id,))
        bal = cursor.fetchone()[0]

        if amt > bal:
           print("❌ Insufficient balance!")
           return

        cursor.execute("UPDATE accounts SET balance = balance - ? WHERE account_id=?",
                (amt, account_id))

        cursor.execute("INSERT INTO transactions(account_id,type,amount,date) VALUES(?,?,?,?)",
                (account_id, "WITHDRAW", amt, str(datetime.now())))

        conn.commit()
        print("💰 Withdrawal successful!")

    except Exception as e :
           print('❌ Error : ',e)
    
    finally :
           conn.close()



def apply_loan(customer_id):
    try:
        conn = sqlite3.connect("bank1.db")
        cursor = conn.cursor()
        print("\n💳 Loan Application")
        amt = float(input("Enter loan amount: "))

        cursor.execute("""
            SELECT COUNT(*) FROM transactions
            WHERE account_id IN (
                SELECT account_id FROM accounts WHERE customer_id=?
            )
        """, (customer_id,))

        trans_count = cur.fetchone()[0]

        cursor.execute("SELECT cibil_score FROM customers WHERE customer_id=?", (customer_id,))
        cibil = cur.fetchone()[0]

        print(f"\nYour CIBIL Score: {cibil}")
        print(f"Your Total Transactions: {trans_count}")

        if cibil >= 650 and trans_count >= 3:
            status = "PENDING"
            print("📝 Loan request submitted for admin approval.")
        else:
            status = "REJECTED"
            print("❌ Loan rejected (low CIBIL or few transactions).")

        cursor.execute("INSERT INTO loan(customer_id,amount,status) VALUES(?,?,?)",
                    (customer_id, amt, status))
        conn.commit()
    except:
        print("❌ Error applying for loan!")
    finally :
        conn.close()


# ------------------------------------------
#               LOGIN MENUS
# ------------------------------------------
def customer_menu(customer_id):
    while True:
        print("\n==== 👤 CUSTOMER MENU ====")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Apply Loan")
        print("4. Logout")

        ch = input("👉 Enter choice: ")

        if ch == "1":
            acc = input("Enter Account ID: ")
            deposit(acc)
        elif ch == "2":
            acc = input("Enter Account ID: ")
            withdraw(acc)
        elif ch == "3":
            apply_loan(customer_id)
        elif ch == "4":
            print("👋 Logged out!")
            break
        else:
            print("❌ Invalid choice!")


def customer_login():
    try :
        conn = sqlite3.connect("bank1.db")
        cursor = conn.cursor()
        print("\n🔐 CUSTOMER LOGIN")
        cid = input("Customer ID: ")
        pwd = input("Password: ")

        cursor.execute("SELECT * FROM customers WHERE customer_id=? AND password=?", (cid, pwd))
        if cursor.fetchone():
            print("✅ Login Successful!")
            customer_menu(cid)
        else:
            print("❌ Invalid Login!")
    except Exception as e :
            print('Error : ',e)

    finally :
        conn.close()



def admin_menu():

    while True:
        print("\n====== 🛠️ ADMIN MENU ======")
        print("1. Create Customer")
        print("2. Create Account")
        print("3. Freeze Account")
        print("4. Activate Account")
        print("5. Sanction Loans")
        print("6. View Accounts")
        print("7. Logout")

        ch = input("👉 Enter choice: ")

        if ch == "1":
            admin_create_customer()
        elif ch == "2":
            admin_create_account()
        elif ch == "3":
            admin_freeze_account()
        elif ch == "4":
            admin_activate_account()
        elif ch == "5":
            admin_sanction_loans()
        elif ch == "6":
            admin_view_accounts()
        elif ch == "7":
            print("👋 Admin Logged out!")
            break
        else:
            print("❌ Invalid choice!")



# ------------------------------------------
#                MAIN SYSTEM
# ------------------------------------------

def main() :
    
    while True:
        print("\n🏦 === WELCOME TO SMART BANK SYSTEM === 🏦")
        print("1. Admin Login")
        print("2. Customer Login")
        print("3. Exit")

        c = input("👉 Enter choice: ")
        if c == "1" :
           admin_menu()
        elif c == "2" :
           customer_login()
        elif c == "3" :
           print("👋 Thank you for using Smart Bank!")
           sys.exit()
        else :
           print("❌ Invalid choice!")

main()