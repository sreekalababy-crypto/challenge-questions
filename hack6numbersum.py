n = int(input('Enter the number of terms : '))
num = input('Enter the numbers').split()
numbers = []
result = []
for i in num :
   numbers.append(int(i))
   for i in numbers :
      number = i
      sum = 0
      while i > 0 :
         d = i % 10
         sum = sum + d
         i = i // 10
      result.append(sum)
   numbers = result
print(numbers) 


      
   



