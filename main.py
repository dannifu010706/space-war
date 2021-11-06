import random
import os
import pygame

FPS = 60
WIDTH = 500
HEIGHT = 600

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space War")
clock = pygame.time.Clock()
background_img = pygame.image.load(os.path.join("img","background.png")).convert()
rock_img = pygame.image.load(os.path.join("img","rocks.png")).convert()
player_img = pygame.image.load(os.path.join("img","spacec.png")).convert()
bullet_img = pygame.image.load(os.path.join("img","Capture.png")).convert()
font_name = pygame.font.match_font('arial')

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface= font.render(text, True,(255,255,255))
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def new_rock():
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)

def draw_health(surf, hp, x, y):
    if hp<0:
        hp=0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    fill_rect = pygame.Rect(x,y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, (0,255,255), fill_rect)
    pygame.draw.rect(surf,(255,255,255),outline_rect, 2)

def draw_init():
        draw_text(screen, 'Space War', 64, WIDTH/2, HEIGHT/4)
        draw_text(screen, 'Use ← → to control your spacecraft, press spacekey to shoot', 15, WIDTH/2, HEIGHT/2)
        draw_text(screen, 'Press any key to start', 18, WIDTH/2, HEIGHT*3/4)
        pygame.display.update()
        waiting = True
        while waiting:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYUP:
                    waiting = False
                    if event.key == pygame.K_SPACE:
                        player.shoot()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img,(50,38))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 8
        self.radius =20
        self.health=100

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = rock_img
        self.image = pygame.transform.scale(rock_img, (50, 38))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(2, 10)
        self.speedx = random.randrange(-3, 3)
        self.radius = int(self.rect.width*0.85/2)




    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 10)
            self.speedx = random.randrange(-3, 3)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img,(20,20))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
rock = Rock()

for i in range(8):
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)
score = 0

show_init = True
running = True
while running:
    if show_init:
        draw_init()
        show_init = False
    clock.tick(FPS)
    screen.fill((0, 0, 0))
    screen.blit(background_img,(0,0))
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH/2, 10)
    draw_health(screen,player.health,5,10)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    all_sprites.update()
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits:
        score += hit.radius
        new_rock()
    hits = pygame.sprite.spritecollide(player,rocks,True, pygame.sprite.collide_circle)
    for hit in hits:
        new_rock()
        player.health -= 20
        if player.health <= 0:
            running = False



pygame.quit()
