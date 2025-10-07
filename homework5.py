import random
ch = ['dragon','goblin','trolls','ghost','skeleton','spider']
enemy = random.choice(ch)
player = input('Enter your name : ')
php = 100
ehp = 100
turn = 1
p = ['attack','defend','heal']
print(f'{player} v/s {enemy}')
print(f'{player} Health point :{php} \n {enemy} Health point : {ehp}')
while php >= 0 and ehp >= 0 :
    print('Turn',turn)
    pch = random.choice(p)
    if (pch == 'attack') :
        edamage = random.randint(10,30)
        ehp = ehp - edamage
        pdamage = random.randint(10,35)
        php = php - pdamage
        print(f'{player} Health point :',{php})
        print(f'{enemy} Health point :',{ehp})
    elif (pch == 'defend') :
        pdamage = random.randint(10,35)
        pdamage = pdamage // 2
        php = php - pdamage
        print(f'{player} Health point :',{php})
        print(f'{enemy} Health point :',{ehp})
    elif (pch == 'heal') :
        pheal = random.randint(10,25)
        if php + pheal < 100 :
            php = php + pheal
        else :
            php = 100
        print(f'{player} Health point :',{php})
        print(f'{enemy} Health point :',{ehp})    
    turn += 1

if php <= 0 :
    print(f'GAME OVER !!! \n {enemy} Wins !!')
elif ehp <= 0 :
    print(f'GAME OVER !!! \n {player} Wins !!')
 
