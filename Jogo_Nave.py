import pygame as pg
import pygame.freetype as freetype
import random
import os



image_evil = pg.image.load(os.path.join('covidpix.png'))
image_player = pg.image.load(os.path.join('navepixgr.png'))
image_shoot = pg.image.load(os.path.join('vacinapix3.png'))
image_background = pg.image.load(os.path.join('fundopix4.jpg'))
record_file = os.path.join('record.txt')
try:
    with open(record_file, 'x') as f:
        f.write(str(0))
except (BaseException, OSError):
    pass

class Menu():
    def __init__(self):

        self.font = freetype.SysFont('Consolas', 25)
        self.score, self.missed = 0, 0
        self.stop = True
        self.white = pg.Color('Black')
        self.red = pg.Color('White')
        self.text1 = ''
        self.text2 = 'INICIAR'
        self.r1 = self.font.get_rect('GAME OVER', size=60)
        self.r2 = self.font.get_rect(self.text2)
        self.level_list = ['GR12']

    def start(self):
        if self.stop:
            tela.blit(jogador.image, (
                (WIDTH - jogador.rect.w) // 2, HEIGHT - jogador.rect.h - 30))
            self.font.render_to(
                tela, (10, 10), f'Pontuação: {self.score}', fgcolor=self.white)
            self.font.render_to(
                tela, (10, 40), f'Recorde: {rec[0]}', fgcolor=self.white)

            self.font.render_to(
                tela, ((WIDTH - self.r1.w) // 2, (HEIGHT - self.r1.h) // 2),
                self.text1, fgcolor=self.red, size= 100)

            button = pg.draw.rect(
                tela, self.white, (WIDTH - 130, 10, 120, 40), border_radius=90)
            self.font.render_to(tela, (
                button.x + (button.w - self.r2.w) // 2,
                button.y + (button.h - self.r2.h) // 2),
                self.text2, fgcolor=self.red)

            button_level = pg.draw.rect(
                tela, self.red, ((WIDTH - 70) // 2, 10, 70, 30), border_radius=5)
            level = self.font.render_to(tela, (
                button_level.x + (10 if self.level_list[0] == 'lov' else 3),
                button_level.y + 3), self.level_list[0], fgcolor=self.white)

            todas_as_sprites.empty()
            e = pg.event.get(pg.MOUSEBUTTONDOWN)
            if e and button.collidepoint(e[0].pos) and e[0].button == 1:
                self.text1 = 'PERDEU'
                self.score, self.missed = 0, 0
                tiro.position.xy = jogador.rect.center = WIDTH // 2, HEIGHT // 2
                tiro.angle = jogador.angle = 0
                tiro.velocity = vec(0, 0).rotate(tiro.angle)
                tiro.image = pg.transform.rotate(tiro.orig_image, tiro.angle)
                todas_as_sprites.add(tiro, jogador)
                for _ in range(10):
                    todas_as_sprites.add(Covid())
                self.stop = False
            elif e and button_level.collidepoint(e[0].pos) and e[0].button == 1:
                self.level_list.reverse()
        else:
            self.font.render_to(tela, (10, 10), str(self.score), fgcolor=self.white)
            self.font.render_to(tela, (10, 40), str(self.missed), fgcolor=self.red)
            if self.score < self.missed:
                self.stop = True
                if self.score > rec[0]:
                    rec[0] = my_record()



class Jogador(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = image_player
        self.angle = 0
        self.speed = 5
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_DOWN]:
            self.rect.y += self.speed
            if self.rect.bottom >= HEIGHT:
                self.rect.bottom = HEIGHT
        elif keys[pg.K_UP]:
            self.rect.y -= self.speed
            if self.rect.top <= 0:
                self.rect.top = 0
        elif keys[pg.K_RIGHT]:
            self.angle -= 1
            if self.angle <= -30:
                self.angle = -30
            self.rect.x += self.speed
            if self.rect.right >= WIDTH:
                self.rect.right = WIDTH
        elif keys[pg.K_LEFT]:
            self.angle += 1
            if self.angle >= 30:
                self.angle = 30
            self.rect.x -= self.speed
            if self.rect.left <= 0:
                self.rect.left = 0

        self.image = pg.transform.rotate(image_player, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)


class Tiro(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = image_shoot
        self.orig_image = self.image.copy()
        self.rect = self.image.get_rect()



        self.position = vec(jogador.rect.center)
        self.velocity = vec()
        self.speed = 10
        self.block = True
        self.collide = False
        self.angle = jogador.angle

    def update(self):
        if self.position.y < -self.rect.h // 2 or self.collide:
            self.position = jogador.rect.center
            self.angle = jogador.angle
            self.image = pg.transform.rotate(self.orig_image, self.angle)
            self.rect = self.image.get_rect(center=self.position)
            self.collide = False

        self.velocity = vec(0, -self.speed).rotate(-self.angle)
        self.position += self.velocity
        self.rect.center = self.position


class Covid(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.transform.rotozoom(
            image_evil, random.randrange(-60, 61, 10), random.randint(4, 8) * 0.1)
        self.rect = self.image.get_rect(bottomright=(random.randint(0, WIDTH), 0))
        self.speed = random.randint(1, 2)
        if menu.level_list[0] == 'lov':
            self.radius = self.rect.h // 2
        else:
            self.radius = self.rect.h // 4

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.bottomright = random.randint(0, WIDTH), 0
            self.speed = random.randint(1, 2)
            menu.missed += 1
        if pg.sprite.collide_circle(tiro, self):
            self.rect.bottomright = random.randint(0, WIDTH), 0
            self.speed = random.randint(1, 2)
            menu.score += 1
            tiro.collide = True


WIDTH, HEIGHT = 600, 730
BG_COLOR = (0,0,25)

pg.init()
vec = pg.math.Vector2
tela = pg.display.set_mode((600, 730,))
FPS = 90
clock = pg.time.Clock()
todas_as_sprites = pg.sprite.Group()
menu = Menu()
jogador = Jogador()
tiro = Tiro()


def my_record():
    with open(record_file, 'r+') as f:
        record = f.read()
        if menu.score > int(record):
            record = str(menu.score)
            f.seek(0)
            f.truncate()
            f.write(record)
    return int(record)



rec = [my_record()]
while not pg.event.get(pg.QUIT):

    tela.blit(image_background, (0,0))
    if not menu.stop:
        todas_as_sprites.update()
        todas_as_sprites.draw(tela)
    menu.start()


    pg.display.update()
    clock.tick(FPS)
    pg.display.set_caption(f'Grupo 12   {round(clock.get_fps())}')

