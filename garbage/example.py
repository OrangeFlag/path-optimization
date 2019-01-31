import sys, os, pygame, random
from pygame.locals import *

# Инициализируем переменные
# Начальное положение НЛО
x_coord = 1
y_coord = 320
# Начальная скорость НЛО
x_speed = 0
y_speed = 0
# Количество жизненной энергии НЛО
score = 1000
# Переменная-счетчик определяет когда
# астероиды изменяют направление движения
shag = 0
# Сдвиги по вертикали для астероидов
go1 = 0
go2 = 0
go3 = 0


def init_window():
    # Инициализируем pygame
    pygame.init()
    # Создаём игровое окно 550*480
    window = pygame.display.set_mode((550, 480))
    # Ставим свой заголовок окна
    pygame.display.set_caption('Астероиды')


# Функция отображения картинок
def load_image(name, colorkey=None):
    # Добавляем к имени картинки имя папки
    fullname = os.path.join('resource', name)
    # Загружаем картинку
    image = pygame.image.load(fullname)
    image = image.convert()
    # Если второй параметр =-1 делаем прозрачным
    # цвет из точки 0,0
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


def draw_background():
    # Получаем поверхность, на которой будем рисовать
    screen = pygame.display.get_surface()
    # и ее размер
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    # или загружаем картинку космоса
    back, back_rect = load_image("sky.jpg")
    # и рисуем ее
    screen.blit(back, (0, 0))
    # переключаем буфер экрана
    pygame.display.flip()
    return back


# Класс описывающий летающие объекты
class Skything(pygame.sprite.Sprite):
    def __init__(self, img, cX, cY):
        # Создаем спрайт из картинки
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(img, -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        # Перемещаем картинку в её начальные координаты
        self.rect.x = cX
        self.rect.y = cY


# Создаём дочерний класс NLO
class Nlo(Skything):
    def __init__(self, cX, cY):
        Skything.__init__(self, "1.png", cX, cY)


# Создаём дочерний класс Asteroid
class Asteroid(Skything):
    def __init__(self, cX, cY):
        Skything.__init__(self, "2.png", cX, cY)


def input(events):
    global x_coord, y_coord, x_speed, y_speed, life
    # Перехватываем нажатия клавиш на клавиатуре
    for event in events:
        if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit(0)
        # Когда нажаты стрелки изменяем скорость НЛО
        # чтобы оно летело
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: x_speed = -1
            if event.key == pygame.K_RIGHT: x_speed = 1
            if event.key == pygame.K_UP: y_speed = -1
            if event.key == pygame.K_DOWN: y_speed = 1
        # Когда стрелки не нажаты скорость ставим в ноль
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT: x_speed = 0
            if event.key == pygame.K_RIGHT: x_speed = 0
            if event.key == pygame.K_UP: y_speed = 0
            if event.key == pygame.K_DOWN: y_speed = 0
    # Меняем положение НЛО не выходя за рамки окна
    x_coord = x_coord + x_speed
    y_coord = y_coord + y_speed
    if (x_coord < 0): x_coord = 0
    if (x_coord > 430): x_coord = 430
    if (y_coord < 0): y_coord = 0
    if (y_coord > 320): y_coord = 320


def action(bk):
    global x_coord, y_coord, score, shag, go1, go2, go3
    screen = pygame.display.get_surface()
    # Создаём НЛО и астероиды
    nlo = Nlo(1, 320)
    asteroid = Asteroid(500, 100)
    asteroid2 = Asteroid(800, 200)
    asteroid3 = Asteroid(1200, 350)
    # Добавляем их в два массива
    asterow = []
    asterow.append(asteroid)
    asterow.append(asteroid2)
    asterow.append(asteroid3)
    air = []
    air.append(nlo)
    # Рисуем их
    asteroids = pygame.sprite.RenderPlain(asterow)
    nlos = pygame.sprite.RenderPlain(air)
    timer = pygame.time.Clock()
    # Запускаем бесконечный цикл
    while 1:
        # Создаем паузу
        timer.tick(700)
        # Ждём нажатий клавиатуры
        input(pygame.event.get())
        # Проверяем столкновения
        blocks_hit_list = pygame.sprite.spritecollide(nlo, asteroids, False)
        # Если есть столкновения уменьшаем жизнь
        if len(blocks_hit_list) > 0:
            score -= len(blocks_hit_list)
            asteroids.draw(screen)
            nlos.draw(screen)
            if (score < 1):
                pygame.quit()
                sys.exit(0)
        # Обновляем координаты НЛО
        nlo.rect.x = x_coord
        nlo.rect.y = y_coord
        # Изменяем положение астероидов
        asteroid.rect.x = asteroid.rect.x - 1
        asteroid2.rect.x = asteroid2.rect.x - 1
        asteroid3.rect.x = asteroid3.rect.x - 1
        if (asteroid.rect.x < 0):
            asteroid.rect.x = 500
            asteroid.rect.y = 100
        if (asteroid2.rect.x < 0):
            asteroid2.rect.x = 800
            asteroid2.rect.y = 200
        if (asteroid3.rect.x < 0):
            asteroid3.rect.x = 1200
            asteroid3.rect.y = 350
        # Раз в 300 итераций астероиды
        # меняют направление движения
        if (shag > 300):
            shag = 0
            go1 = random.randint(-1, 1)
            go2 = random.randint(-1, 1)
            go3 = random.randint(-1, 1)
        asteroid.rect.y += go1
        asteroid2.rect.y += go2
        asteroid3.rect.y += go3
        shag += 1
        # Заново прорисовываем объекты
        screen.blit(bk, (0, 0))
        font = pygame.font.Font(None, 25)
        white = (255, 255, 255)
        life = int(score / 10)
        text = font.render("Жизнь: " + str(life), True, white)
        # Рисуем надпись с жизнями
        screen.blit(text, [10, 10])
        # Обновляем положение объектов
        asteroids.update()
        nlos.update()
        # Обновляем кадр
        asteroids.draw(screen)
        nlos.draw(screen)
        pygame.display.flip()


def main():
    init_window()
    bk = draw_background()
    action(bk)


main()