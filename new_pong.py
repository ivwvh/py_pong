import pygame
from sys import exit
from degrees_to_velocity import degrees_to_velocity
from random import choice, randint
WHITE = (255, 255, 255)
FPS = 250


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
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
            move_keys=(pygame.K_w, pygame.K_s),
            isautomatic=1)
        self.player_2 = Racket(
            screen_rect=self.screen_rect,
            center=(self.screen_rect.width * 0.9, self.screen_rect.centery),
            isautomatic=1)
        self.ball = Ball(
            screen_rect=self.screen_rect,
            color=WHITE,
            center_x=self.screen_rect.centerx,
            center_y=self.screen_rect.centery)
        self.scoreboard_1 = Scoreboard(x=self.screen_width * 0.25,
                                       y=self.screen_height * 0.05)
        self.scoreboard_2 = Scoreboard(x=self.screen_width * 0.75,
                                       y=self.screen_height * 0.05)
        self.jugde = Jugde(self.screen, self.ball)
        self.paddles = pygame.sprite.Group()
        self.balls = pygame.sprite.Group()
        self.paddles.add(self.player_1)
        self.paddles.add(self.player_2)
        self.balls.add(self.ball)
        self.clock.tick(FPS)

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
            self.ball.direction[1] *= -1
        if self.ball.rect.top <= self.screen_rect.top:
            self.ball.direction[1] *= -1
        if self.ball.rect.right >= self.screen_rect.right:
            self.jugde.throw_in()
            self.jugde.update_scoreboard(self.scoreboard_1)
        if self.ball.rect.left <= self.screen_rect.left:
            self.jugde.throw_in()
            self.jugde.update_scoreboard(self.scoreboard_2)

        if self.ball.rect.colliderect(self.player_1.rect):
            self.ball.rect.centerx += self.ball.direction[0] * -1
            self.ball.direction[0] *= -1
        if self.ball.rect.colliderect(self.player_2.rect):
            self.ball.rect.centerx += self.ball.direction[0] * -1
            self.ball.direction[0] *= -1

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
            self.ball.move()
            self.paddles.update()
            self.screen.fill((0, 0, 0))
            self.paddles.draw(self.screen)
            self.balls.draw(self.screen)
            pygame.draw.line(self.screen,
                             WHITE,
                             self.screen_rect.midtop,
                             self.screen_rect.midbottom
                             )
            self.scoreboard_1.draw(self.screen)
            self.scoreboard_2.draw(self.screen)
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

    def update(self):
        if not self.isautomatic:
            keys = pygame.key.get_pressed()
            if keys[self.move_keys[0]]:
                self.rect.y -= self.speed
            if keys[self.move_keys[1]]:
                self.rect.y += self.speed
        else:
            pass

    def move(self, ball_y: int):
        if not self.isautomatic:
            keys = pygame.key.get_pressed()
            if keys[self.move_keys[0]]:
                self.rect.centery -= 1
            elif keys[self.move_keys[0]]:
                self.rect.centery += 1
        else:
            if self.rect.centery > ball_y:
                self.rect.centery -= self.speed
            elif self.rect.centery < ball_y:
                self.rect.centery += self.speed


class Ball(pygame.sprite.Sprite):
    def __init__(
            self,
            screen_rect,
            color,
            center_x,
            center_y
            ) -> None:
        super().__init__()
        degrees = 320
        self.speed = 2.5
        self.direction = list(degrees_to_velocity(degrees, self.speed))
        self.width = 10
        self.height = 10
        self.image = pygame.Surface(
            (self.width, self.height)
        )
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.centerx = center_x
        self.rect.centery = center_y

    def move(self):
        self.rect.centerx, self.rect.centery = self.rect.centerx + self.direction[0], self.rect.centery + self.direction[1]


class Scoreboard:
    def __init__(self, x=0, y=0, counter=0, color=WHITE) -> None:
        self.x = x
        self.y = y
        self.counter = counter
        self.color = color

    def draw(self, screen: pygame.Surface):
        font = pygame.font.Font(size=50)
        img = font.render(str(self.counter), False, self.color)
        screen.blit(img, (self.x, self.y))


class Jugde:
    def __init__(self, screen: pygame.Surface, ball: Ball) -> None:
        self.screen = screen
        self.ball = ball

    def throw_in(self):
        self.ball.rect.center = self.screen.get_rect().center
        self.ball.direction = list(degrees_to_velocity(choice((randint(45, 135), randint(225, 315))), self.ball.speed))

    def update_scoreboard(self, scoreboard: Scoreboard):
        scoreboard.counter += 1
        scoreboard.draw(self.screen)


game = Game()
game.main_loop()
pygame.quit
exit()
