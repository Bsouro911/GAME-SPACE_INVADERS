import pygame, random
pygame.font.init()
#pygame.mixer.init()

# MAKING OUR GAME WINDOW
WIDTH, HEIGHT= 1280, 720
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACE INVADERS BY - @Souro")

# --LOADING IMAGES--

# INVADING SPACESHPS
RED_SPACE_SHIP = pygame.transform.rotate(pygame.image.load("C:\\Users\\Sourojyoti Biswas\Desktop\Gspace_invaders\Assets\\red_spaceship.png"), 180)
GREEN_SPACE_SHIP = pygame.transform.rotate(pygame.image.load("C:\\Users\\Sourojyoti Biswas\Desktop\Gspace_invaders\Assets\\green_spaceship.png"), 180)
BLUE_SPACE_SHIP = pygame.transform.rotate(pygame.image.load("C:\\Users\\Sourojyoti Biswas\Desktop\Gspace_invaders\Assets\\blue_spaceship.png"), 180)

# PLAYER SPACESHIP
YELLOW_SPACE_SHIP = pygame.image.load("C:\\Users\\Sourojyoti Biswas\Desktop\Gspace_invaders\Assets\\yellow_spaceship.png")

# LASERS FOR INVADERS
RED_LASER = pygame.transform.rotate(pygame.image.load("C:\\Users\\Sourojyoti Biswas\Desktop\Gspace_invaders\Assets\\red_laser.png"), 180)
BLUE_LASER = pygame.transform.rotate(pygame.image.load("C:\\Users\\\Sourojyoti Biswas\Desktop\Gspace_invaders\Assets\\blue_laser.png"), 180)
GREEN_LASER = pygame.transform.rotate(pygame.image.load("C:\\Users\Sourojyoti Biswas\Desktop\Gspace_invaders\Assets\green_laser.png"), 180)

# LASER FOR PLAYER
YELLOW_LASER = pygame.image.load("C:\\Users\\Sourojyoti Biswas\Desktop\Gspace_invaders\Assets\yellow_laser.png")

#LASER FIRED SOUND
#LASER_FIRED_SOUND = pygame.mixer.Sound("C:\\Users\\Sourojyoti Biswas\Desktop\Gspace_invaders\Assets\lsersound.wav")

#COLLIDE SOUND
#LASER_COLLIDE = pygame.mixer.Sound("C:\\Users\\Sourojyoti Biswas\Desktop\Gspace_invaders\Assets\lsercollision.wav")

# BACKGROUND
BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load("C:\\Users\\Sourojyoti Biswas\Desktop\Gspace_invaders\Assets\space_background.png"),(WIDTH+50, HEIGHT+50))

#TITLE IMAGE
TITLE_IMAGE = pygame.transform.scale(pygame.image.load("C:\\Users\\Sourojyoti Biswas\Desktop\Gspace_invaders\Assets\\title.png"), (800, 340))
TITLE_IMAGE2 = pygame.transform.scale(pygame.image.load("C:\\Users\\Sourojyoti Biswas\Desktop\Gspace_invaders\Assets\\title2.png"), (600, 200))

class Laser:

    def __init__(self, x, y, img) -> None:
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
    
    def move (self, velocity):
        self.y += velocity
    
    def off_screen(self, height):
        return not(self.y <= height and self.y >=0)

    def collision(self, object):
        return collide(self, object)

class Ship:

    COOL_DOWN = 10

    def __init__(self, x, y, health = 100) -> None:
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        # pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, 50, 50))
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, velocity, object):
        self.cooldown()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(object):
                object.health -= 10
                self.lasers.remove(laser)


    def cooldown(self):
        if self.cool_down_counter >= self.COOL_DOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x+7.5, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):

    def __init__(self, x, y, health=100) -> None:
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, velocity, objects):
        self.cooldown()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for object in objects:
                    if laser.collision(object):
                        #LASER_COLLIDE.play()
                        objects.remove(object)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.health_bar(window)

    def health_bar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

class Enemy_ship(Ship):

    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green" : (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue" : (BLUE_SPACE_SHIP, BLUE_LASER)
    }

    def __init__(self, x, y, color, health=100) -> None:
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 20.5, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

def collide(object_1, object_2):
    offset_x = object_2.x - object_1.x
    offset_y = object_2.y - object_1.y
    return object_1.mask.overlap(object_2.mask, (offset_x, offset_y)) != None

