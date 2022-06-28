from cs50 import get_string


def main():
    text = get_string('Text: ')
    letters = count_letters(text)
    words = count_words(text)
    sentances = count_sentances(text)

    L = letters / words * 100
    S = sentances / words * 100
    index = round(0.0588 * L - 0.296 * S - 15.8)

    if index < 1:
        print('Before Grade 1')
    elif index >= 16:
        print('Grade 16+')
    else:
        print(f'Grade {index}')


def count_letters(text):
    letters = 0
    for i in range(len(text)):
        if text[i].isalnum():
            letters += 1
    return letters


def count_words(text):
    words = 1
    for i in range(len(text)):
        if text[i] == ' ':
            words += 1
    return words


def count_sentances(text):
    sentances = 0
    for i in range(len(text)):
        if text[i] == '.' or text[i] == '!' or text[i] == '?':
            sentances += 1
    return sentances


if __name__ == "__main__":
    main()