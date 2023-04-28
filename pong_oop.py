import pygame
import sys
from degrees_to_velocity import degrees_to_velocity


class Racket:  # класс для ракеток
    def __init__(self, x: int, player: int) -> None:
        self.width = 10
        self.height = 70
        self.x = x
        self.y = pygame.display.Info().current_h // 2 - self.height // 2
        self.color = (255, 255, 255)
        self.speed = 10
        self.player = player
        self.counter = 0
        self.rect = None

    def draw(self, screen: pygame.display) -> None:
        self.rect = pygame.draw.rect(screen,
                                     self.color,
                                     (self.x, self.y, self.width, self.height))

    def move(self) -> None:
        key = pygame.key.get_pressed()
        if self.player == 1:
            if key[pygame.K_w]:
                if self.y > 0:
                    print(f"Координаты игрока {self.player}: {self.y}")
                    self.y -= self.speed
            if key[pygame.K_s]:
                if self.y < pygame.display.Info().current_h - self.height:
                    print(f"Координаты игрока {self.player}: {self.y}")
                    self.y += self.speed
        elif self.player == 2:
            if key[pygame.K_UP]:
                if self.y > 0:
                    self.y -= self.speed
                    print(f"Координаты игрока {self.player}: {self.y}")
            if key[pygame.K_DOWN]:
                if self.y < pygame.display.Info().current_h - self.height:
                    print(f"Координаты игрока {self.player}: {self.y}")
                    self.y += self.speed


class Ball:
    def __init__(self) -> None:
        self.width = 10
        self.height = 10
        self.x = pygame.display.Info().current_w // 2 - self.width // 2
        self.y = pygame.display.Info().current_h // 2 - self.height // 2
        self.direction = degrees_to_velocity(130, 5)
        self.speed_x = self.direction[0]
        self.speed_y = self.direction[1]
        self.color = (255, 255, 255)
        self.rect = None
        self.iscollided = False

    def draw(self, screen) -> None:
        self.rect = pygame.draw.rect(screen,
                                     self.color,
                                     (self.x, self.y,
                                      self.width, self.height))

    def move(self, players: list):
        self.x += self.speed_x
        self.y += self.speed_y

        if self.x <= 0:
            self.x = pygame.display.Info().current_w // 2 - self.width // 2
            self.y = pygame.display.Info().current_h // 2 - self.height // 2
            players[1].counter += 1

        if self.x >= pygame.display.Info().current_w - self.width:
            self.x = pygame.display.Info().current_w // 2 - self.width // 2
            self.y = pygame.display.Info().current_h // 2 - self.height // 2
            players[0].counter += 1

        if self.y < 0:
            self.speed_y *= -1
        if self.y > pygame.display.Info().current_h - self.height:
            self.speed_y *= -1

    def score(players, i):
        players[i].counter += 1


def collisions(ball:Ball, rackets:list):
    if ball.rect.colliderect(rackets[0].rect) and ball.iscollided is False or ball.rect.colliderect(rackets[1].rect) and ball.iscollided is False:
        ball.speed_x *= -1
        ball.iscollided = True
    elif ball.rect.left > rackets[0].rect.right and ball.rect.right < rackets[1].rect.left:  # нейтральная точка обоих ракеток
        ball.iscollided = False


class Counter:
    def __init__(self) -> None:
        self.score_right = pygame.font.Font(None, size=30)
        self.score_left = pygame.font.Font(None, size=30)
        self.score_right_x = pygame.display.Info().current_w * 0.25
        self.score_y = pygame.display.Info().current_h * 0.07
        self.score_left_x = pygame.display.Info().current_w * 0.75
        self.right_img = None
        self.left_img = None

    def draw(self, players):
        self.right_img = self.score_right.render(str(players[0].counter), True, (255, 255, 255))
        self.left_img = self.score_right.render(str(players[1].counter), True, (255,255, 255))
        screen.blit(self.left_img, (self.score_left_x, self.score_y))
        screen.blit(self.right_img, (self.score_right_x, self.score_y))


screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.init()

clock = pygame.time.Clock()
racket = Racket(x=100, player=1)
racket_2 = Racket(x=screen_width - 100 - racket.height, player=2)
ball = Ball()
counter = Counter()
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
    ball.move(rackets)
    counter.draw(rackets)
    collisions(ball, rackets)
    pygame.display.flip()
    clock.tick(60)