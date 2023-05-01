import pygame
import sys
import os
import pathlib
from degrees_to_velocity import degrees_to_velocity

# Зачем?
os.chdir(pathlib.Path(__file__).parent.resolve())  # меняем CWD на папку из которой запускается файл


class Racket:
    def __init__(self, x: int, player: int) -> None:  # Как создать здоровую синюю ракетку, которой играет компьютер, посередине экрана?
        """
        создает ракетку с определенными свойствами:

        width(int) - ширина
        height(int) - высота
        x(int) - местоположение по x
        y(int) - местоположение по y
        color(tuple) - цвет в формате RGB
        speed(int) - скорость ракетки
        player(int) - номер игрока, отвечает за управление
        score(int) - счетчик игрока
        rect(pygame.Rect) - объект класса Rect представляющий ракетку
        
        Позиционирование по rect.x и rect.y не всегда удобно, посмотрите на остальные атрибуты прямоугольника https://vk.com/ddtinfo?w=wall-170034757_207
        Игрока лучше сделать из Surface, снять с него прямогуольник методом get_rect и нарисовать методом blit
        """
        self.width = 10
        self.height = 70
        self.x = x
        self.y = pygame.display.Info().current_h // 2 - self.height // 2  # Вы часто создаёте этот экземпляр дальше в коде. Почему бы не сделать это один раз, а потом пользоваться результатом?
        self.color = (255, 255, 255)
        self.speed = 10
        self.player = player
        self.score = 0
        self.rect = None

    def draw(self, screen: pygame.Surface) -> None:
        """
        рисует ракетку и присваиваем получившийся объект класса Rect к переменной
        
        """
        self.rect = pygame.draw.rect(screen,
                                     self.color,
                                     (self.x, self.y, self.width, self.height)
                                     )

    def move(self) -> None:
        """
        изменяет положение ракетки меняя её y координату
        
        DRY!
        Лучше вместо self.player сделать self.key_up и self.key_down
        А self.is_automatic может контролировать управление игроком/компом
        """
        key = pygame.key.get_pressed()
        if self.player == 1:
            if key[pygame.K_w]:
                if self.y > 0:
                    self.y -= self.speed
            if key[pygame.K_s]:
                if self.y < pygame.display.Info().current_h - self.height:
                    self.y += self.speed
        elif self.player == 2:
            if key[pygame.K_UP]:
                if self.y > 0:
                    self.y -= self.speed
            if key[pygame.K_DOWN]:
                if self.y < pygame.display.Info().current_h - self.height:
                    self.y += self.speed


class Ball:
    def __init__(self) -> None:  # Как сделать большой жёлтый мячик в правом углу?
        """
        создает мячик с определенными свойствами:

        width(int) - ширина
        height(int) - высота
        x(int) - местоположение по x
        y(int) - местоположение по y
        direction(tuple) - ускорение ракетки
        speed_x(int) - скорость мячика по x
        speed_y(int) - скорость мячика по y
        color(tuple) - цвет в формате RGB
        rect(pygame.Rect) - объект класса Rect представляющий мячик
        iscollided(bool) - булево значение отвчеющие столкнулся ли мяч с рактекой
        
        Если мы хотим показать тип, то обычно пишем его не в скобках, а так width:int
        Здесь лучше использовать velocity вместо speed
        """
        self.width = 8
        self.height = 8
        self.x = pygame.display.Info().current_w // 2 - self.width // 2
        self.y = pygame.display.Info().current_h // 2 - self.height // 2
        self.direction = degrees_to_velocity(130, 5)
        self.speed_x = self.direction[0]
        self.speed_y = self.direction[1]
        self.color = (255, 255, 255)
        self.rect = None
        self.iscollided = False

    def draw(self, screen: pygame.Surface) -> None:
        """
        рисует мячик и присваиваем получившийся Rect к переменной

        screen - экран на котором нужно нарисовать мячик
        """
        self.rect = pygame.draw.rect(screen,
                                     self.color,
                                     (self.x, self.y,
                                      self.width, self.height))

    def move(self, players: list) -> None:
        """
        двигает мячик, в цикле изменяя его x и y координату на speed мячика

        players(list) - список с игроками
        """
        self.x += self.speed_x
        self.y += self.speed_y

        # Я бы вынес голы отсюда в логику класса Game
        if self.x <= 0:  # при ударе о левую стену
            self.x = pygame.display.Info().current_w // 2 - self.width // 2   # центрируем мячик по x
            self.y = pygame.display.Info().current_h // 2 - self.height // 2  # центрируем мячик по y
            pygame.mixer.Sound("goal.ogg").play()  # проигрываем звук удара
            players[1].score += 1  # засчитываем очко игроку

        if self.x >= pygame.display.Info().current_w - self.width:  # при ударе о правую стену
            self.x = pygame.display.Info().current_w // 2 - self.width // 2
            self.y = pygame.display.Info().current_h // 2 - self.height // 2
            pygame.mixer.Sound("goal.ogg").play()
            players[0].score += 1

        if self.y < 0:  # при ударе о верхнюю стену
            self.speed_y *= -1  # изменяем скорость
            pygame.mixer.Sound("wall.ogg").play()  # проигрываем звук удара

        if self.y > pygame.display.Info().current_h - self.height:  # при ударе о нижнюю стену
            self.speed_y *= -1
            pygame.mixer.Sound("wall.ogg").play()


