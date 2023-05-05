import pygame
from sys import exit


class Game:
    def __init__(self) -> None:
        pygame.init()
        WHITE = (255, 255, 255)
        self.screen_info = pygame.display.Info()
        self.screen_width = pygame.display.Info().current_w
        self.screen_height = pygame.display.Info().current_h
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height),
            pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
        self.player_1 = Racket(
            self.screen_rect,
            self.screen_rect.center,
            WHITE,
            self.screen_rect.width * 0.1,
            self.screen_rect.centery,
            )
        self.player_2 = Racket(
            self.screen_rect,
            self.screen_rect.center,
            WHITE,
            self.screen_rect.width * 0.9,
            self.screen_rect.centery,
            )
        self.all_sprites = pygame.sprite.Group() # создаем объект класс Group
        self.all_sprites.add(self.player_1)
        self.all_sprites.add(self.player_2)

    def main_loop(self):
        game = True
        while game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
            
            key = pygame.key.get_pressed()
            if key[pygame.K_ESCAPE]:
                game = False

            self.all_sprites.draw(self.screen)
            pygame.display.flip()


class Racket(pygame.sprite.Sprite):
    def __init__(
            self,
            screen_rect, 
            center: tuple,
            color: tuple,
            center_x: int,
            center_y: int
            ) -> None:
        super().__init__()
        self.image = pygame.Surface(
            (screen_rect.width * 0.01, screen_rect.height * 0.05)
        )
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.centerx = center_x
        self.rect.centery = center_y

game = Game()
game.main_loop()
pygame.quit
exit()