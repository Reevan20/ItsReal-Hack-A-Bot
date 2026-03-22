import pygame
import random
import math
import serial_handler

# =======================
# GAME CLASS
# =======================
class Game:
    def __init__(self, serial_handler=None):
        pygame.init()

        self.width, self.height = 600, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Minefield - Directional Movement")

        self.serial_handler = serial_handler

        self.clock = pygame.time.Clock()
        self.running = True

        # Player state
        self.x = 50
        self.y = self.height // 2
        self.angle = 0  # degrees
        self.speed = 2
        self.turn_speed = 3
        self.closest_distance = 999

        # Mines
        self.mines = []
        for _ in range(30):
            mx = random.randint(50, self.width - 50)
            my = random.randint(50, self.height - 50)
            self.mines.append((mx, my))

        self.game_over = False
        self.win = False

    def move_forward(self):
        rad = math.radians(self.angle)
        self.x += math.cos(rad) * self.speed
        self.y += math.sin(rad) * self.speed
        self.serial_handler.send('f')  # f for forward

    def check_collision(self):
        for mx, my in self.mines:
            mine_distance = math.hypot(self.x - mx, self.y - my)
            if mine_distance < self.closest_distance:
                self.closest_distance = mine_distance
            if mine_distance < 15:
                self.game_over = True
                self.serial_handler.send('l')  # lose

        if self.x >= self.width - 20:
            self.win = True
            self.serial_handler.send('w')  # win

        self.serial_handler.send(f'd{self.closest_distance}')  # distance

    def draw_player(self):
        # Draw triangle pointing in direction
        rad = math.radians(self.angle)

        tip = (self.x + math.cos(rad) * 15,
               self.y + math.sin(rad) * 15)

        left = (self.x + math.cos(rad + 2.5) * 10,
                self.y + math.sin(rad + 2.5) * 10)

        right = (self.x + math.cos(rad - 2.5) * 10,
                 self.y + math.sin(rad - 2.5) * 10)

        pygame.draw.polygon(self.screen, (0, 200, 255), [tip, left, right])

    def draw_mines(self):
        for mx, my in self.mines:
            pygame.draw.circle(self.screen, (200, 0, 0), (int(mx), int(my)), 8)

    def draw_goal(self):
        pygame.draw.rect(self.screen, (0, 200, 0), (self.width - 10, 0, 10, self.height))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()

            if not self.game_over and not self.win:
                if keys[pygame.K_LEFT]:
                    self.angle -= self.turn_speed
                    self.serial_handler.send('tl')  # turn left
                if keys[pygame.K_RIGHT]:
                    self.angle += self.turn_speed
                    self.serial_handler.send('tr')  # turn rigth
                if keys[pygame.K_UP]:
                    self.move_forward()

                self.check_collision()

            # Draw
            self.screen.fill((30, 30, 30))
            self.draw_mines()
            self.draw_goal()
            self.draw_player()

            # End text
            if self.game_over:
                self.draw_text("GAME OVER", (200, 0, 0))
            elif self.win:
                self.draw_text("YOU WIN", (0, 200, 0))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def draw_text(self, text, color):
        font = pygame.font.SysFont(None, 48)
        surf = font.render(text, True, color)
        rect = surf.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(surf, rect)
