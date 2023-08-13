#Create your own shooter

from pygame import *
from random import randint
from time import time as timer
mixer.init()
mixer.music.load('fire.ogg')
#mixer.music.play()
fire_sound=mixer.Sound('fire.ogg')
img_back='space.jpg'
img_hero='ship.png'
img_enemy='ee.png'
img_bullete='bullet.png'
img_as='asteroid.png'
width=700
height=500
window=display.set_mode((width,height))
display.set_caption('space game')
background=transform.scale(image.load('space.jpg'),(width,height))
font.init()
font2=font.SysFont('Arial',30)

font1=font.SysFont('Arial',80)
win=font1.render('YOU WIN',True,(255,255,255))
lose=font1.render('YOU LOSE',True,(180,180,0))


score=0
lost=0
class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
         sprite.Sprite.__init__(self)
         self.image=transform.scale(image.load(player_image),(size_x,size_y))
         self.speed=player_speed
         self.rect=self.image.get_rect()
         self.rect.x=player_x
         self.rect.y=player_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def update(self):
        keys=key.get_pressed()
        if keys[K_LEFT] and self.rect.x>10:
            self.rect.x-=self.speed
        if keys[K_RIGHT] and self.rect.x<width-80:
            self.rect.x+=self.speed

    def fire(self):
        bx=self.rect.centerx
        by=self.rect.top
        bullet=Bullet(img_bullete,bx,self.rect.top,15,20,randint(15,30))
        Bullets.add(bullet)
        bullet=Bullet(img_bullete,self.rect.x,self.rect.top,15,20,randint(15,30))
        Bullets.add(bullet)
        bullet=Bullet(img_bullete,self.rect.x+10,self.rect.top,15,20,randint(15,30))
        Bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y+=self.speed
        global lost
        
        

        if self.rect.y>height:
            self.rect.x=randint(80,width-80)
            self.rect.y=0
            lost=lost+1


class ast(GameSprite):
    def update(self):
        self.rect.y+=self.speed
        if self.rect.y>height:
            self.rect.x=randint(80,width-80)
            self.rect.y=0


class Bullet(GameSprite):
    def update(self):
        self.rect.y-=self.speed
        if self.rect.y<0:
            self.kill()

Bullets=sprite.Group()

monsters=sprite.Group()     
for i in range(1,6):
    mx=randint(80,width-80)
    monster=Enemy(img_enemy,mx,-40,80,50,randint(1,2))
    monsters.add(monster)

asteroids=sprite.Group()     
for i in range(1,4):
    aster=randint(80,width-80)
    asteroid=ast(img_as,aster,-40,80,50,randint(1,2))
    asteroids.add(asteroid)


ship=Player(img_hero,5,height-100,80,100,10)
finish=False
life=5
nf=0
rl=False
run=True
while run:
    for e in event.get():
        if e.type==QUIT:
            run=False
        elif e.type==KEYDOWN:
            if e.key==K_SPACE:
                nf=nf
                if not nf>=3 and rl==False:
                    ship.fire()
                    fire_sound.play()
                if nf>=3 and rl==False: 
                    last_time=timer()
                    rl==True


    if not finish:

        window.blit(background,(0,0))
        text=font2.render('Score:'+str(score),1,(255,255,255))
        window.blit(text,(10,20))
        text_life=font2.render('life:'+str(life),1,(255,255,255))
        window.blit(text_life,(10,70))
        text_lose=font2.render('Missed:'+str(lost),1,(255,255,255))
        window.blit(text_lose,(10,50))  
        sprites_list=sprite.groupcollide(monsters,Bullets,True,True)

        for a in sprites_list:
            score+=1
            mx=randint(80,width-80)
            monster=Enemy(img_enemy,mx,-40,80,50,randint(1,5))
            monsters.add(monster)
        if sprite.spritecollide(ship,monsters,False) or  sprite.spritecollide(ship,asteroids,False):
            sprite.spritecollide(ship,monsters,True)
            sprite.spritecollide(ship,asteroids,True)
            life=life-1 
        if life==0 or lost>=5:
            finish=True
            window.blit(lose,(200,200))

        sprites_list=sprite.groupcollide(asteroids,Bullets,True,True)

        if score>=51:
            finish=True
            window.blit(win,(200,200))
        ship.update()
        monsters.update()
        Bullets.update()
        asteroids.update()
        ship.reset()
        asteroids.draw(window)
        monsters.draw(window)
        Bullets.draw(window)

        if rl==True:
            now_time=timer()
            if now_time-last_time<1:
                reload=font2.render('Wait,reload......',1,(150,0,0))
                window.blit(reload,(260,450))
            else:
                nf=0
                rl=False

        display.update()
    else:
        finish=False
        score=0
        lost=0
        life=5
        for w in Bullets:
            w.kill()
        for p in monsters:
            p.kill()
        for g in asteroids:
            g.kill()
        time.delay(3000)
        for i in range(1,6):
            mx=randint(80,width-80)
            monster=Enemy(img_enemy,mx,-40,80,50,randint(1,2))
            monsters.add(monster)
        for i in range(1,4):
            aster=randint(80,width-80)
            asteroid=ast(img_as,aster,-40,80,50,randint(1,2))
            asteroids.add(asteroid)
        if rl==True:
            now_time=timer()
            if now_time-last_time<3:
                reload=font2.render('Wait,reload......',1,(150,0,0))
                window.blit(reload,(260,450))
            else:
                nf=0
                rl=False
time.delay(50)