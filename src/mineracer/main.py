import game

# MAIN
if __name__ == "__main__":
    # serial_handler = SerialHandler('/dev/ttyACM0')

    game = game.Game()
    game.run()

    # serial_handler.close()
