#include <ctype.h>
#include <cs50.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    // Prompt the user for some text
    string text = get_string("Text: ");

    // Count the number of letters, words, and sentences in the text
    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);

    printf("Letters: %i\n", letters);
    printf("Words: %i\n", words);
    printf("Sentences: %i\n", sentences);


    // Compute the Coleman-Liau index

    // Print the grade level
}

bool is_alpha(char c)
{
    return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z');
}

int count_letters(string text)
{
    // Return the number of letters in text
    unsigned int total_letter_count = 0;
    char *s = text;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (is_alpha(s[i]))
        {
            total_letter_count++;
        }
    }
    return total_letter_count;
}

int count_words(string text)
{
    int n = strlen(text);
    char *s = text;
    unsigned int total_words = 0;
    for (int i = 0; i < n; i++)
    {
        if (s[i] == ' ')
        {
            total_words++;
        }
    }
    if (s[n-1]!=' '){
        total_words++; // count the last word
    }
    return total_words;
}

bool sentence_separator(char c){
    return (c=='!' || c=='.' || c=='?');
}

int count_sentences(string text)
{
    // Return the number of sentences in text
    int n = strlen(text);
    char *s = text;
    unsigned int total_sentences = 0;
    for (int i = 0; i < n; i++)
    {
        if (sentence_separator(s[i]))
        {
            total_sentences++;
        }
    }
    if (!sentence_separator(s[n-1])){
        total_sentences++; // count the last word
    }
    return total_sentences;


}