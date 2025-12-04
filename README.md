

## Project Overview
Title: Text Twist Game
Description:
    The player starts by selecting EASY or HARD level, then a random set of 6 letters appears. The timer starts automatically. 
    The player types words into the textbox and presses Enter. Words must be 3–6 letters long and must be valid based on the word list. Points are earned based on word length.



## Code Organization
.py file
    ui.py               -Handles the graphical interface and user interactions.
    texttwistgame.py    -Manages game rules, scoring, word validation, and timer.
    words.py            -Generates word lists, validates words, and provides base words for the game.
    app.py	            -Main class of the game. Creates TextTwistUI and TextTwistGame objects.

.txt file
    highscore.txt           – This file keeps the player’s best score.
    (Inside wordlist directory)
    original_wordlist.txt   – This is the the source words we downloaded from the internet. Before filtering it
                            - Retrieve from SCOWL dictionary downloaded from https://diginoodles.com/projects/eowl
    6letterwords.txt        – This file contains all the 6-letter words we can make. After filtering it
    allwords.txt            – This file contains all the possible words we can make from the 6-letter base word

.png (inside images directory)
    1.png	- image for EASY button.
    2.png	- image for HARD button.



## Directories arrangment
│
├─ app.py              # Main to run the game
├─ ui.py               # GUI tkinter
├─ texttwistgame.py    # Game logic
├─ words.py            # Word list validation
├─ highscore.txt       # Stores highest score
├─ wordlists/          # Word lists folder
│    ├─ original_wordlist.txt   # Original word source
│    ├─ 6letterwords.txt        # Six-letter words
│    └─ allwords.txt            # Words of length 3-6
└─ images/             # Images for UI buttons
     ├─ 1.png          # EASY button image
     └─ 2.png          # HARD button image



## How to Run
1. Make sure all files are in the folder structure above.
2. Make sure to tkinter is installed
3. Run app.py to start the game.



