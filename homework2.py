# CREATE A LIST OF FIRST 100 NUMBERS

num = []
even = []
odd = []
divisibles = []
for i in range (1,101) :
    num.append(i)
print('NUMBERS ARE :- ',num)

# CREATE A LIST FOR ALL EVEN NUMBERS
# CREATE A LIST FOR ALL ODD NUMBERS

for i in num :
        if i % 2 == 0 :
              even.append(i)
        else :
              odd.append(i)
print('EVEN NUMBERS ARE  :- ',even)
print('ODD NUMBERS ARE :- ',odd)

#  CREATE A LIST FOR NUMBERS THAT ARE DIVISIBLE BY BOTH 5 AND 3

for i in num :
      if i % 5 == 0 and i % 3 == 0 :
            divisibles.append(i)
print('DIVISIBLES ARE :- ',divisibles)