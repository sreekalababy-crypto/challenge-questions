def roman_to_int(s) :
    roman_map = {'I' : 1,'V' : 5,'X' : 10,'L' : 50,'C' : 100,'D' : 500,'M' : 1000}
    result = 0
    for i in range(len(s)):
        if (i + 1) < len(s) and roman_map[s[i]] < roman_map[s[i+1]] :
            result -= roman_map[s[i]]
        else :
            result += roman_map[s[i]]
    return result
roman_input = input('Enter the roman number : ')
result = roman_to_int(roman_input)
print(f'The integer value of {roman_input} is : {result}')
