import threading
import os
from time import sleep
from tkinter import StringVar
from words import *

"""
This handles the game logic.
    -Keeps track of the score and words typed by the player.
    -Manages the timer and ends the game when time runs out.
    -Checks and finds valid words from the word list efficiently.
    -Controls the game flow for starting, resetting, and ending rounds.
"""

gameTimer = 180

#Class for tracking the remaining time, can start, stop, reset, and notify when time is up
class Clock:
    def __init__(self, startTime=120):
        self.displayTime = StringVar()
        self.startTime = startTime
        self.countDownTime = startTime
        self.timeIsOver = []  # list for function to call

        self.stopTimerFlag = False
        self.resetTimerFlag = False

        self.displayTime.set(str(self))

    # Returns the current countdown time in seconds
    def getTimeLeft(self):
        return self.countDownTime

    # Set a new time limit for the countdown and update display
    def setTimeLimit(self, new_time):
        self.startTime = new_time
        self.countDownTime = new_time
        self.displayTime.set(str(self))

    # Starts the countdown timer  in seconds
    def startTimer(self):
        self.stopTimerFlag = False
        self.countDownTime = self.startTime
        self.displayTime.set(str(self))

        while True:
            # check if need reset
            if self.resetTimerFlag:
                self.countDownTime = self.startTime
                self.resetTimerFlag = False

            # check if stop
            if self.stopTimerFlag:
                self.stopTimerFlag = False
                break

            self.countDownTime -= 1
            self.displayTime.set(str(self))

            # time reach zero, call function
            if self.countDownTime == 0:
                self.timeIsUp()
                break

            sleep(1)

    # Call all functions in the timeIsOver list when the timer reaches zero
    def timeIsUp(self):
        for functionCall in self.timeIsOver:
            functionCall()

    # Immediately stops the timer and sets countdown to zero
    def stopTimer(self):
        self.countDownTime = 0
        self.stopTimerFlag = True
        self.displayTime.set(str(self))

    # Resets the timer to the original start time (without starting it)
    def resetTimer(self):
        self.countDownTime = self.startTime
        self.displayTime.set(str(self))

    # Sets a flag to reset the timer during countdown (used in startTimer loop)
    def resetWhileRunning(self):
        self.resetTimerFlag = True

    def __str__(self):
        # calculating minute and seconds
        #To display the timer in a readable MM:SS format
        return "{}:{}".format(self.countDownTime // 60,
                              str(self.countDownTime % 60).zfill(2))


class TextTwistGame:
    def __init__(self):
        self.clock = Clock(gameTimer)
        self.clock.timeIsOver.append(self.timeIsUp)
        self.clock_thread = None
        self.ui_callbacks = {}

        self.highestScore = {"highestScore": 0}
        self.loadHighScore()

        self.gameLetters = []
        # this list will hold sorted words
        self.possibleWordAnswer = []
        self.enteredWordsFromUser = set()
        self.currentScoreDisplayUI = 0

        self.resetGame()

    # sorting algorithm,,, split the list into half
    def mergeSortAlgo(self, arrayInput):
        if len(arrayInput) <= 1:
            return arrayInput

        middleIndex = len(arrayInput) // 2
        leftArr = self.mergeSortAlgo(arrayInput[:middleIndex])
        rightArr = self.mergeSortAlgo(arrayInput[middleIndex:])

        return self.mergeArrays(leftArr, rightArr)

    # helper to put back the list together
    def mergeArrays(self, leftArr, rightArr):
        sortedResult = []
        leftIndex = 0
        rightIndex = 0

        # loop while both have elements
        while leftIndex < len(leftArr) and rightIndex < len(rightArr):
            if leftArr[leftIndex] < rightArr[rightIndex]:
                sortedResult.append(leftArr[leftIndex])
                leftIndex += 1
            else:
                sortedResult.append(rightArr[rightIndex])
                rightIndex += 1

        # add the remaining item
        sortedResult.extend(leftArr[leftIndex:])
        sortedResult.extend(rightArr[rightIndex:])
        return sortedResult

    # finding word using binary search
    def binarySearchAlgo(self, sortedList, targetWord):
        lowIndex = 0
        highIndex = len(sortedList) - 1

        while lowIndex <= highIndex:
            midIndex = (lowIndex + highIndex) // 2
            guessWord = sortedList[midIndex]

            if guessWord == targetWord:
                return True
            if guessWord > targetWord:
                highIndex = midIndex - 1
            else:
                lowIndex = midIndex + 1
        return False

    def loadHighScore(self):
        try:
            if os.path.exists("highscore.txt"):
                f = open("highscore.txt", "r")
                content = f.read().strip()
                if content:
                    self.highestScore["highestScore"] = int(content)
                f.close()
        except:
            self.highestScore["highestScore"] = 0

    def updateHighScore(self):
        # check if score is higher
        if self.currentScoreDisplayUI > self.highestScore["highestScore"]:
            self.highestScore["highestScore"] = self.currentScoreDisplayUI
            # saving the new high score to txt
            f = open("highscore.txt", "w")
            f.write(str(self.highestScore["highestScore"]))
            f.close()

    def getHighScore(self):
        return self.highestScore["highestScore"]

    def getScore(self):
        return self.currentScoreDisplayUI

    def getLetters(self):
        return self.gameLetters

    def getWordList(self):
        return self.possibleWordAnswer

    def checkWord(self, word):
        # check if word already typed by user
        if word in self.enteredWordsFromUser:
            return False

        # using binary search to check if word exist in valid list
        isWordValid = self.binarySearchAlgo(self.possibleWordAnswer, word)

        if isWordValid:
            self.enteredWordsFromUser.add(word)
            self.currentScoreDisplayUI += len(word)
            # stop timer if all word found
            if len(self.enteredWordsFromUser) == len(self.possibleWordAnswer):
                self.clock.stopTimer()
            return True
        return False

    def levelPassed(self):
        # loop to find if 6 letter word exist
        for word in self.enteredWordsFromUser:
            if len(word) == 6:
                return True
        return False

    def getMissingWords(self):
        # finding word that are missing manually
        missingList = set()
        for word in self.possibleWordAnswer:
            if word not in self.enteredWordsFromUser:
                missingList.add(word)
        return missingList

    def startClock(self):
        if self.clock_thread and self.clock_thread.is_alive():
            self.clock.resetWhileRunning()
        else:
            self.clock_thread = threading.Thread(target=self.clock.startTimer)
            self.clock_thread.daemon = True
            self.clock_thread.start()

    def resetClock(self):
        self.clock.resetTimer()

    def timeIsUp(self):
        for func in list(self.ui_callbacks.values()):
            func()

    def addUIUpdate(self, name, func):
        self.ui_callbacks[name] = func

    def startGame(self, difficulty="EASY"):
        self.enteredWordsFromUser = set()

        if difficulty == "HARD":
            timeLimit = 120
            minLen = 5
        else:
            timeLimit = 180
            minLen = 3

        self.clock.setTimeLimit(timeLimit)

        baseWordStr = getBaseWord(minLen)
        self.gameLetters = list(baseWordStr)

        # getting the words
        rawWordsList = list(generateValidWordsFromBaseWord(baseWordStr, minLen))

        # calling sort function
        self.possibleWordAnswer = self.mergeSortAlgo(rawWordsList)

        self.startClock()

    def resetGame(self):
        self.possibleWordAnswer = []
        self.enteredWordsFromUser = set()
        self.currentScoreDisplayUI = 0
        self.gameLetters = []
        self.resetClock()