import pygame
from sys import exit
from degrees_to_velocity import degrees_to_velocity


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
            self.screen_rect,
            WHITE,
            self.screen_rect.width * 0.1,
            self.screen_rect.centery,
            )
        self.player_2 = Racket(
            self.screen_rect,
            WHITE,
            self.screen_rect.width * 0.9,
            self.screen_rect.centery,
            )

        self.ball = Ball(
            screen_rect=self.screen_rect,
            color=WHITE,
            center_x=self.screen_rect.centerx,
            center_y=self.screen_rect.centery)

        self.counter_1 = Counter(30, WHITE, self.screen_info)
        self.counter_2 = Counter(30, WHITE, self.screen_info)

        self.all_sprites = pygame.sprite.Group() # создаем объект класс Group
        self.all_sprites.add(self.player_1)
        self.all_sprites.add(self.player_2)
        self.all_sprites.add(self.ball)
        self.clock.tick(60)

    def move_players(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
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
            self.ball.speed_y *= -1
        if self.ball.rect.top <= self.screen_rect.top:
            self.ball.speed_y *= -1
        if self.ball.rect.right >= self.screen_rect.right:
            self.ball.rect.center = self.screen_rect.center
            self.counter_1.counter += 1
        if self.ball.rect.left <= self.screen_rect.left:
            self.ball.rect.center = self.screen_rect.center
            self.counter_2.counter += 1

        if self.ball.rect.colliderect(self.player_1.rect):
            self.ball.rect.centerx += self.ball.speed_x * -1
            self.ball.speed_x *= -1
        if self.ball.rect.colliderect(self.player_2.rect):
            self.ball.rect.centerx += self.ball.speed_x * -1
            self.ball.speed_x *= -1

    def main_loop(self):
        game = True
        while game:
            key = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
            if key[pygame.K_ESCAPE]:
                game = False

            self.counter_1.draw(self.screen)
            self.counter_2.draw(self.screen)
            self.move_players()
            self.collisions()
            self.ball.move()
            self.screen.fill((0, 0, 0))
            self.all_sprites.draw(self.screen)
            pygame.display.flip()


class Racket(pygame.sprite.Sprite):
    def __init__(
            self,
            screen_rect,
            color: tuple,
            center_x: int,
            center_y: int
            ) -> None:
        super().__init__()
        self.speed = 3
        self.width = screen_rect.width * 0.005
        self.height = screen_rect.height * 0.08
        self.isautomatic = False
        self.image = pygame.Surface(
            (self.width, self.height)
        )
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.centerx = center_x
        self.rect.centery = center_y

    def move(self, screen_rect, ball):
        if not self.isautomatic:
            if self.rect.bottom >= screen_rect.bottom:
                self.rect.bottom = screen_rect.bottom
            if self.rect.top <= screen_rect.top:
                self.rect.top = screen_rect.top


class Ball(pygame.sprite.Sprite):
    def __init__(
            self,
            screen_rect,
            color,
            center_x,
            center_y
            ) -> None:
        super().__init__()
        self.direction = degrees_to_velocity(320, 2.5)
        self.speed_x, self.speed_y = self.direction
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
        self.rect.centerx, self.rect.centery = self.rect.centerx + self.speed_x, self.rect.centery + self.speed_y


class Counter():
    def __init__(self, size, screen_info, counter) -> None:
        self.size = size
        self.score = pygame.font.Font(size=self.size)
        self.score_x = screen_info.current_w * 0.5
        self.score_y = screen_info.current_h * 0.5
        self.counter = 0
        self.img = self.score.render(str(counter), True, (255, 255, 255))

    def draw(self, screen):
        screen.blit(self.img, (self.score_x, self.score_y))


game = Game()
game.main_loop()
pygame.quit
exit()