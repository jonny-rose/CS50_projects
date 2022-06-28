#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

bool only_digits(string s);
char rotate(char c, int n);

int main(int argc, string argv[])
{
    if (argc != 2 || only_digits(argv[1]) == false)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    int key = atoi(argv[1]);

    string text = get_string("plaintext: ");

    printf("ciphertext: ");
    for (int i = 0; i < strlen(text); i++)
    {
        printf("%c", rotate(text[i], key));
    }
    printf("\n");
    return 0;
}

bool only_digits(string s)
{
    for (int i = 0; i < strlen(s); i++)
    {
        if (!isdigit(s[i]))
        {
            return false;
        }
    }
    return true;
}

char rotate(char c, int n)
{
    if (isalnum(c))
    {
        if (islower(c))
        {
            return (c - 97 + n) % 26 + 97;
        }
        return (c - 65 + n) % 26 + 65;
    }
    return c;
}