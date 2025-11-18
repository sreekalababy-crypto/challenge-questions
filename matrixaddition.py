rows = int(input('Enter the number of rows : '))
cols = int(input('Enter the number of columns : '))
print('\nEnter the elements of the first matrix : ')
A = []
for i in range(rows) :
    row = []
    for j in range(cols) :
        value = int(input(f'A[{i}][{j}] : '))
        row.append(value)
    A.append(row)

print('\nEnter the elements of the second matrix : ')
B = []
for i in range(rows) :
    row = []
    for j in range(cols) :
        value = int(input(f'B[{i}][{j}] : '))
        row.append(value)
    B.append(row)

C = []
for i in range(rows) :
    row = []
    for j in range(cols) :
       row.append(A[i][j] + B[i][j])
    C.append(row)

print('\nResultant Matrix : ')
for row in C :
    print(row)