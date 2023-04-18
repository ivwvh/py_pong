import pygame
import sys
import degrees_to_velocity

pygame.init()  # инициализация модулей пайгейма

# константы
WHITE = (255, 255, 255)  # белый цвет
BLACK = (0, 0, 0)  # черный цвет

# экран
screen_width = 800  # ширина экрана в пикселях
screen_height = 600  # высота экрана в пикселях
screen = pygame.display.set_mode((screen_width, screen_height))  # экран

# игрок
player_1_width = 20  # ширина игрока
player_1_height = 70  # высота игрока
player_1_x = 100  # игрок в центре по ширине
player_1_y = screen_height // 2 - player_1_height // 2  # игрок в центре по высоте
player_1 = pygame.Rect((player_1_x, player_1_y, player_1_width, player_1_height))  # создаем игрока

player_2_width = 20  # ширина игрока
player_2_height = 70  # высота игрока
player_2_x = screen_width - 100 - player_2_height # игрок в центре по ширине
player_2_y = screen_height // 2 - player_1_height // 2  # игрок в центре по высоте
player_2 = pygame.Rect((player_2_x, player_2_y, player_2_width, player_2_height))  # создаем игрока

ball_width = 15  # ширина игрока
ball_height = 15  # высота игрока
ball_x = screen_width // 2 - ball_width // 2  # игрок в центре по ширине
ball_y = screen_height // 2 - ball_height // 2  # игрок в центре по высоте
ball_speed_x = 1
ball_speed_y = 1
ball = pygame.Rect((ball_x, ball_y, ball_width, ball_height))

game = True  
while game:
    """ 
        Главный цикл игры
        Цикл должен обязательно закончится обновлением дисплея,
        если выйти по break, то игра зависнет!
        Контролируем, идет ли игра, переменной game
    """

    # события
    for event in pygame.event.get():  # проходим по всем событиям, которые происходят сейчас
        if event.type == pygame.QUIT:  # обработка события выхода
            game = False
        if event.type == pygame.KEYDOWN:  # нажатая клавиша (не зажатая!)
            if event.key == pygame.K_ESCAPE:  # клавиша Esc
                game = False

    keys = pygame.key.get_pressed() # собираем коды нажатых клавиш в список
    if keys[pygame.K_w]:  # клавиша стрелка вверх
        if player_1.y > 0:
            player_1.y -= 1  # двигаем игрока вверх (в PG Y растет вниз)
    if keys[pygame.K_s]:  # клавиша стрелка вниз
        if player_1.y < screen_height - player_1_height:
            player_1.y += 1  # двигаем игрока вниз
    if keys[pygame.K_UP]:  # клавиша стрелка вверх
        if player_2.y > 0:
            player_2.y -= 1  # двигаем игрока вверх (в PG Y растет вниз)
    if keys[pygame.K_DOWN]:  # клавиша стрелка вниз
        if player_2.y < screen_height - player_2_height:
            player_2.y += 1  # двигаем игрока вниз

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.x <= 0:
        ball_speed_x *= -1
    if ball.x >= screen_width - ball_width:
        ball_speed_x *= -1
    if ball.y < 0:
        ball_speed_y *= -1
    if ball.y > screen_height - ball_height:
        ball_speed_y *= -1

    # отрисовка
    screen.fill(BLACK)  # заливаем экран чёрным
    pygame.draw.rect(screen, WHITE, player_1)  # рисуем игрока
    pygame.draw.rect(screen, WHITE, player_2)
    pygame.draw.rect(screen, WHITE, ball)
    pygame.display.flip()  # обновляем экран

# после завершения главного цикла
pygame.quit()  # выгрузили модули pygame из пямяти
sys.exit()  # закрыли программу
