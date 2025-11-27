📖 Wordlist Preparation
Our TextTwist game relies on two dictionary files:
6letterwords.txt → contains only six‑letter words, used to generate the puzzle’s base word.
allwords.txt → contains all valid words between 3–6 letters, used to validate player guesses.

Instead of typing words manually, we download a large free dictionary file from https://diginoodles.com/projects/eowl (SCOWL) and then filter it using this Python script.

import os

SOURCE_FILE = "english_words.txt"   # big dictionary file you downloaded
SIX_LETTER_FILE = "6letterwords.txt"
ALL_WORDS_FILE = "allwords.txt"

MIN_WORD_LENGTH = 3
MAX_WORD_LENGTH = 6

six_letter_words = []
all_words = []

with open(SOURCE_FILE, "r", encoding="utf-8") as f:
    for line in f:
        word = line.strip().lower()   # clean and normalize to lowercase
        if word.isalpha():            # keep only alphabetic words
            if MIN_WORD_LENGTH <= len(word) <= MAX_WORD_LENGTH:
                all_words.append(word)        # add 3–6 letter words
            if len(word) == 6:
                six_letter_words.append(word) # add exactly 6‑letter words

# Save results into two files
with open(SIX_LETTER_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(sorted(set(six_letter_words))))

with open(ALL_WORDS_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(sorted(set(all_words))))

print(f"Created {SIX_LETTER_FILE} with {len(six_letter_words)} words")
print(f"Created {ALL_WORDS_FILE} with {len(all_words)} words")

# This script takes a large dictionary file (english_words.txt) and filters it into two smaller
# wordlists for the game: one containing only six-letter words (6letterwords.txt) and another
# containing all valid words between 3–6 letters (allwords.txt). It reads each line, cleans it
# (lowercase, alphabetic only), checks the word length, and then saves it into the appropriate
# list. Finally, duplicates are removed, the words are sorted alphabetically, and the results
# are written into the two text files, ready for use by the TextTwist game.

