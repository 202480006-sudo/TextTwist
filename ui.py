import tkinter as tk
import random
from string import ascii_lowercase, ascii_uppercase
import os


"""
ui.py – Handles all user interface.

All visual elements and user interactions are controlled in this file.
- Displaying letters, timer, score, and word list.
- Input box for typing words.
- Buttons for EASY/HARD difficulty, Reset, and Start.
- Updating the UI during gameplay 
- Visual popup for missing words, final score, exit button, game rule.
"""

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 800


class TextTwistUI:
    def __init__(self):
        self.__root = tk.Tk()
        self.__root.title("TextTwist Game")
        self.__root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.__root.configure(bg="white")

        # grid setup
        self.__root.columnconfigure(0, weight=1)
        self.__root.rowconfigure(0, weight=1)

        #Score
        self.high_score = 0
        self.btn_easy = None
        self.btn_hard = None
        self.current_difficulty = "EASY"

        # making the frames
        self.createStartPage()
        self.createGamePage()

        # grid the start page
        self.start_page_frame.grid(row=0, column=0, sticky="nsew")
        self.game_page_frame.grid_remove()

        self.initializeKeyBindings()
        self.setDifficulty("EASY")

    """
       SCREEN 1 GUI
            function for the 1st interface of the gain,
            this contain the game title, the level of hard and easy
            button, and the start game button
    """

    def createStartPage(self):
        self.start_page_frame = tk.Frame(self.__root, bg="white")
        self.start_page_frame.columnconfigure(0, weight=1)

        # rows setup
        self.start_page_frame.rowconfigure(0, weight=1)
        self.start_page_frame.rowconfigure(1, weight=0)
        self.start_page_frame.rowconfigure(2, weight=0)
        self.start_page_frame.rowconfigure(3, weight=0)
        self.start_page_frame.rowconfigure(4, weight=0)
        self.start_page_frame.rowconfigure(5, weight=1)

        # title part
        f1 = tk.Frame(self.start_page_frame, bg="white")
        f1.grid(row=1, column=0, pady=(0, 10))

        txt = "TEXT TWIST"
        idx = 0
        for c in txt:
            if c == " ":
                tk.Label(f1, text=" ", bg="white", width=1).grid(row=0, column=idx)
            else:
                l = tk.Label(f1, text=c, font=("Calibri", 30, "bold"),
                             bg="#262626", fg="white", relief="raised", borderwidth=5,
                             width=2, height=1)
                l.grid(row=0, column=idx, padx=4)
            idx += 1

        # choosing level area
        f2 = tk.Frame(self.start_page_frame, bg="white")
        f2.grid(row=2, column=0, pady=10)

        curr = os.path.dirname(os.path.abspath(__file__))

        # easy button
        easyF = tk.Frame(f2, bg="white")
        easyF.grid(row=0, column=0, padx=40)

        try:
            p = os.path.join(curr, "images", "1.png")
            self.easy_img_tk = tk.PhotoImage(file=p)
            l = tk.Label(easyF, image=self.easy_img_tk, bg="white", bd=0)
            l.grid(row=0, column=0, sticky="ew")
        except:
            tk.Label(easyF, text="[IMG]", bg="white", fg="red").grid(row=0, column=0)

        self.btn_easy = tk.Button(easyF, text="EASY LEVEL", font=("Calibri", 12, "bold"), cursor="hand2",
                                  bg="#E4DFD7", fg="#232323", relief="raised",
                                  command=lambda: self.setDifficulty("EASY"))
        self.btn_easy.grid(row=1, column=0, pady=0, ipady=3, ipadx=20)

        # hard button
        hardF = tk.Frame(f2, bg="white")
        hardF.grid(row=0, column=1, padx=40)

        try:
            p2 = os.path.join(curr, "images", "2.png")
            self.hard_img_tk = tk.PhotoImage(file=p2)
            l2 = tk.Label(hardF, image=self.hard_img_tk, bg="white", bd=0)
            l2.grid(row=0, column=0, sticky="ew")
        except:
            tk.Label(hardF, text="[IMG]", bg="white", fg="red").grid(row=0, column=0)

        self.btn_hard = tk.Button(hardF, text="HARD LEVEL", font=("Calibri", 12, "bold"), cursor="hand2",
                                  bg="#E4DFD7", fg="#232323", relief="raised",
                                  command=lambda: self.setDifficulty("HARD"))
        self.btn_hard.grid(row=1, column=0, pady=0, ipady=3, ipadx=20)


        # start game button
        self.main_start_btn = tk.Button(self.start_page_frame, text="START GAME", font=("Calibri", 15, "bold"),
                                        bg="#6D2932", fg="white", relief="raised", borderwidth=5,
                                        activebackground="black", activeforeground="white", cursor="heart",
                                        command=self.startGameSession)
        self.main_start_btn.grid(row=4, column=0, ipadx=20, ipady=3, pady=(70, 0))

    def setDifficulty(self, mode):
        self.current_difficulty = mode
        if self.btn_easy is None: return

        # swapping colors, when button is clicked it changes to black bg, when unclick its white
        if mode == "EASY":
            self.btn_easy.config(bg="#181716", fg="white", relief="sunken")
            self.btn_hard.config(bg="#E4DFD7", fg="#232323", relief="raised")
        else:
            self.btn_easy.config(bg="#E4DFD7", fg="#232323", relief="raised")
            self.btn_hard.config(bg="#181716", fg="white", relief="sunken")

    def createGamePage(self):
        self.game_page_frame = tk.Frame(self.__root, bg="white")
        self.game_page_frame.columnconfigure(0, weight=1)
        self.game_page_frame.rowconfigure(0, weight=1)

        # main container
        main = tk.Frame(self.game_page_frame, bg="white")
        main.grid(column=0, row=0, ipadx=5, ipady=10, sticky="nsew", padx=50, pady=50)

        # header section
        self.header_pane = tk.Frame(main, bg="white")
        self.header_pane.grid(row=0, column=0, sticky="nsew", padx=12, pady=(0, 10))
        self.header_pane.columnconfigure(0, weight=1)
        self.header_pane.columnconfigure(1, weight=1)
        self.header_pane.columnconfigure(2, weight=1)

        # creating header buttons - RULES, SCORE, EXIT
        b1 = tk.Button(self.header_pane, text="📜 Rules", command=self.openRulesPopup,
                       font=("Calibri", 12, "bold"), bg="#181716", fg="white",
                       relief="raised", borderwidth=3, cursor="heart")
        b1.grid(row=0, column=0, sticky="w", ipadx=10)

        b2 = tk.Button(self.header_pane, text="🏆 High Score", command=self.openHighScorePopup,
                       font=("Calibri", 12, "bold"), bg="#181716", fg="white",
                       relief="raised", borderwidth=3, cursor="heart")
        b2.grid(row=0, column=1, sticky="n", ipadx=10)

        b3 = tk.Button(self.header_pane, text="❌ Exit", command=self.__root.destroy,
                       font=("Calibri", 12, "bold"), bg="#181716", fg="white",
                       relief="raised", borderwidth=3, cursor="heart")
        b3.grid(row=0, column=2, sticky="e", ipadx=10)

        # The top box container below the button header
        self.top_pane = tk.Frame(main, relief="ridge", borderwidth=4, width=WINDOW_WIDTH,
                                 height=300, bg="#E4DFD7",
                                 highlightbackground="#181716", highlightthickness=0)
        self.top_pane.grid(row=1, column=0, sticky="nsew", padx=12, pady=(5, 5), ipadx=50)

        # bottom area for inputs
        self.bottom_pane = tk.Frame(main, relief="ridge", borderwidth=4, width=WINDOW_WIDTH,
                                    height=300, bg="#E4DFD7",
                                    highlightbackground="#181716", highlightthickness=0)
        self.bottom_pane.grid(row=2, column=0, sticky="nsew", padx=12, pady=(5, 10), ipadx=50)
        self.bottom_pane.columnconfigure(0, weight=1)
        self.bottom_pane.rowconfigure(0, weight=1)

        # frame inside bottom pane
        tf = tk.Frame(self.bottom_pane, relief="flat", borderwidth=0, bg="#E4DFD7")
        tf.grid(row=0, column=0, sticky="nsew")

        tf.rowconfigure(0, weight=1)
        tf.rowconfigure(1, weight=0)
        tf.rowconfigure(2, weight=0)
        tf.rowconfigure(3, weight=0)
        tf.rowconfigure(4, weight=1)
        tf.columnconfigure(0, weight=1)

        # inputs
        f_in = tk.Frame(tf, bg="#E4DFD7")
        f_in.grid(row=1, column=0, padx=5, pady=5)

        c_in = tk.Frame(f_in, bg="#E4DFD7")
        c_in.pack(expand=True, pady=10)

        self.entry_labels = []
        for i in range(6):
            l = tk.Label(c_in, font=("Calibri", 20, "bold"), bg="white", fg="#181716",
                         relief="sunken", borderwidth=2, width=3, height=1)
            l.grid(row=0, column=i, padx=5)
            self.entry_labels.append(l)

        # letters
        f_let = tk.Frame(tf, bg="#E4DFD7")
        f_let.grid(row=2, column=0, padx=5, pady=5)

        c_let = tk.Frame(f_let, bg="#E4DFD7")
        c_let.pack(expand=True, pady=10)

        self.letter_labels = []
        for i in range(6):
            l = tk.Label(c_let, font=("Calibri", 20, "bold"), bg="#181716", fg="white",
                         relief="raised", borderwidth=4, width=3, height=1)
            l.grid(row=0, column=i, padx=5)
            self.letter_labels.append(l)

        # score label
        f_stat = tk.Frame(tf, bg="#E4DFD7")
        f_stat.grid(row=3, column=0, sticky="nsew")

        self.level_status_label = tk.Label(f_stat, font=10, bg="#E4DFD7", fg="#181716")
        self.level_status_label.grid(row=0, column=0, sticky="nsew")

        self.score_label = tk.Label(f_stat, font=("Calibri", 14, "bold"), bg="#E4DFD7", fg="#232323")
        self.score_label.grid(row=0, column=1, sticky="nsew")

        f_stat.columnconfigure(0, weight=2)
        f_stat.columnconfigure(1, weight=1)

        self.resetInputSlotsText()

        # footer setting
        self.footer_pane = tk.Frame(main, bg="white")
        self.footer_pane.grid(row=3, column=0, sticky="nsew", padx=12, pady=(5, 0))

        self.clock_frame = tk.Frame(self.footer_pane, bg="white")
        self.clock_frame.grid(row=0, column=0, sticky="nsew")
        self.clock_frame.columnconfigure(0, weight=1)

        # weights for main
        main.columnconfigure(0, weight=1)
        main.rowconfigure(0, weight=0)
        main.rowconfigure(1, weight=1)
        main.rowconfigure(2, weight=1)
        main.rowconfigure(3, weight=0)

    def bindClockToUi(self, clock):
        for w in self.clock_frame.winfo_children():
            w.destroy()

        self.clock_label = tk.Label(self.clock_frame, textvariable=clock.displayTime,
                                    font=('Courier', 24, 'bold'), bg="white", fg="#232323", anchor="e")
        self.clock_label.grid(row=0, column=0, padx=20, sticky="e")

        self.shuffle_btn = tk.Button(self.clock_frame, text="🔀 Shuffle", font=("Calibri", 13, "bold"),
                                     bg="#181716", fg="white", relief="raised", borderwidth=3,
                                     activebackground="#4a4a4a", activeforeground="white", cursor="heart",
                                     command=self.shuffleTiles)
        self.shuffle_btn.grid(row=0, column=1, padx=10, pady=10, sticky="e", ipadx=10)

        self.reset_btn = tk.Button(self.clock_frame, text="🔄 Reset", font=("Calibri", 13, "bold"),
                                   bg="#181716", fg="white", relief="raised", borderwidth=3,
                                   activebackground="#4a4a4a", activeforeground="white", cursor="heart",
                                   command=self.restartRound)
        self.reset_btn.grid(row=0, column=2, padx=(5, 20), pady=10, sticky="e", ipadx=15)

    def initializeKeyBindings(self):
        self.bindings = {}
        self.bindings["<space>"] = self.shuffleTiles
        for char in ascii_lowercase:
            self.bindings[char] = self.handleTypedLetter
        self.bindings["<BackSpace>"] = self.handleBackspace
        self.bindings["<Return>"] = self.submitWord

    def toggleKeyBindings(self, action=0):
        if action == 1:
            for k, v in self.bindings.items():
                self.__root.bind_all(k, v)
        else:
            for k in self.bindings:
                self.__root.unbind_all(k)

    def add_game_object_to_ui(self, game):
        self.game = game
        self.bindClockToUi(game.clock)
        self.game.addUIUpdate("process_clock_reached_zero", self.handleGameEnd)

    def handleTypedLetter(self, event):
        char = event.char.upper()
        if char in ascii_uppercase:
            for lbl in self.letter_labels:
                if char == lbl['text']:
                    self.fillInputSlot(char)
                    lbl['text'] = ' '
                    lbl['relief'] = "sunken"
                    break

    def fillInputSlot(self, char):
        for entry in self.entry_labels:
            if entry['text'] == ' ' or entry['text'] == '_':
                entry['text'] = char
                break

    def handleBackspace(self, event):
        for entry in reversed(self.entry_labels):
            if entry['text'] != ' ' and entry['text'] != '_':
                self.returnLetterToTile(entry)
                break

    def returnLetterToTile(self, entry):
        for lbl in self.letter_labels:
            if lbl['text'] == ' ':
                lbl['text'] = entry['text']
                lbl['bg'] = "#181716"
                lbl['relief'] = "raised"
                entry['text'] = ' '
                break

    def submitWord(self, event):
        arr = []
        for l in self.entry_labels:
            if l['text'] != " " and l['text'] != "_":
                arr.append(l['text'])
        word = "".join(arr)

        if self.game.checkWord(word):
            self.revealSolutionWord(word)
            self.refreshTilesAndInputs()
            self.updateGameStatusLabels()

    def revealSolutionWord(self, word, color="#232323"):
        for sol in self.solution_labels:
            if "_" in sol['text'] and len(sol['text']) == len(word):
                sol['text'] = word
                sol['fg'] = color
                break

    def updateGameStatusLabels(self):
        score = self.game.getScore()
        self.score_label['text'] = f"Score: {score}"
        if self.game.levelPassed():
            self.level_status_label['text'] = "Keyword Found! Keep going <3"
        else:
            self.level_status_label['text'] = ""

    def resetInputSlotsText(self, text=" "):
        for x in self.entry_labels:
            x['text'] = text

    def clearInputsAndTiles(self):
        self.resetInputSlotsText()
        self.updateTileDisplay()

    def refreshTilesAndInputs(self):
        self.resetInputSlotsText()
        self.updateTileDisplay(self.game.getLetters())

    def updateTileDisplay(self, letters=[" "] * 6):
        self.letters = letters
        random.shuffle(self.letters)
        i = 0
        for x in self.letters:
            self.letter_labels[i].config(text=x)
            i += 1

    def shuffleTiles(self, *args):
        random.shuffle(self.letter_labels)
        i = 0
        for l in self.letter_labels:
            l.grid(row=0, column=i)
            i += 1

    def generateSolutionGrid(self):
        for w in self.top_pane.winfo_children():
            w.destroy()

        self.top_pane.columnconfigure(0, weight=1)
        self.top_pane.rowconfigure(0, weight=1)

        f = tk.Frame(self.top_pane, bg="#E4DFD7")
        f.grid(row=0, column=0)

        self.solution_labels = []
        wl = self.game.getWordList()

        # logic for grid size,, manual math
        count = len(wl)
        w = (count + 6) // 7
        if w < 4: w = 4
        h = (count + w - 1) // w

        idx = 0
        for word in sorted(wl, key=len):
            lbl = tk.Label(f, font=("Calibri", 12), text="_" * len(word), bg="#E4DFD7",
                           fg="#232323")
            r = idx % h
            c = idx // h
            lbl.grid(row=r, column=c, padx=10, pady=5)
            self.solution_labels.append(lbl)
            idx += 1

    def clearSolutionGrid(self):
        for w in self.top_pane.winfo_children():
            w.destroy()

    def showMissingWords(self):
        missing = self.game.getMissingWords()
        for word in sorted(missing, key=len):
            self.revealSolutionWord(word, color="#6D2932")

    def _createCenteredPopup(self, title, width, height):
        self.__root.update_idletasks()
        rw = self.__root.winfo_width()
        rh = self.__root.winfo_height()
        x = self.__root.winfo_x() + (rw // 2) - (width // 2)
        y = self.__root.winfo_y() + (rh // 2) - (height // 2)

        top = tk.Toplevel(self.__root)
        top.title(title)
        top.geometry(f"{width}x{height}+{x}+{y}")
        top.configure(bg="#E5DED2")
        return top

    def openRulesPopup(self):
        p = self._createCenteredPopup("Rules of the game", 300, 250)

        t = (
            "✨ Welcome to TextTwist! ✨\n\n"
            "Easy: 3mins to find 3–6 letters words\n"
            "Hard: 2mins to find 5–6 letters words\n\n"
            "🔀 Shuffle: Rearrange letters\n"
            "🔄 Reset: Start a new round\n"
            "🏆 Score: See highest score\n"
            "✖ Exit: Quit game\n\n"
        )

        tk.Message(p, text=t, font=("Calibri", 12), bg="#E5DED2", fg="#232323", justify="center",
                   aspect=300).pack(pady=20)
        tk.Button(p, text="OK", command=p.destroy, bg="#181716", fg="white").pack()

    def openHighScorePopup(self):
        p = self._createCenteredPopup("High Score", 300, 200)
        tk.Label(p, text="Highest Score", font=("Calibri", 18), bg="#E5DED2").pack(pady=20)
        tk.Label(p, text=f"{self.game.getHighScore()}", font=("Calibri", 36), fg="#CD5C5C", bg="#E5DED2").pack()

    def openGameOverPopup(self, final_score):
        p = self._createCenteredPopup("Game Over", 300, 300)

        def close():
            p.destroy()
            self.returnToMainMenu()

        tk.Label(p, text="TIME IS UP!", font=("Calibri", 20, "bold"),
                 bg="#E5DED2", fg="#232323").pack(pady=(70, 5))

        tk.Label(p, text=f"Your Score: {final_score}", font=("Calibri", 15),
                 bg="#E5DED2", fg="#181716").pack(pady=(0, 10))

        tk.Button(p, text="Play Again", font=("Calibri", 12, "bold"),
                  bg="#181716", fg="white", relief="raised", borderwidth=4,
                  cursor="heart", command=close).pack(pady=10, ipadx=30, ipady=3)

    def startGameSession(self):
        self.start_page_frame.grid_remove()
        self.game_page_frame.grid()
        self.toggleKeyBindings(1)

        self.game.startGame(self.current_difficulty)
        self.clearInputsAndTiles()
        self.updateTileDisplay(self.game.getLetters())
        self.clearSolutionGrid()
        self.generateSolutionGrid()
        self.updateGameStatusLabels()

    def restartRound(self):
        self.game.resetGame()
        self.game.startGame(self.current_difficulty)
        self.clearInputsAndTiles()
        self.updateTileDisplay(self.game.getLetters())
        self.clearSolutionGrid()
        self.generateSolutionGrid()
        self.updateGameStatusLabels()
        self.toggleKeyBindings(1)

    def returnToMainMenu(self):
        self.game.resetGame()
        self.game_page_frame.grid_remove()
        self.start_page_frame.grid()
        self.score_label['text'] = ""
        self.level_status_label['text'] = ""

    def handleGameEnd(self):
        self.__root.after(0, self._performGameOverSequence)

    def _performGameOverSequence(self):
        self.showMissingWords()
        self.refreshTilesAndInputs()
        self.toggleKeyBindings(0)

        final_score = self.game.getScore()
        self.game.updateHighScore()

        if final_score > self.high_score:
            self.high_score = final_score

        self.openGameOverPopup(final_score)

    def start_mainloop(self):
        self.__root.mainloop()