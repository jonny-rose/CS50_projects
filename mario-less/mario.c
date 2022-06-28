#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n;
    do
    {
        n = get_int("number: ");
    }
    while (n < 1 || n > 8);

    for (int i = 0; i < n; i++)
    {
        // Build the left pyramid
        for (int j = 1; j <= n; j++)
        {
            if (j < n - i)
            {
                printf(" ");
            }
            else
            {
                printf("#");
            }
        }
        // Print 2 empty spaces
        printf("  ");
        // Build the right pyramid
        for (int k = 0; k < n; k ++)
        {
            if (k <= i)
            {
                printf("#");
            }
        }
        printf("\n");
    }

}
