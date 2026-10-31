from pygame import *
from random import*

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, w, h, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w, h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 700 - 80:
            self.rect.x += self.speed
    def fire(self):
        peluru = Bullet('bullet.png',self.rect.centerx,self.rect.top,15, 20, 10)
        bullets.add(peluru)

class Ufo(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 490:
            self.rect.y = 10
            self.rect.x = randint(10, 625)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

player = player('rocket.png', 10, 425,80, 100, 5)
monster = sprite.Group()
for i in range(1,6):
    enemy = Ufo('ufo.png', randint(10,265), 10, 80,50,randint(1,5))
    monster.add(enemy)
bullets = sprite.Group()

window = display.set_mode((700, 500))
background = transform.scale(image.load('galaxy.jpg'), (700, 500))

font.init()
font1 = font.SysFont('Copperplate Gothic', 70)
font2 = font.SysFont('Colonna MT', 36)
menang =  font1.render('HOORAY!:', True, (255,255,0))
kalah = font1.render('kamu kalah!', True, (255, 0,0))
finish = False
game = True
clock = time.Clock()
FPS = 60
score = 0
lost = 0

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif  e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
        
    if finish != True:
        window.blit(background,(0, 0))
        player.update()
        bullets.draw(window)
        bullets.update()
        monster.draw(window)
        monster.update()
        skor = font2.render('Skor:'+str(score), True, (255, 255, 255))
        missed = font2.render('Missed:'+str(lost), True, (255, 255, 255))
        window.blit(skor, (5, 5))
        window.blit(missed, (5,35))

        collides = sprite.groupcollide(monster, bullets, True, True)
        for c in collides:
            score += 1
            enemy = Ufo('ufo.png', randint(10,625), 10, 80,50,randint(1,5))
            monster.add(enemy)
        if sprite.spritecollide(player, monster, False) or lost >= 3:
            window.blit(kalah, (200, 200))
            finish = True
        if score >= 10:
            finish = True
            window.blit(menang, (200,200))

        player.reset()
       



        if sprite.collide_rect(player, enemy):
            finish = True
            window.blit(kalah, (200, 200))
            #kick.play()

        #if sprite.collide_rect(enemy, peluru):
            #finish = True
            #window.blit(menang, (200, 200))
            #money.play()

        display.update()
        #bonus: automatic restart of the game
    else:
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monster:
            m.kill()


        time.delay(3000)
        for i in range(1, 6):
            enemy= Ufo('ufo.png', randint(10, 625), 10, 80, 50, randint(1, 5))
            monster.add(enemy)
    clock.tick(FPS)