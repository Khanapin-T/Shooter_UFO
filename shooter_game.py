#Создай собственный Шутер!
from pygame import *
from random import randint
score = 0
lost = 0
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y, hp):
        super().__init__(player_image, player_x, player_y, player_speed, size_x, size_y)
        self.hp = hp
        
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 70:
            self.rect.x += self.speed

    def Fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx - 8, self.rect.top, 20, 15, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= 460:
            self.speed = randint(1, 3)
            self.rect.x = randint(80, 620)
            lost += 1
            self.rect.y = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, 620)
            self.rect.y = 0

player = Player('rocket.png', 300, 420, 8, 60, 80, 10)
health = GameSprite('health.png', randint(90, 610), randint(100, 300), 0, 40, 30)

monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()

for i in range(1, 6):
    monster = Enemy('ufo.png', randint(90, 610), 0, randint(1, 2), 70, 40)
    monsters.add(monster)

for i in range(3):
    asteroid = Asteroid('asteroid.png', randint(90, 610), 0, randint(1, 2), 70, 40)
    asteroids.add(asteroid)

mixer.init()
mixer.music.load('music_fon.ogg')
mixer.music.set_volume(0.2)
mixer.music.play()

fps = 60
clock = time.Clock()

game = True
finish = False

font.init()
font1 = font.Font(None, 30)
font2 = font.Font(None, 80)
win_text = font2.render('YOU WIN', True, (0, 255, 0))
lose_text = font2.render('YOU LOSE', True, (255, 0, 0))

goal = 15

fire_sound = mixer.Sound('fire.ogg')
fire_sound.set_volume(0.1)

win_sound = mixer.Sound('ura_pobeda.ogg')
win_sound.set_volume(0.4)

lose_sound = mixer.Sound('win_lose.ogg')
lose_sound.set_volume(0.2)

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.Fire()

    if finish != True:
        window.blit(background, (0, 0))
        player.update()
        bullets.update()
        monsters.update()
        asteroids.update()

        player.reset()
        health.reset()
        bullets.draw(window)
        monsters.draw(window)
        asteroids.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for collide in collides:
            score += 1
            monster = Enemy('ufo.png', randint(70, 630), 0, randint(1, 2), 70, 40)
            monsters.add(monster)
        
        if sprite.spritecollide(player, monsters, True) or lost >= 7:
            if player.hp > 1:
                player.hp -= 1
                monster = Enemy('ufo.png', randint(70, 630), 0, randint(1, 2), 70, 40)
                monsters.add(monster)
            else:
                finish = True
                window.blit(lose_text, (200, 200))
                lose_sound.play()
                mixer.music.stop()

        if sprite.spritecollide(player, asteroids, True) or lost >= 7:
            if player.hp > 1:
                player.hp -= 2
                asteroid = Asteroid('asteroid.png', randint(90, 610), 0, randint(1, 2), 70, 40)
                asteroids.add(asteroid)
            else:
                finish = True
                window.blit(lose_text, (200, 200))
                lose_sound.play()
                mixer.music.stop()

        if sprite.spritecollide(health, bullets, True):
            player.hp += 1
            health.rect.x = randint(90, 610)
            health.rect.y = randint(100, 300)

        if score >= goal:
            finish = True
            window.blit(win_text, (200, 200))
            mixer.music.stop()
            win_sound.play()

        score_sc = font1.render('Счет: ' + str(score), True, (255, 255, 255))
        lost_sc = font1.render('Пропущено: ' + str(lost) + ' из 7',  True, (255, 255, 255))
        now = font1.render('Цель: ' + str(goal), True, (255, 255, 255))
        text_hp = font1.render('Количество жизней: '+ str(player.hp), 1, (255, 255, 255))
        window.blit(now, (5, 20))
        window.blit(score_sc, (5, 40))
        window.blit(lost_sc, (5, 60))
        window.blit(text_hp, (5, 80))

        display.update()
    clock.tick(fps)