import random
import os

"""
Handles all word-related tasks in the game.
    -Takes a large source word list and creates smaller lists for the game.
    -Provides a main 6-letter word for each round.
    -Checks if the player’s typed words are valid using the letters from the main word.
    -Makes sure words are correct length and contain only letters.
    -Can generate or update word lists if they are missing.
"""



# setup for files
# access the file location
currentFolder = os.path.dirname(os.path.abspath(__file__))
wordlistPath = currentFolder + "/wordlists"
sourcePath = wordlistPath + "/original_wordlist.txt"
sixLetterPath = wordlistPath + "/6letterwords.txt"
allWordsPath = wordlistPath + "/allwords.txt"


# function to make the list files if missing
def generateWordListsFromSource():
    if not os.path.exists(wordlistPath):
        os.makedirs(wordlistPath)

    try:
        # reading the source file manually
        f = open(sourcePath, "r")
        sixLetterList = []
        allWordsList = []

        for line in f:
            cleanWord = line.strip().lower()
            #this filter words with apostrophe
            if "'" in cleanWord: continue
            if not cleanWord.isalpha(): continue

            # sort words by length -
            length = len(cleanWord)
            if length >= 3 and length <= 6:
                allWordsList.append(cleanWord)
            if length == 6:
                sixLetterList.append(cleanWord)
        f.close()

        # writing the 6 letter file
        f2 = open(sixLetterPath, "w")
        # making it unique set then list and sort
        uniqueSix = sorted(list(set(sixLetterList)))
        f2.write("\n".join(uniqueSix))
        f2.close()

        # writing all words file
        f3 = open(allWordsPath, "w")
        uniqueAll = sorted(list(set(allWordsList)))
        f3.write("\n".join(uniqueAll))
        f3.close()

    except:
        print("error finding source file,,, check folder")


# helper to check file exist
def validate_file_name(fileNameInput):
    if not os.path.exists(fileNameInput):
        print("missing file.. generating now")
        generateWordListsFromSource()



# counting letters
# logic: turn string to list and remove letter if found
def manualCheckLetters(baseWordString, testWordString):
    baseCharList = list(baseWordString)
    testCharList = list(testWordString)

    for charItem in testCharList:
        if charItem in baseCharList:
            # remove found char so it cant be used again
            baseCharList.remove(charItem)
        else:
            return False
    return True


def getBaseWord(min_length=3, filename=sixLetterPath):
    validate_file_name(filename)

    f = open(filename, "r")
    lines = f.readlines()
    f.close()

    cleanList = []
    for w in lines:
        if w.strip().isalpha():
            cleanList.append(w.strip())

    while True:
        # picking random word
        randomBaseWord = random.choice(cleanList)

        # checking if it has enough answers
        validList = generateValidWordsFromBaseWord(randomBaseWord, min_length)
        # minimum 10 words required
        if len(validList) >= 10:
            return randomBaseWord


def generateValidWordsFromBaseWord(base_word, min_length=3, filename=allWordsPath):
    validate_file_name(filename)

    resultList = []
    f = open(filename, "r")
    allLines = f.readlines()
    f.close()

    for line in allLines:
        checkWord = line.strip()

        # logic to check length and letters
        if len(checkWord) >= min_length and checkWord.isalpha():
            # using my manual check function
            if manualCheckLetters(base_word, checkWord):
                resultList.append(checkWord)

    return resultList