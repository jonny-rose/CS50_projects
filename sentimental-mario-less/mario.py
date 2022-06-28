from cs50 import get_int


def main():
    height = get_height()
    for i in range(height):
        for j in range(1, height + 1):
            if j < height - i:
                print(" ", end="")
            else:
                print("#", end="")
        print()


def get_height():
    while True:
        h = get_int("Height: ")
        if h > 0 and h <= 8:
            return h


if __name__ == "__main__":
    main()
