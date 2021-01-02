import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute('''DROP TABLE IF EXISTS card;''')
#conn.commit()
cur.execute('''CREATE table card(
        id INTEGER, 
        number TEXT, 
        pin TEXT, 
        balance INTEGER DEFAULT 0
        )''')
conn.commit()

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
            self.card = '0'*(9-len(str(card_num)))+str(card_num)
        else:
            self.card = str(card_num)
        self.card = iin+self.card+str(self.Luhn(iin+self.card))

        return self.card

    def set_pin(self):
        pin_num = random.randint(0, 9999)
        if pin_num < 1000:
            self.pin = '0'*(4-len(str(pin_num)))+str(pin_num)
        else:
            self.pin = str(pin_num)

        return self.pin

    def log_out(self):
        return 'You have successfully logged out!'

print('1. Create an account')
print('2. Log into account')
print('0. Exit')
n = int(input())
in_account = False
accounts = []
i = 0

while n != 0:
    if n == 1:
        acc = Account()
        if in_account == False:
            print('Your card has been created')
            print('Your card number:')
            card_number = acc.set_card()
            print(card_number)
            print('Your PIN:')
            pin = acc.set_pin()
            print(pin)
            cur.execute(
                '''
                INSERT INTO 
                    card (id, number, pin, balance)
                VALUES 
                    ({},{},{},{})
                '''.format(i, card_number, pin, "0")
            )
            conn.commit()
            i += 1
        else:
            cur.execute('SELECT * FROM card')
            print('Balance: {}'.format(cur.fetchall()[-1][3]))
    if n == 2:
        if not in_account:
            print('Enter your card number:')
            login = input()
            print('Enter your PIN:')
            password = input()
            cur.execute('SELECT pin FROM card WHERE number = {}'.format(login))
            try:
                check_pin = cur.fetchall()[0][0]
                if password == check_pin:
                    print('You have successfully logged in!')
                    in_account = True
                else:
                    print("Wrong card number or PIN!")
            except IndexError:
                print("Wrong card number or PIN!")
        else:
            print('You have successfully logged out!')
            in_account = False
    if not in_account:
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