from os import path # imports
import pygame
import random
import pickle

WIDTH = 550
HEIGHT = 750
FPS = 60

images_dir = path.join(path.dirname(__file__), 'images')
sounds_dir = path.join(path.dirname(__file__), 'sounds')

# ========================================== COLOUR DEFINITIONS =======================================================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DGREEN = (0, 175, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)

# ========================================== END OF - COLOUR DEFINITIONS ==============================================

# ======================================== INITIALIZE PYGAME AND CREATE WINDOW ========================================
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fusion Driver") # setting game name to window
clock = pygame.time.Clock()
font_name = pygame.font.match_font("impact") # setting variables for fonts to use
font_name1 = pygame.font.match_font("impact")
font_name2 = pygame.font.match_font("impact")
# lane1 = (int(WIDTH / 5) / 2, -64)
# lane2 = (((int(WIDTH / 5) + int(WIDTH / 5 * 2)) / 2), -64)
# lane3 = (((int(WIDTH / 5 * 2) + int(WIDTH / 5 * 3)) / 2), -64)
# lane4 = (((int(WIDTH / 5 * 3) + int(WIDTH / 5 * 4)) / 2), -64)
# lane5 = (((int(WIDTH / 5 * 4) + WIDTH) / 2), -64)
player_img = pygame.image.load(path.join(images_dir, "SportsRacingCar_00.png")).convert() # loading plater and background imagesC:\Users\vjosh\AppData\Local\Temp\Fusion_Driver.py
player_right = pygame.image.load(path.join(images_dir, "SportsRacingCar_06.png")).convert()
player_left = pygame.image.load(path.join(images_dir, "SportsRacingCar_04.png")).convert()
background = pygame.image.load(path.join(images_dir, "chikyuu_16_edge.png")).convert()
background_rect = background.get_rect()
ENEMY_SPEED = 5000 # setting speeds for enemies and powerups
POWERUP_SPEED = 7500
try: # making the highscore function using the "pickle" import
    with open('score.dat', 'rb') as file:
        highscore = pickle.load(file)
except:
    highscore = 0

enemy_images = [] # Loading enemy images into a list
enemy_list = ['glooRotated00.png', 'BluglooRotated00.png', 'RedglooRotated00.png']

for img in enemy_list:
    enemy_images.append(pygame.image.load(path.join(images_dir, img)).convert())
all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()


