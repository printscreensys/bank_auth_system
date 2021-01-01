#WITH LUHN
import random

class Account:
    def __init__(self):
        self.logged = False

    def Luhn(self,card_num):
        card_num = list(card_num)
        card_num = [int(i) for i in card_num]
        for i in range(len(card_num)):
            if i%2 == 0:
                card_num[i] = card_num[i]*2
            if card_num[i]>9:
                card_num[i] -= 9
        
        if sum(card_num) % 10 == 0:
            return 0
        else:
            return 10-(sum(card_num)%10)
        
    def set_card(self):
        iin = '400000'
        card_num = random.randint(1, 1000000000)
        if card_num < 100000000:
            self.card = '0'*(8-len(str(card_num)))+str(card_num)
        else:
            self.card = str(card_num)
        self.card = iin+self.card+str(self.Luhn(iin+self.card))

        return self.card

    def set_pin(self):
        pin_num = random.randint(0, 9999)
        if pin_num < 1000:
            self.pin = '0'*4-len(str(pin_num))+str(pin_num)
        else:
            self.pin = str(pin_num)
        
        return self.pin

    def log_out():
        return 'You have successfully logged out!'

print('1. Create an account')
print('2. Log into account')
print('0. Exit')
n = int(input())
in_account = False
accounts = []

while n != 0:
    if n == 1:
        accounts.append(Account())
        if in_account == False:
            print('Your card has been created')
            print('Your card number:')
            card_number = accounts[-1].set_card()
            print(card_number)
            print('Enter your PIN:')
            pin = accounts[-1].set_pin()
            print(pin)
        else:
            print('Balance: 0')
    if n == 2:
        if in_account == False:
            print('Enter your card number:')
            login = input()
            print('Enter your PIN:')
            password = input()
            if login == accounts[-1].card and password == accounts[-1].pin:
                print('You have successfully logged in!')
                in_account = True
            else:
                print('Wrong card number or PIN!')
        else:
            print('You have successfully logged out!')
            in_account = False
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