
from rf_handler import RFHandler
import game

if __name__ == "__main__":
    rf = RFHandler()

    game = game.Game(serial_handler=rf)
    game.run()
