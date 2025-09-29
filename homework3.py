# CHECK WHETHER THE GIVEN NUMBER IS ARMSTRONG OR NOT

def armstrong(n) :
  result = 0
  order = len(str(n))
  
  while (n > 0) :
    digit = n % 10
    result = result + digit ** order
    n = n // 10
  return result

def check(a,b):
  if a == b :
    return True
  else :
    return False

n = int(input('Enter a number :- ')) 
x = check(n,armstrong(n))
if x == True :
  print(n , 'Is an Armstrong number')
else :
  print(n , 'Is not an Armstrong number')

# ARMSTRONG NUMBERS IN GIVEN RANGE

a = int(input('Enter range :- '))
for i in range(1,a+1) :
   x = check(i,armstrong(i))
   if x == True :
      print(i ,end = ' ')




  





