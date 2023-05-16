import pygame
from sys import exit
from degrees_to_velocity import degrees_to_velocity
from math import sin, cos, radians
from random import randint, choice
WHITE = (255, 255, 255)
FPS = 60


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        WHITE = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.screen_info = pygame.display.Info()
        self.screen_width = self.screen_info.current_w
        self.screen_height = self.screen_info.current_h
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height),
            pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
        self.player_1 = Racket(
            screen_rect=self.screen_rect,
            center=(self.screen_rect.width * 0.1, self.screen_rect.centery),
            move_keys=(pygame.K_w, pygame.K_s))
        self.player_2 = Racket(
            screen_rect=self.screen_rect,
            center=(self.screen_rect.width * 0.9, self.screen_rect.centery),
            isautomatic=True)
        self.ball = Ball(
            screen_rect=self.screen_rect)

        self.paddles = pygame.sprite.Group()  # создаем объект класс Group
        self.ball_group = pygame.sprite.Group()
        self.paddles.add(self.player_1)
        self.paddles.add(self.player_2)
        self.ball_group.add(self.ball)
        self.clock.tick(FPS)

    def move_players(self):
        keys = pygame.key.get_pressed()
        if keys[self.player_1.keys[0]]:
            self.player_1.rect.centery -= self.player_1.speed
        if keys[pygame.K_s]:
            self.player_1.rect.centery += self.player_1.speed
        if keys[pygame.K_UP]:
            self.player_2.rect.centery -= self.player_2.speed
        if keys[pygame.K_DOWN]:
            self.player_2.rect.centery += self.player_2.speed

    def collisions(self):
        if self.player_1.rect.top <= self.screen_rect.top:
            self.player_1.rect.top = self.screen_rect.top
        if self.player_2.rect.top <= self.screen_rect.top:
            self.player_2.rect.top = self.screen_rect.top
        if self.player_1.rect.bottom >= self.screen_rect.bottom:
            self.player_1.rect.bottom = self.screen_rect.bottom
        if self.player_2.rect.bottom >= self.screen_rect.bottom:
            self.player_2.rect.bottom = self.screen_rect.bottom

        if self.ball.rect.bottom >= self.screen_rect.bottom:
            self.ball.direction *= -1
        if self.ball.rect.top <= self.screen_rect.top:
            self.ball.direction *= -1
        if self.ball.rect.right >= self.screen_rect.right:
            self.ball.throw_in()
        if self.ball.rect.left <= self.screen_rect.left:
            self.ball.throw_in()

        if self.ball.rect.colliderect(self.player_1.rect):
            self.ball.rect.centerx += self.ball.vel_x * -1
            self.ball.direction *= -1
        if self.ball.rect.colliderect(self.player_2.rect):
            self.ball.rect.centerx += self.ball.vel_x * -1
            self.ball.direction *= -1

    def main_loop(self):
        game = True
        while game:
            key = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
            if key[pygame.K_ESCAPE]:
                game = False

            self.player_1.move(self.ball.rect.y)
            self.player_2.move(self.ball.rect.y)
            self.collisions()
            self.paddles.update(self.ball.rect.y)
            self.ball_group.update()
            self.screen.fill((0, 0, 0))
            self.paddles.draw(self.screen)
            self.ball_group.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)


class Racket(pygame.sprite.Sprite):
    """
    ракетка
    """
    def __init__(
            self,
            screen_rect,
            color=WHITE,
            center=(0, 0),
            size=None,
            move_keys=(pygame.K_UP, pygame.K_DOWN),
            speed=30,
            isautomatic=False
            ) -> None:
        super().__init__()
        self.speed = 3
        if not size:
            size = (screen_rect.width * 0.005, screen_rect.height * 0.08)
        self.isautomatic = isautomatic
        self.image = pygame.Surface(
            size
        )
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.move_keys = move_keys

    def update(self, ball_y):
        if not self.isautomatic:
            keys = pygame.key.get_pressed()
            if keys[self.move_keys[0]]:
                self.rect.y -= self.speed
            if keys[self.move_keys[1]]:
                self.rect.y += self.speed
        else:
            if self.rect.centery > ball_y:
                self.rect.centery -= self.speed
            elif self.rect.centery < ball_y:
                self.rect.centery += self.speed


class Ball(pygame.sprite.Sprite):
    def __init__(
            self,
            screen_rect:pygame.Rect,
            color=WHITE,
            center = None,
            size=None,
            speed=10,
            direction=250,
            vel_x=0,
            vel_y=0,
            ) -> None:
        super().__init__()
        self.direction = direction
        self.speed = speed
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.screen_rect = screen_rect
        if not size:
            size = (screen_rect.width * 0.01, screen_rect.width * 0.01)
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        if not center:
            self.rect.center = screen_rect.center
        
    def update(self):
        self.vel_x = sin(radians(self.direction)) * self.speed
        self.vel_y = cos(radians(self.direction)) * self.speed * -1
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.bounce()

    def throw_in(self):
        self.rect.center = self.screen_rect.center
        self.direction = choice((randint(45, 135), randint(225, 315)))

    def bounce(self):
        if self.rect.top < self.screen_rect.top:
            self.direction *= -1
        elif self.rect.top > self.screen_rect.top:
            self.direction *= -1
            self.direction += 180
"""class Counter():
    def __init__(self, size, screen_info, counter) -> None:
        self.size = size
        self.score = pygame.font.Font(size=self.size)
        self.score_x = screen_info.current_w * 0.5
        self.score_y = screen_info.current_h * 0.5
        self.counter = 0
        self.img = self.score.render(str(counter), True, (255, 255, 255))

    def draw(self, screen):
        screen.blit(self.img, (self.score_x, self.score_y))"""


game = Game()
game.main_loop()
pygame.quit
exit()
