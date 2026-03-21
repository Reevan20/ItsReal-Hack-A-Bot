import pygame
import serial
import random


# =======================
# SERIAL CLASS (SEND ONLY)
# =======================
class SerialHandler:
    def __init__(self, port='/dev/ttyACM0', baud=115200):
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
        self.width, self.height = 600, 600
        self.rows, self.cols = 12, 12
        self.cell_size = self.width // self.cols

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Minefield + Serial")

        self.serial = serial_handler

        self.player_pos = [0, self.rows // 2]
        self.clock = pygame.time.Clock()
        self.running = True

        # Generate mines
        self.mines = set()
        self.num_mines = 25
        while len(self.mines) < self.num_mines:
            x = random.randint(0, self.cols - 1)
            y = random.randint(0, self.rows - 1)
            if (x, y) != tuple(self.player_pos):
                self.mines.add((x, y))

        self.game_over = False
        self.win = False

    def move_player(self, direction):
        if self.game_over or self.win:
            return

        if direction == "UP":
            self.player_pos[1] = max(0, self.player_pos[1] - 1)
        elif direction == "DOWN":
            self.player_pos[1] = min(self.rows - 1, self.player_pos[1] + 1)
        elif direction == "LEFT":
            self.player_pos[0] = max(0, self.player_pos[0] - 1)
        elif direction == "RIGHT":
            self.player_pos[0] = min(self.cols - 1, self.player_pos[0] + 1)

        # Send to Pico
        if self.serial:
            self.serial.send(direction)

        # Check mine collision
        if tuple(self.player_pos) in self.mines:
            self.game_over = True

        # Check win condition
        if self.player_pos[0] == self.cols - 1:
            self.win = True

    def draw_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                rect = pygame.Rect(col * self.cell_size, row * self.cell_size,
                                   self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, (80, 80, 80), rect, 1)

    def draw_mines(self):
        for (mx, my) in self.mines:
            rect = pygame.Rect(mx * self.cell_size, my * self.cell_size,
                               self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, (200, 0, 0), rect)

    def draw_player(self):
        rect = pygame.Rect(self.player_pos[0] * self.cell_size,
                           self.player_pos[1] * self.cell_size,
                           self.cell_size, self.cell_size)
        pygame.draw.rect(self.screen, (0, 200, 255), rect)

    def draw_goal(self):
        for row in range(self.rows):
            rect = pygame.Rect((self.cols - 1) * self.cell_size,
                               row * self.cell_size,
                               self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, (0, 200, 0), rect, 3)

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

            # Draw everything
            self.screen.fill((30, 30, 30))
            self.draw_grid()
            self.draw_mines()  # Always visible
            self.draw_goal()
            self.draw_player()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


# =======================
# MAIN
# =======================
if __name__ == "__main__":
    # serial_handler = SerialHandler('/dev/ttyACM0')

    game = Game()
    game.run()

    # serial_handler.close()
