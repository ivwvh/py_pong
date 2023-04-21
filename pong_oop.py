import pygame
import sys


class Racket:  # класс для ракеток
    def __init__(self, x: int, player: int) -> None:
        self.width = 20
        self.height = 70
        self.x = x
        self.y = pygame.display.Info().current_h // 2 - self.height // 2
        self.color = (255, 255, 255)
        self.speed = 1
        self.player = player
        self.rect = None

    def draw(self, screen) -> None:
        self.rect = pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self) -> None:
        key = pygame.key.get_pressed()
        if self.player == 1:
            if key[pygame.K_UP]:
                if self.y > 0:
                    self.y -= self.speed
                    print(f"{self.y}")
            if key[pygame.K_DOWN]:
                if self.y < pygame.display.Info().current_h - self.height:
                    self.y += self.speed
                    print(f"{self.y}")

        elif self.player == 2:
            if key[pygame.K_w]:
                if self.y > 0:
                    self.y -= self.speed
                    print(f"{self.y}")
            if key[pygame.K_s]:
                if self.y < pygame.display.Info().current_h - self.height:
                    self.y += self.speed
                    print(f"{self.y}")


class Ball:
    def __init__(self) -> None:
        self.width = 15
        self.height = 15
        self.x = pygame.display.Info().current_w // 2 - self.width // 2
        self.y = pygame.display.Info().current_h // 2 - self.height // 2
        self.speed_x = 1
        self.speed_y = 1
        self.color = (255, 255, 255)
        self.rect = None

    def draw(self, screen) -> None:
        self.rect = pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        if self.x <= 0:
            self.speed_x *= -1
        if self.x >= pygame.display.Info().current_w - self.width:
            ball.speed_x *= -1

        if self.y < 0:
            self.speed_y *= -1
        if self.y > pygame.display.Info().current_h - self.height:
            self.speed_y *= -1


def collisions(ball, rackets):
    for racket in rackets:
        if ball.rect.colliderect(racket.rect):
            ball.speed_x *= -1
            ball.speed_y *= -1


screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.init()

racket = Racket(x=100, player=1)
racket_2 = Racket(x=screen_width - 100 - racket.height, player=2)
ball = Ball()
rackets = [racket, racket_2]
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((0, 0, 0))
    ball.draw(screen)
    racket.draw(screen)
    racket_2.draw(screen)
    racket.move()
    racket_2.move()
    ball.move()
    collisions(ball, rackets)
    pygame.display.flip()