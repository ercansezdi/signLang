__auther__  = "Ercan Sezdi"
__email__   = "ercansezdi007@gmail.com"
__version__ = "0.9"
__status__  = "homework"

from random import randint

def set_number():
    value = str(randint(1,9))
    while str(len(value)) != '4':
        add = False
        lenght = int(len(value))
        new_value = str(randint(0,9))
        control_number = 0
        while lenght > 0:
            if new_value == value[lenght-1]:
                break
            else:
                control_number += 1
            lenght -= 1
        if control_number == int(len(value)):
            value += new_value
    return value

def control_number(value,value_two): # return True or False , True: it's have value, False: it's not have value
    for i in range(0,4):
        if value_two[i] == value:
            return True
        else:
            pass
    return False


if __name__ == "__main__":
    number = set_number()
    print('Number :',number)

    while number != True:
        value = input('\nMake your guess:')
        dog = 0
        cat = 0
        if int(value) < 1000 or int(value) > 9999:
            print('Please make a 4-digit number guess')
        else:
            if str(value) == str(number):
                print('Congratulations! You have made the correct guess!')
                exit(0)
            for i in range(0,4):
                if str(value)[i] == str(number)[i]:
                    print(str(value)[i],'is correct at the correct location')
                    dog += 1
                else:
                    answer = control_number(str(value)[i],str(number))
                    if answer == True:
                        print(str(value)[i],'is correct at the wrong location')
                        cat += 1

            print( 'You have {} dogs and {} cats'.format(dog,cat))


