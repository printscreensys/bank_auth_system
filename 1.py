#BASELINE
import random
print('1. Create an account')
print('2. Log into account')
print('0. Exit')
iin = '400000'
card_numbers = list(i for i in range(10000000,10100000))
accounts = {}
n = int(input())
commands = []
in_account = False
commands.append(n) 
while n != 0:
    if n == 1:
        if in_account == False:
            print('Your card has been created')
            print('Your card number:')
            card_number = iin + str(card_numbers.pop(0))+str(random.randint(10,99))
            print(card_number)
            print('Enter your PIN:')
            pin = random.randint(1000, 9999)
            print(pin)
            accounts[card_number] = pin
            accounts.update({
                int(card_number):pin
            })
        else:
            print('Balance: 0')
    if n == 2:
        if in_account == False:
            print('Enter your card number:')
            login = int(input())
            print('Enter your PIN:')
            password = int(input())
            try: 
                if password == accounts[login]:
                    print('You have successfully logged in!')
                    in_account = True
                else:
                    print('Wrong card number or PIN!')
            except KeyError:
                print('Wrong card number or PIN!')
        else:
            print('You have successfully logged out!')
    if in_account == False:
        print('1. Create an account')
        print('2. Log into account')
        print('0. Exit')
        n = int(input())
    else:
        print('1. Balance')
        print('2. Log out')
        print('0. Exit')
        n = int(input())

else:
    print('Bye!')
