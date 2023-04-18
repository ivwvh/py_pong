"""
Ракетка:
движется только вверх и вниз

Мячик:
двигается, откскакивает от верхней и нижней границ
правая граница - гол противнику
левая граница - гол игроку

Счетчик:
показывает счёт

"""
import pygame
import sys
from random import randint




class Racket():
    def __init__(self, screen, x=100, y=177) -> None:
        self.x = x
        self.y = y
        self.width = 20
        self.height = 100
        self.color = (255, 255, 255)
        self.speed = 0.2

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            self.y -= self.speed
            print(f"{self.y}")
        if key[pygame.K_DOWN]:
            self.y += self.speed
            print(f"{self.y}")

    def auto_move(self):
        for i in range(10):
            self.y += 0.1
        for i in range(10):
            self.y -= 0.1

s_width = 800
s_height = 600
screen = pygame.display.set_mode((s_width, s_height))

pygame.init()

racket = Racket()
racket_2 = Racket(x=650, y= 177)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((0, 0, 0))
    racket.move()
    racket_2.auto_move()
    racket.draw(screen)
    racket_2.draw(screen)
    pygame.display.flip()