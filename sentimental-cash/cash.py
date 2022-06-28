from cs50 import get_float


def main():
    money = get_money()

    quarters = calculate_quarters(money)
    money = round(money - quarters * 0.25, 2)

    dimes = calculate_dimes(money)
    money = round(money - dimes * 0.10, 2)

    nickles = calculate_nickles(money)
    money = round(money - nickles * 0.05, 2)

    pennies = calculate_pennies(money)
    money = round(money - pennies * 0.01, 2)

    coins = int(quarters + dimes + nickles + pennies)

    print(f'{coins}')


def get_money():
    while True:
        m = get_float("Cash owed: ")
        if m > 0:
            return m


def calculate_quarters(n):
    return int(n / 0.25)


def calculate_dimes(n):
    return int(n / 0.10)


def calculate_nickles(n):
    return int(n / 0.05)


def calculate_pennies(n):
    return int(n / 0.01)


if __name__ == "__main__":
    main()