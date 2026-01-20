#Создай собственный Шутер!
from pygame import *
from random import randint
from time import time as timer
class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, x, y, w, h, speed):
        super().__init__()
        self.image = transform.scale(image.load(sprite_image), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if key_pressed[K_RIGHT] and self.rect.x < 1200 - 100:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("lazer.png", self.rect.centerx - 15, self.rect.top, 30, 40, -30)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 800:
            self.rect.y = 0
            self.rect.x = randint(50, 1150)
            lost += 1 

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 800:
            self.rect.x = randint(50, 1150)
            self.rect.y = 0

monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()

for _ in range(3):
    asteroid = Asteroid("asteroid.png", randint(50, 1150), 0, 70, 70, randint(3, 5))
    asteroids.add(asteroid)
for _ in range(5):
    monster = Enemy("enemy2_1.png", randint(50, 1150), -20, 70, 70, randint(3, 5))
    monsters.add(monster)

window = display.set_mode((1200, 800))
display.set_caption("pygame")
backgroung = transform.scale(image.load('galaxy.jpg'), (1200, 800))
heart = transform.scale(image.load('life_bar.png'), (40, 40))
rocket = Player("player.png", 600, 600, 100, 100, 15)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play(-1)
mixer.music.set_volume(0.1)
kick = mixer.Sound("aug_clipout.mp3")

font.init()
font = font.SysFont("sitkasmall", 35)
win = font.render("Ты победил!", 1, (125, 60, 3))
lose = font.render("Ты проиграл!", 1, (125, 60, 3))
lost = 0
suma = 0
num_fire = 0 
life = 3
rel_time = False

clock = time.Clock()

game = True

finish = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    rocket.fire()
                    kick.play()
                    num_fire += 1
                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    start = timer()

    if finish != True:
        window.blit(backgroung, (0, 0))
        loser = font.render("Пропущено: " + str(lost), 1, (125, 60, 3))
        numder = font.render('Счет:' + str(suma), 1, (125, 60, 3))
        window.blit(numder, (50, 100))
        window.blit(loser, (50, 50))
        rocket.reset()
        rocket.update()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        asteroids.update()
        monsters.update()
        bullets.update() 

        if rel_time == True:
            end = timer()
            if end - start < 3:
                recharge = font.render("Перезарядка", 1, (125, 60, 3))
                window.blit(recharge, (50, 250))
            else:
                num_fire = 0
                rel_time = False

        sprite_list = sprite.groupcollide(monsters, bullets, True, True)
        if sprite.spritecollide(rocket, asteroids, True) or sprite.spritecollide(rocket, monsters, True):
            life -= 1
        if life == 3:
            window.blit(heart, (50, 500))
            window.blit(heart, (50, 550))
            window.blit(heart, (50, 600))
        if life == 2:
            window.blit(heart, (50, 500))
            window.blit(heart, (50, 550))

        if life == 1:
            window.blit(heart, (50, 500)) 

        for _ in sprite_list:
            suma += 1
            monster = Enemy("enemy2_1.png", randint(50, 1150), -20, 70, 70, randint(3, 5))
            monsters.add(monster)

        if suma >= 10:
            finish = True
            window.blit(win, (700, 700))

        if lost >= 4 or life == 0:
            loser.set_alpha(255)
            loser = font.render("Пропущено: " + str(lost), 1, (125, 60, 3))
            #window.blit(loser, (50, 100))
            finish = True
            window.blit(lose, (700, 700))
        
        display.update()
    time.delay(60)