def draw_text(surf, text, size, x, y): # text functions
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_text1(surf, text, size, x, y):
    font = pygame.font.Font(font_name1, size)
    text_surface = font.render(text, True, RED)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_text2(surf, text, size, x, y):
    font = pygame.font.Font(font_name2, size)
    text_surface = font.render(text, True, YELLOW)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_health_bar(surf, x, y, percent): # making and customizing health bar
    if percent < 0:
        percent = 0
    BAR_LENGTH = 150
    BAR_HEIGHT = 25
    fill = (percent / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect1 = pygame.Rect(x, y, int(fill), BAR_HEIGHT)
    fill_rect2 = pygame.Rect(x, y, int(fill), int(BAR_HEIGHT / 2))
    pygame.draw.rect(surf, DGREEN, fill_rect1)
    pygame.draw.rect(surf, GREEN, fill_rect2)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def game_over_screen(): # making title screen function and cool down timer for title screen
    screen.blit(background, background_rect)
    draw_text(screen, "Fusion Driver", 70, int(WIDTH / 2), int(HEIGHT / 4))
    draw_text(screen, "Use the arrow keys or the A and W keys, to move and dodge the enemies!", 16, int(WIDTH / 2), int((HEIGHT * 3) / 5))
    draw_text1(screen, "Press any key to start", 16, int(WIDTH / 2), int(HEIGHT * 3 / 4))
    timer = 0
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        timer += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP and timer >= 100:
                waiting = False

class Player(pygame.sprite.Sprite): # player class
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (114, 114)) # loading player image
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = 1
        pygame.draw.circle(self.image, RED, self.rect.center, self.radius) # making circle hit detection value for player
        self.rect.centerx = int(WIDTH / 2) # spawn location for player
        self.rect.bottom = HEIGHT - 100
        self.speedx = 0 # speed of player
        self.health = 100 # health for healthbar
        self.radius = int(self.rect.width * .85 / 2)
        pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.multiplier = 1 # timers for hide and powerup functions
        self.timer = 0
        self.shield_timer = 0
        self.powerup_timer = 0
        self.immortality = False
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()

    def update(self):
        self.speedx = 0
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_LEFT]: # moving player left and right
            self.speedx = -7 * self.multiplier
            self.image = pygame.transform.scale(player_left, (114, 114))
            self.image.set_colorkey(WHITE)
        if key_state[pygame.K_RIGHT]:
            self.speedx = 7 * self.multiplier
            self.image = pygame.transform.scale(player_right, (114, 114))
            self.image.set_colorkey(WHITE)
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_a]:
            self.speedx = -7 * self.multiplier
            self.image = pygame.transform.scale(player_left, (114, 114))
            self.image.set_colorkey(WHITE)
        if key_state[pygame.K_d]:
            self.speedx = 7 * self.multiplier
            self.image = pygame.transform.scale(player_right, (114, 114))
            self.image.set_colorkey(WHITE)
        self.rect.x += int(self.speedx)
        if self.rect.right > WIDTH: # retricting player movement (making range for player to move)
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.speedx == 0:
            self.image = pygame.transform.scale(player_img, (114, 114))
            self.image.set_colorkey(WHITE)
        if self.multiplier > 1: # multiplier for "bolt" powerup increasing player speed temporarily
            self.timer += 1
        if self.timer >= 500:
            self.multiplier /= 2
            self.timer = 0
        if self.immortality == True: # making player invinsible temporarily if self.immortality == True
            if self.shield_timer > 0:
                self.shield_timer -= 1
                self.immortality = True
            if self.shield_timer == 0:
                self.immortality = False
                self.shield_timer = 0
        if self.powerup_timer >= 500: # making countdown for player powerups
            self.powerup_timer -= 1
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000: # hiding player
            self.hidden = False
            self.rect.centerx = int(WIDTH / 2)
            self.rect.bottom = HEIGHT - 100

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = ((int(WIDTH / 2)), int(HEIGHT + 200))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, lane):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale((random.choice(enemy_images)), (55, 45)) # loading enemy images
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.speedy = random.randrange(3, 7) # random speeds for enemies
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        # self.rect.x = int(WIDTH / 2)
        # self.rect.y = -64
        self.lane = lane # making enemies spawn in lanes at different speeds at different places above screen
        if self.lane == 1:
            self.rect.centerx = int((WIDTH / 5) / 2)
            self.rect.y = -550
        if self.lane == 2:
            self.rect.centerx = int(((WIDTH / 5) + int(WIDTH / 5 * 2)) / 2)
            self.rect.y = -250
        if self.lane == 3:
            self.rect.centerx = int((((WIDTH / 5 * 2) + int(WIDTH / 5 * 3)) / 2))
            self.rect.y = -495
        if self.lane == 4:
            self.rect.centerx = int(((WIDTH / 5 * 3) + int(WIDTH / 5 * 4)) / 2)
            self.rect.y = -475
        if self.lane == 5:
            self.rect.centerx = int((((WIDTH / 5 * 4) + WIDTH) / 2))
            self.rect.y = -1100

    def update(self): # if enemies go below screen they die
        self.rect.y += self.speedy
        if self.rect.bottom > HEIGHT:
            self.kill()


class Explosion(pygame.sprite.Sprite): # making explosion class
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update < self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_animation[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_animation[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Powerup(pygame.sprite.Sprite):
    def __init__(self, lane):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'heart', 'bolt']) # setting set images for each type of powerup
        self.image = pygame.transform.scale(powerup_images[self.type], (36, 36))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.speedy = 2 # making powerups spawn in lanes at same speed at different places above screen
        self.lane = lane
        if self.lane == 1:
            self.rect.centerx = int((WIDTH / 5) / 2)
            self.rect.y = -550
        if self.lane == 2:
            self.rect.centerx = int(((WIDTH / 5) + int(WIDTH / 5 * 2)) / 2)
            self.rect.y = -250
        if self.lane == 3:
            self.rect.centerx = int((((WIDTH / 5 * 2) + int(WIDTH / 5 * 3)) / 2))
            self.rect.y = -495
        if self.lane == 4:
            self.rect.centerx = int(((WIDTH / 5 * 3) + int(WIDTH / 5 * 4)) / 2)
            self.rect.y = -475
        if self.lane == 5:
            self.rect.centerx = int((((WIDTH / 5 * 4) + WIDTH) / 2))
            self.rect.y = -1100

    def update(self): # if powerups go below screen they die
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

