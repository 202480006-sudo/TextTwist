import threading
from texttwistgame import TextTwistGame
from ui import TextTwistUI

"""
This is the main
creates the objects for UI and the game logic
Starts the game loop and handles user interactions.
"""


def handle_thread_exceptions(*args):
    pass

if __name__ == "__main__":
    threading.excepthook = handle_thread_exceptions
    ui = TextTwistUI()
    game = TextTwistGame()
    ui.add_game_object_to_ui(game)
    ui.start_mainloop()