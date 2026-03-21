import pygame
import serial

DEVICE_PORT = '/dev/ttyACM0'

# =======================
# SERIAL CLASS (SEND ONLY)
# =======================
class SerialHandler:
    def __init__(self, port=DEVIC_PORT, baud=115200):
        self.ser = serial.Serial(port, baud, timeout=1)

    def send(self, msg: str):
        self.ser.write((msg + "\n").encode())

    def close(self):
        self.ser.close()


# =======================
# GAME CLASS
# =======================
class Game:
    def __init__(self, serial_handler=None):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("Minefield + Serial")

        self.serial = serial_handler

        self.player_pos = [5, 5]
        self.clock = pygame.time.Clock()
        self.running = True

    def move_player(self, direction):
        if direction == "UP":
            self.player_pos[1] -= 1
        elif direction == "DOWN":
            self.player_pos[1] += 1
        elif direction == "LEFT":
            self.player_pos[0] -= 1
        elif direction == "RIGHT":
            self.player_pos[0] += 1

        # Send to Pico at the SAME time
        if self.serial:
            self.serial.send(direction)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.move_player("UP")
                    elif event.key == pygame.K_DOWN:
                        self.move_player("DOWN")
                    elif event.key == pygame.K_LEFT:
                        self.move_player("LEFT")
                    elif event.key == pygame.K_RIGHT:
                        self.move_player("RIGHT")

            # Draw
            self.screen.fill((30, 30, 30))
            pygame.draw.rect(
                self.screen,
                (0, 200, 255),
                (self.player_pos[0]*40, self.player_pos[1]*40, 40, 40)
            )

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


# =======================
# MAIN
# =======================
if __name__ == "__main__":
    serial_handler = SerialHandler('/dev/ttyACM0')

    game = Game(serial_handler)
    game.run()

    serial_handler.close()