def main():

    # --GAME LOOP--
    RUN = True
    FPS = 60
    LEVEL = 0
    LIVES = 50
    MAIN_FONT = pygame.font.Font("C:\\Users\\Sourojyoti Biswas\Desktop\Gspace_invaders\Assets\\SpaceArmor-vmlv4.otf", 18)
    LOST_FONT = pygame.font.Font("C:\\Users\\Sourojyoti Biswas\Desktop\Gspace_invaders\Assets\\SpaceArmor-vmlv4.otf", 26)

    ENEMIES = []
    WAVE_LENGTH = 5
    ENEMY_VEL = 1

    PLAYER_VELOCITY = 10
    PLAYER_LASER_VELOCITY = 10 
    ENEMY_LASER_VELOCITY = 4

    player = Player(300, 300)

    CLOCK = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_win():
        # BLITTING THE SURFACE
        WINDOW.blit(BACKGROUND_IMAGE, (0, 0))

        # DRAW TEXT
        LIVES_LABEL = MAIN_FONT.render(f"LIVES: {LIVES}", 1, (255, 255, 255))
        LEVEL_LABEL = MAIN_FONT.render(f"LEVEL: {LEVEL}", 1, (255, 255, 255))

        WINDOW.blit(LIVES_LABEL, (10, 10))
        WINDOW.blit(LEVEL_LABEL, (WIDTH - LEVEL_LABEL.get_width() - 10, 10))
        
        for enemy in ENEMIES:
            enemy.draw(WINDOW)
       
        player.draw(WINDOW)

        if lost:

            lost_label = LOST_FONT.render("YOU LOST!", 1, (255, 255, 255))
            WINDOW.blit(lost_label, (WIDTH//2 - lost_label.get_width()//2, 250))

        pygame.display.update()

    while RUN:
        CLOCK.tick(FPS)
        redraw_win()

        if LIVES <= 0 or player.health <= 0:
            lost = True
            lost_count += 1
        
        if lost:
            if lost_count > FPS * 3:
                RUN = False
            else:
                continue
        
        if len(ENEMIES) == 0:
            LEVEL += 1
            WAVE_LENGTH += 5
            for i in range(WAVE_LENGTH):
                enemy = Enemy_ship(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                ENEMIES.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit() 

        KEYS = pygame.key.get_pressed()
        if KEYS[pygame.K_LEFT] and player.x +PLAYER_VELOCITY > 0: # LEFT
            player.x -= PLAYER_VELOCITY

        if KEYS[pygame.K_RIGHT] and player.x + PLAYER_VELOCITY + player.get_width() < WIDTH + 10: # RIGHT
            player.x += PLAYER_VELOCITY

        if KEYS[pygame.K_UP] and player.y + PLAYER_VELOCITY > 10: # UP
            player.y -= PLAYER_VELOCITY

        if KEYS[pygame.K_DOWN] and player.y + PLAYER_VELOCITY  + player.get_height() + 20 < HEIGHT: # DOWN
            player.y += PLAYER_VELOCITY

        if KEYS[pygame.K_SPACE]:
            player.shoot()
            #LASER_FIRED_SOUND.play()

        for enemy in ENEMIES[:]:
            if LEVEL == 1:
                enemy.move(ENEMY_VEL)
                enemy.move_lasers(ENEMY_LASER_VELOCITY, player)
            
            elif LEVEL == 2:
                enemy.move(ENEMY_VEL+1)
                enemy.move_lasers(ENEMY_LASER_VELOCITY, player)

            elif LEVEL == 3:
                enemy.move(ENEMY_VEL+1)
                enemy.move_lasers(ENEMY_LASER_VELOCITY, player)

            elif LEVEL == 4:
                enemy.move(ENEMY_VEL+1)
                enemy.move_lasers(ENEMY_LASER_VELOCITY, player)

            elif LEVEL == 5:
                enemy.move(ENEMY_VEL+1)
                enemy.move_lasers(ENEMY_LASER_VELOCITY, player)

            elif LEVEL == 6:
                enemy.move(ENEMY_VEL+1)
                enemy.move_lasers(ENEMY_LASER_VELOCITY, player)

            elif LEVEL == 7:
                enemy.move(ENEMY_VEL+1)
                enemy.move_lasers(ENEMY_LASER_VELOCITY, player)

            elif LEVEL == 8:
                enemy.move(ENEMY_VEL+1)
                enemy.move_lasers(ENEMY_LASER_VELOCITY, player)

            elif LEVEL == 9:
                enemy.move(ENEMY_VEL+1)
                enemy.move_lasers(ENEMY_LASER_VELOCITY, player)

            elif LEVEL == 10:
                enemy.move(ENEMY_VEL+1)
                enemy.move_lasers(ENEMY_LASER_VELOCITY, player)
                    
            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                ENEMIES.remove(enemy)
                
            elif enemy.y + enemy.get_height() > HEIGHT:
                LIVES -= 1
                ENEMIES.remove(enemy)
    

        player.move_lasers(-PLAYER_LASER_VELOCITY, ENEMIES)

def main_menu():

    title_font = pygame.font.Font("C:\\Users\\Sourojyoti Biswas\Desktop\Gspace_invaders\Assets\\SpaceArmor-vmlv4.otf", 18)

    run = True
    while run:
        WINDOW.blit(BACKGROUND_IMAGE, (0,0))
        WINDOW.blit(TITLE_IMAGE, (WIDTH//2 - TITLE_IMAGE.get_width()//2, 50))
        WINDOW.blit(TITLE_IMAGE2, (WIDTH//2 - TITLE_IMAGE2.get_width()//2, 340))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            KEYS = pygame.key.get_pressed()
            if KEYS[pygame.K_p]:
                main()
            
            elif KEYS[pygame.K_q]:
                quit()

    pygame.quit()

if __name__ == "__main__":
    main_menu()

        # title_label = title_font.render("Press p to begin", 1, (255,255,255))
        # WINDOW.blit(title_label, (WIDTH//2 - title_label.get_width()//2, 410))
        # title_label = title_font.render("Press q to quit", 1, (255,255,255))
        # WINDOW.blit(title_label, (WIDTH//2 - title_label.get_width()//2, 430))