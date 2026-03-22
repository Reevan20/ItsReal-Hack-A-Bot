import game
import serial_handler

# MAIN
if __name__ == "__main__":
    serial_handler = serial_handler.SerialHandler('/dev/ttyACM0')

    game = game.Game()
    game.run()

    serial_handler.close()