def racket_collisions(ball: Ball, rackets: list) -> None:
    """
    функция отвечает за поведение мячика при столкновении с ракетками

    ball(Ball) - мячик
    rackets(list) - список с игроками
    
    Такое ощущение, что эта функция хочет быть частью класса Ball
    ball.iscollided дублирует стандартный метод colliderect, подумайте ещё, как прекратить коллизию сразу после изменеения скорости мяча
    """
    if ball.rect.colliderect(rackets[0].rect) and ball.iscollided is False or ball.rect.colliderect(rackets[1].rect) and ball.iscollided is False:  # О-о-о-очень длинно и непонятно. Is - плохая проверка для bool
        # условие выше срабатывает только тогда когда мячик сталкивается с одной из ракеток и его переменная iscollided равна False

        pygame.mixer.Sound("racket.ogg").play()  # проигрываем звук столковения
        ball.iscollided = True  # изменяем значение переменной iscollided
        ball.speed_x *= -1  # изменяем скорость

    elif ball.rect.left > rackets[0].rect.right and ball.rect.right < rackets[1].rect.left:
        # условие выше срабатывает лишь тогда когда мячик находится на относительно нейтральном расстоянии от обоих ракеток
        # Не понял камент выше
        ball.iscollided = False  # изменяем значение переменной iscollided


class Counter:
    def __init__(self) -> None:  # Как создать маленький красный счётчик для голов второго игрока в углу?
        """
        создает объекты класса Font со следующими свойствами:
        score_right - правый счетчик
        score_left - левый счетчик
        self.score_right_x - положение правого счетчика по x
        self.score_left_x - положение левого счетчика по x
        self.score_y - положение счетика по y, является общиим для обоих счетчиков
        self.right_img - переменная класса Surface для правого счетчика
        self.left_img - переменная класса Surface для левого счетчика
        
        У вас два счётчика score_right и score_left пытаются уместиться в один класс.
        Сделайте их САМОСТОЯТЕЛЬНЫМИ экземплярами
        """
        self.score_right = pygame.font.Font(size=30)
        self.score_left = pygame.font.Font(size=30)
        self.score_right_x = pygame.display.Info().current_w * 0.25
        self.score_left_x = pygame.display.Info().current_w * 0.75
        self.score_y = pygame.display.Info().current_h * 0.07
        self.right_img = None
        self.left_img = None

    def draw(self, players: list) -> None:
        """
        создаем объекты класса Surface с счетчиками обоих игроков методом render и рисуем их на экране методом blit

        players(list) - список с игроками
        """ 
        self.right_img = self.score_right.render(str(players[0].score), True, (255, 255, 255))  # вынесите цвета в константы!
        self.left_img = self.score_right.render(str(players[1].score), True, (255, 255, 255))
        screen.blit(self.left_img, (self.score_left_x, self.score_y))
        screen.blit(self.right_img, (self.score_right_x, self.score_y))


# Остальное явно просится в класс Game
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
    racket_collisions(ball, rackets)
    pygame.display.flip()
    clock.tick(60)
