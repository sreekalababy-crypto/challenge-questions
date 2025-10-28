class Expensetracker :
    def __init__(self) :
        self.expenses = []
    
    def add_expense(self,name,amount) :
        amount = float(amount)
        self.expenses.append((name,amount))
        print(f'expense added{name}-{amount:2f}')

    def view_expenses(self) :
        if not self.expenses :
            print('no expenses')
        else :
            print('Expense list:')
            for i,(name,amount) in enumerate(self.expenses,start = 1) :
               print(f'{i}.{name} - {amount:.2f}')

    def total_amount(self) :
        total = sum(amount for _, amount in self.expenses)
        print(f'Total Amount Spent:{total:.2f}')
        return total
       
def main() :
    tracker = Expensetracker()
    while True :
        print('Expense Tracker menu')
        print('1 .Add Expense\n2.View Expenses\n3.Total amount\n4.exit')
        ch =int(input('Enter your choice :'))
        if ch == 1 :
           name = input('Enter your Expense name :-')
           amount = input('Enter amount')
           tracker.add_expense(name,amount)
        elif ch == 2 :
           tracker.view_expense()
        elif ch == 3 :
            tracker.total_amount()
        elif ch == 4 :
            break
        else :
            print('Invalid choice')
main()
