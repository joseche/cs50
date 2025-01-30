#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

// These are the values for each letter from a to z
const int VALUES[] = {1, 3, 3, 2,  1, 4, 2, 4, 1, 8, 5, 1, 3,
                      1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int letter_value(char l)
{
    int index;
    if (l >= 'a' && l <= 'z')
    {
        index = l - 'a';
    }
    else if (l >= 'A' && l <= 'Z')
    {
        index = l - 'A';
    }
    else
    {
        return 0;
    }
    return VALUES[index];
}

int calculate_word_score(string word)
{
    int len = strlen(word);
    char *s = word;
    int score = 0;
    for (int i = 0; i < len; i++)
    {
        score += letter_value(s[i]);
    }
    return score;
}

int main(void)
{
    // Prompt the user for two words
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Compute the score of each word
    int score1 = calculate_word_score(word1);
    int score2 = calculate_word_score(word2);

    // Print the winner
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score2 > score1)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}

