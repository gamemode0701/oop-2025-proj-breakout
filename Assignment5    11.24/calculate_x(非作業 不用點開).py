def main():
    while True:
        al = str(input('alphabet:'))
        high = int(input('y:'))
        option = str(input('a/l/r?'))
        if al == 'g':
            num = 62
        elif al == 'a':
            num = 110
        elif al == 'm':
            num = 158
        elif al == 'e1':
            num = 206
        elif al == 'o':
            num = 286
        elif al == 'v':
            num = 334
        elif al == 'e2':
            num = 382
        elif al == 'r':
            num = 436
        y = 220+6*(high-1)
        print('RESULT:')
        if option.find('a') >= 0:
            print('x' + str(num - 18))
            print('y' + str(y))
            print('x' + str(num - 12))
            print('y' + str(y))
            print('x' + str(num - 6))
            print('y' + str(y))
            print('x' + str(num))
            print('y' + str(y))
            print('x' + str(num + 6))
            print('y' + str(y))
            print('x' + str(num + 12))
            print('y' + str(y))
            print('x' + str(num + 18))
            print('y' + str(y))
        if option.find('l') != -1:
            print('x' + str(num - 18))
            print('y' + str(y))
            print('x' + str(num - 12))
            print('y' + str(y))
        if option.find('r') != -1:
            print('x' + str(num + 12))
            print('y' + str(y))
            print('x' + str(num + 18))
            print('y' + str(y))
        print('================================================')


if __name__ == '__main__':
    main()