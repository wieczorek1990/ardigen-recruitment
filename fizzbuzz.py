#!/usr/bin/env python3


def fizzbuzz(number):
    multiple_of_three = number % 3 == 0
    multiple_of_five = number % 5 == 0
    if multiple_of_three and multiple_of_five:
        print('FizzBuzz')
    elif multiple_of_three:
        print('Fizz')
    elif multiple_of_five:
        print('Buzz')
    else:
        print(number)


def main():
    print('Please input n:')
    n = int(input())
    print('Please input m:')
    m = int(input())
    input_ok = 1 <= n < m <= 10000
    if not input_ok:
        print('Invalid input')
        exit(1)
    print('Result:')
    for number in range(n, m + 1):
        fizzbuzz(number)


if __name__ == '__main__':
    main()
