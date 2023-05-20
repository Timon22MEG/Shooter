from pygame import *
from random import randint
from time import time as timer

class GameSprite(sprite.Sprite):
    def __init__(self, _image, x, y, sprite_width, sprite_height, speed):
        super().__init__()
        self.image = transform.scale(image.load(_image), (sprite_width, sprite_height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < width - 85:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(image_bullet, self.rect.centerx - 6, self.rect.top, 15, 15, 20)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > height:
            self.rect.x = randint(80, width - 80)
            self.rect.y = -50
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

width = 700
height = 500

image_back = 'galaxy.jpg'
image_hero = 'rocket.png'
image_enemy1 = 'ufo.png'
image_enemy2 = 'asteroid.png'
image_bullet = 'bullet.png'

size = (width, height)
window = display.set_mode((size))
display.set_caption('Шутер')

background = transform.scale(image.load(image_back), size)

game = True

reload_bullets = 0

score = 0
lost = 0
max_score = 100
max_lost = 70
life = 3
max_bullets = 10
num_bullet = 0

font.init()
font1 = font.Font(None, 36)
font2 = font.Font(None, 80)
win = font2.render('YOU WIN!', True, (255, 255, 255))
lose = font2.render('YOU LOSE!', True, (180, 0, 0))

finish = False
clock = time.Clock()
FPS = 30

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

ship = Player(image_hero, width / 2, height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(7):
    monster = Enemy(image_enemy1, randint(80, width - 80), -40, 80, 50, randint(1, 7))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy(image_enemy2, randint(0, width - 50), -40, 50, 50, randint(1, 7))
    asteroids.add(asteroid)

bullets = sprite.Group()

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif  e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_bullet < 10 and reload_bullets == False:
                    fire_sound.play()
                    ship.fire()
                    num_bullet += 1
                if num_bullet >= 10 and reload_bullets == False:
                    last_time = timer()
                    reload_bullets = True

    if finish != True:
        window.blit(background, (0, 0))

        text = font1.render('Счёт: ' + str(score), True, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font1.render('Пропущено: ' + str(lost), True, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        ship.update()
        ship.reset()

        monsters.update()
        monsters.draw(window)

        bullets.update()
        bullets.draw(window)

        asteroids.update()
        asteroids.draw(window)

        if reload_bullets:
            now_time = timer()
            if now_time - last_time < 3:
                reload_text = font1.render('Wait, reload...', True, (150, 0, 0))
                window.blit(reload_text, (260, 460))
            else:
                num_bullet = 0
                reload_bullets = False

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life -= 1

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy(image_enemy1, randint(80, width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        
        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))
        
        if score >= max_score:
            finish = True
            window.blit(win, (200, 200))

        if life == 3:
            life_color = (0, 150, 0)
        elif life == 2:
            life_color = (150, 150, 0)
        elif life == 1:
            life_color = (150, 0, 0)

        life_text = font2.render(str(life), True, life_color)
        window.blit(life_text, (650, 10))

    else:
        finish = False
        score = 0
        lost = 0
        num_bullet = 0
        life = 3
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()
        
        time.delay(3000)
        for i in range(7):
            monster = Enemy(image_enemy1, randint(80, width - 80), -40, 80, 50, randint(1, 10))
            monsters.add(monster)

        
        for i in range(3):
            asteroid = Enemy(image_enemy2, randint(0, width - 50), -40, 50, 50, randint(1, 7))
            asteroids.add(asteroid)
        
    display.update()
    clock.tick(FPS)
