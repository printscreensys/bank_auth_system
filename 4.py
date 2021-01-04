import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute('''DROP TABLE IF EXISTS card;''')
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

def Luhn_check(card_number):
    sum = 0
    num_digits = len(card_number)
    oddeven = num_digits & 1
    for count in range(0, num_digits):
        digit = int(card_number[count])
        if not (( count & 1 ) ^ oddeven ):
            digit = digit * 2
        if digit > 9:
            digit = digit - 9
        sum = sum + digit
    if sum % 10 == 0:
        return True
    else:
        return False

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
            cur.execute('SELECT balance FROM card WHERE number = {}'.format(card_number))
            print('Balance: {}'.format(cur.fetchall()[0][0]))
    if n == 2:
        if not in_account:
            print('Enter your card number:')
            login = input()
            print('Enter your PIN:')
            password = input()
            cur.execute('SELECT number, pin FROM card WHERE number = {}'.format(login))
            check_data = cur.fetchall()
            if check_data != []:
                if (login, password) == check_data[0]:
                    print('You have successfully logged in!')
                    in_account = True
                    card_number = login
                else:
                    print("Wrong card number or PIN!")
            else:
                print("Wrong card number or PIN!")
        else:
            print('Enter income:')
            income = int(input())
            cur.execute("""
                UPDATE card SET balance = {} WHERE number = {} """.format('balance+'+ str(income), card_number))
            conn.commit()
            #print(card_number)
            print('Income was added!')
    if n == 3:
        print('Transfer')
        print('Enter card number')
        recipient = input()
        cur.execute('SELECT number FROM card WHERE number = {}'.format(recipient))
        enough_money = None
        same = None
        luhn_check = None
        exist = None
        if card_number == recipient:
            print("You can't transfer money to the same account!")
        elif not Luhn_check(recipient):
            print("Probably you made a mistake in the card number. Please try again!")
        elif cur.fetchall() != []:
            print('Enter how much money you want to transfer:')
            transfer_sum = int(input())
            cur.execute('SELECT balance FROM card WHERE number = {}'.format(card_number))
            if transfer_sum > cur.fetchall()[0][0]:
                print("Not enough money!")
            else:
                cur.execute('UPDATE card SET balance = {} WHERE number = {}'.format('balance-'+str(transfer_sum), card_number))
                conn.commit()
                cur.execute('UPDATE card SET balance = {} WHERE number = {}'.format('balance+'+str(transfer_sum), recipient))
                conn.commit()
                print('Success!')
        else:
            print("Such a card does not exist.")

    if n == 4:
        cur.execute('''DELETE FROM card WHERE number = {}'''.format(card_number))
        conn.commit()
        in_account = False

    if n == 5:
        print('You have successfully logged out!')
        in_account = False

    if not in_account:
        print('1. Create an account')
        print('2. Log into account')
        print('0. Exit')
        n = int(input())
    else:
        print('1. Balance')
        print('2. Add icnome')
        print('3. Do transfer')
        print('4. Close account')
        print('5. Log out')
        print('0. Exit')
        n = int(input())

else:
    print('Bye!')