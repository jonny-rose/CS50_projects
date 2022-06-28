#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

int count_letters(string text);
int count_words(string word);
int count_sentances(string sentance);

int main(void)
{
    string text = get_string("Text: ");
    int letters = count_letters(text);
    int words = count_words(text);
    int sentances = count_sentances(text);
    // printf("%i\n", letters);
    // printf("%i\n", words);
    // printf("%i\n", sentances);

    float L = letters / (float) words * 100;
    float S = sentances / (float) words * 100;
    int index = round(0.0588 * L - 0.296 * S - 15.8);
    // printf("L: %.2f, S: %.2f\n", L, S);

    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

int count_letters(string text)
{
    int length = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isalpha(text[i]))
        {
            length++;
        }
    }
    return length;
}

int count_words(string text)
{
    int words = 1;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isspace(text[i]))
        {
            words++;
        }
    }
    return words;
}

int count_sentances(string text)
{
    int sentances = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentances++;
        }
    }
    return sentances;
}