powerup_images = {} # loading powerup images
powerup_images['shield'] = pygame.image.load(path.join(images_dir, "shield.png"))
powerup_images["bolt"] = pygame.image.load(path.join(images_dir, "bolt.png"))
powerup_images["heart"] = pygame.image.load(path.join(images_dir, "heart.png"))

#spawning sprites
player = Player()
all_sprites.add(player)
enemy = Enemy(1)
all_sprites.add(enemy)
enemy_sprites.add(enemy)
enemy = Enemy(2)
all_sprites.add(enemy)
enemy_sprites.add(enemy)
enemy = Enemy(3)
all_sprites.add(enemy)
enemy_sprites.add(enemy)
enemy = Enemy(4)
all_sprites.add(enemy)
enemy_sprites.add(enemy)
enemy = Enemy(5)
all_sprites.add(enemy)
enemy_sprites.add(enemy)
now = pygame.time.get_ticks()
last_spawn = now
powerups = pygame.sprite.Group()
last_powerspawn = now

# loading explosion images
explosion_animation = {}
explosion_animation["large"] = []
explosion_animation["small"] = []
explosion_animation["player"] = []

for i in range(45): # animating explosions
    filename = 'explosion1_00{}.png'.format(i) #WrathGames Studio [http://wrathgames.com/blog]
    img = pygame.image.load(path.join(images_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_large = pygame.transform.scale(img, (512, 384))
    explosion_animation["large"].append(img_large)
    img_small = pygame.transform.scale(img, (128, 96))
    explosion_animation["small"].append(img_small)
    filename = 'explosion1_00{}.png'.format(i)
    img = pygame.image.load(path.join(images_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_animation['player'].append(img)

# loading background music
pygame.mixer.music.load(path.join(sounds_dir, "Zodik - Future Travel.ogg"))  # Copyright Zodik
pygame.mixer.music.set_volume(0.3)  # lowering music volume

explosion_sounds = []  # laoding explosion sounds into list
for sound in ['explosion.wav', 'explosion1.ogg']:  # WrathGames Studio [http://wrathgames.com/blog]
    explosion_sounds.append(pygame.mixer.Sound(path.join(sounds_dir, sound)))
for i in explosion_sounds:
    pygame.mixer.Sound.set_volume(i, 0.1) # lowering volume of sounds in list

powerup_sounds = [] # loading powerup sounds into list
for sound in ['SFX_Powerup_17.wav', 'SFX_Powerup_18.wav', 'SFX_Powerup_19.wav']:  # WrathGames Studio [http://wrathgames.com/blog]
    powerup_sounds.append(pygame.mixer.Sound(path.join(sounds_dir, sound)))
for i in powerup_sounds:
    pygame.mixer.Sound.set_volume(i, 0.1) # lowering volume of sounds in list




# setting variabes for game_over and score/ looping background music
game_over = True
score = 0
pygame.mixer.music.play(loops=-1)
# ======================================== END OF - INITIALIZE PYGAME AND CREATE ======================================

# ===================================================== GAME LOOP =====================================================
done = False
while not done:
    # keep loop running at the right speed
    clock.tick(FPS)

    if game_over == True: # making game over screen True and reloading enemies and reseting score
        game_over_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        enemy_sprites = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)

        if now - last_spawn > ENEMY_SPEED:
            enemy = Enemy(1)
            all_sprites.add(enemy)
            enemy_sprites.add(enemy)
            enemy = Enemy(2)
            all_sprites.add(enemy)
            enemy_sprites.add(enemy)
            enemy = Enemy(3)
            all_sprites.add(enemy)
            enemy_sprites.add(enemy)
            enemy = Enemy(4)
            all_sprites.add(enemy)
            enemy_sprites.add(enemy)
            enemy = Enemy(5)
            all_sprites.add(enemy)
            enemy_sprites.add(enemy)
            last_spawn = pygame.time.get_ticks()

        score = 0

    # making score and powerup countdown increase and decrease to show player score and time untill powerup runs out
    score += 1
    player.powerup_timer -= 1
    now = pygame.time.get_ticks()
    hits = pygame.sprite.spritecollide(player, enemy_sprites, True, pygame.sprite.collide_circle)

    for hit in hits: # for explsoions and death explosion hits loop
        if player.immortality == False:
            explosion = Explosion(hit.rect.center, "small")
            all_sprites.add(explosion)
            random.choice(explosion_sounds).play()
            player.health -= 20

        if player.health <= 0:
            death_explosion = Explosion(player.rect.center, 'large')
            all_sprites.add(death_explosion)
            player.hide() # hiding player before sending back to title screen

    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits: # powerup hits loop
        if hit.type == "heart":
            player.health += 30
            random.choice(powerup_sounds).play()
        if hit.type == "bolt":
            powerup_hit = now
            player.multiplier *= 2
            random.choice(powerup_sounds).play()
            player.powerup_timer += 500
        if hit.type == "shield":
            player.immortality = True
            random.choice(powerup_sounds).play()
            player.powerup_timer += 500
            player.shield_timer += 500

        if score > highscore:
            highscore = score
            with open('score.dat', 'wb') as file:
                pickle.dump(highscore, file)

    if player.health <= 0 and not death_explosion.alive():
        game_over = True

    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            done = True

    if now - last_spawn > ENEMY_SPEED: # spanwiing enemies in loop at a set rate
        enemy = Enemy(1)
        all_sprites.add(enemy)
        enemy_sprites.add(enemy)
        enemy = Enemy(2)
        all_sprites.add(enemy)
        enemy_sprites.add(enemy)
        enemy = Enemy(3)
        all_sprites.add(enemy)
        enemy_sprites.add(enemy)
        enemy = Enemy(4)
        all_sprites.add(enemy)
        enemy_sprites.add(enemy)
        enemy = Enemy(5)
        all_sprites.add(enemy)
        enemy_sprites.add(enemy)
        last_spawn = pygame.time.get_ticks()

    if score >= 1000: # increasing number of enemies spawning as score increase
        ENEMY_SPEED = 4500
    if score >= 3000:
        ENEMY_SPEED = 4000
    if score >= 5000:
        ENEMY_SPEED = 3500
    if score >= 7000:
        ENEMY_SPEED = 3000
    if score >= 9000:
        ENEMY_SPEED = 2500
    if score >= 11000:
        ENEMY_SPEED = 2250

    if now - last_powerspawn > POWERUP_SPEED: # looping spawn of powerups
        powerup = Powerup(random.randrange(1, 5))
        all_sprites.add(powerup)
        powerups.add(powerup)
        last_powerspawn = now

    if score >= 1000: # decreasing number of powerups that spawn as score increases
        POWERUP_SPEED = 8000
    if score >= 3000:
        POWERUP_SPEED = 8000
    if score >= 5000:
        POWERUP_SPEED = 8250
    if score >= 7000:
        POWERUP_SPEED = 8500
    if score >= 9000:
        POWERUP_SPEED = 9000
    if score >= 11000:
        POWERUP_SPEED = 9500

    if player.powerup_timer <= 0: # timer cannot go below 0
        player.powerup_timer = 0

    if player.health >= 100: # player health cannot go over 100 (heart powerup allows +30 health)
        player.health = 100

    # --------------------------------------------------- UPDATE --------------------------------------------------
    all_sprites.update()

    # --------------------------------------------------- DRAW ----------------------------------------------------
    # drawing screen, lanes, player, enemies, score, health bar, powerup timer, and highscore
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    pygame.draw.line(screen, WHITE, [int(WIDTH / 5), 0], [int(WIDTH / 5), HEIGHT])
    pygame.draw.line(screen, WHITE, [int(WIDTH / 5 * 2), 0], [int(WIDTH / 5 * 2), HEIGHT])
    pygame.draw.line(screen, WHITE, [int(WIDTH / 5 * 3), 0], [int(WIDTH / 5 * 3), HEIGHT])
    pygame.draw.line(screen, WHITE, [int(WIDTH / 5 * 4), 0], [int(WIDTH / 5 * 4), HEIGHT])
    pygame.draw.line(screen, WHITE, [WIDTH - 1, 0], [WIDTH - 1, HEIGHT])
    pygame.draw.line(screen, WHITE, [1, 0], [1, HEIGHT])
    all_sprites.add(player)
    all_sprites.draw(screen)
    pygame.draw.rect(screen, (100, 100, 100), [30, 15, 160, 35])
    draw_health_bar(screen, 35, 20, player.health)
    draw_text(screen, str(score), 20, int(WIDTH / 2), 25)
    draw_text1(screen, "Highscore: " + str(highscore), 20, int(WIDTH / 5 * 4), 25)
    draw_text2(screen, str(round(player.powerup_timer / 100)), 20, int(WIDTH / 2), 50)


  # ---------------------------------------------- REFRESH THE SCREEN -------------------------------------------
    pygame.display.flip()
pygame.quit()


