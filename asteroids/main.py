import pygame
import math
import random

pygame.init()

# Initialize the joysticks.
pygame.joystick.init()

display_width = 1000
display_height = 800

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('The asteroids clone')

BLACK = (0,0,0)
WHITE = (255,255,255)

clock = pygame.time.Clock()
done = False

playerSnd = pygame.mixer.Sound('sounds/miau.wav') 

def check_bounce(element, boundaries):
    if element.x < 0 or element.x > display_width:
        element.speedX = - element.speedX
    if element.y < 0 or element.y > display_height:
        element.speedY = - element.speedY

def detect_off_boundaries(element_list):
    for element in element_list:
        if element.x < 0 or element.x > display_width or element.y < 0 or element.y > display_height:
            element_list.remove(element)

def detect_fire_collision(fire_list, element_list):
    # Not working. Rects have to be calculated from the current x,y
    for fire in fire_list:
        for element in element_list:
            r = fire.is_collided_with(element)
            if r:
                #fire_list.remove(fire)
                print("BOOOOM!", r)




class Sprite:
    x = 0
    y = 0
    angle = 0
    speedX = 0
    speedY = 0
    image = None
    rect = None
    disposable = False

    def __init__(self, angle, initial_x, initial_y, image):
        self.x = initial_x
        self.y = initial_y
        self.angle = angle
        self.image = image
        self.rect = self.image.get_rect()

    def move(self):
        self.x += self.speedX
        self.y += self.speedY
    
    def display(self):
        image_center = self.image.get_rect().size
        centerX = self.x - image_center[0]/2 
        centerY = self.y - image_center[1]/2
        gameDisplay.blit(self.image, (centerX,centerY))

    def action(self):
        self.move()
        self.display()

    def is_collided_with(self, element):
        # Not working. Rects have to be calculated from the current x,y
        return self.image.get_rect().colliderect(element.image.get_rect())

class Player(Sprite):
    fire_list = []
    baseImg = None

    def __init__(self, angle, initial_x, initial_y):
        playerImg = pygame.image.load('graphics/ship.png') #84x108
        Sprite.__init__(self, angle, initial_x, initial_y, playerImg)
        self.baseImg = playerImg

    def rotate(self, degrees):
        self.angle += degrees
        self.angle %= 360 
        rotatedImage = pygame.transform.rotate(self.baseImg, self.angle)
        self.image = rotatedImage

    def move_fires(self):
        for f in self.fire_list:
            f.move()

    def accelerate(self, amount):
        rad_angle = self.angle/180 * math.pi
        self.speedX += -amount * math.sin(rad_angle)
        self.speedY += -amount * math.cos(rad_angle)

    def display(self):
        for f in self.fire_list:
            f.display()

        Sprite.display(self)

    def action(self):
        self.move_fires()
        Sprite.action(self)

    def shoot(self):
        rad_angle = self.angle/180 * math.pi
        shipnoseX = self.x - 40 * math.sin(rad_angle)
        shipnoseY = self.y - 40 * math.cos(rad_angle)
        # Initial speed should be relative to the ship's speed
        fire = Missile(self.angle, shipnoseX, shipnoseY)
        self.fire_list.append(fire)


class Missile(Sprite):
    def __init__(self, angle, initial_x, initial_y):
        image = pygame.image.load('graphics/fire.png')
        image = pygame.transform.rotate(image, angle)

        Sprite.__init__(self, angle, initial_x, initial_y, image)

        rad_angle = angle/180 * math.pi
        self.speedX += -15 * math.sin(rad_angle)
        self.speedY += -15 * math.cos(rad_angle)

        self.disposable = True

class Asteroid(Sprite):
    def __init__(self, angle, initial_x, initial_y, initial_speedX, initial_speedY):
        image = pygame.image.load('graphics/asteroid1.png')
        Sprite.__init__(self, angle, initial_x, initial_y, image)
        self.speedX = initial_speedX
        self.speedY = initial_speedY

x_change = 0
y_change = 0
pl1 = Player(angle=0, initial_x = display_width * 0.30, initial_y = display_height * 0.65)

fire = None
asteroids = []

# Asteroids init
total_asteroids = 10
for i in range(total_asteroids):
    asteroids.append(
                    Asteroid(random.randint(0,359),
                            random.randint(0, display_width),
                            random.randint(0, display_height),
                            random.randint(0, 10),
                            random.randint(0, 10))
                    )

# Get count of joysticks.
joystick_count = pygame.joystick.get_count()
print("%d joysticks found" %joystick_count)

if joystick_count >= 1:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pl1.rotate(10)

            elif event.key == pygame.K_RIGHT:
                pl1.rotate(-10)

            elif event.key == pygame.K_UP:
                #x_change = speed
                pl1.accelerate(1)
            
            elif event.key == pygame.K_SPACE:
                pl1.shoot()

        if event.type == pygame.JOYAXISMOTION:
            #print(event)
            
            y_axis_value = joystick.get_axis(1)
            x_axis_value = joystick.get_axis(0)

            if event.joy == 0:
                angle += x_axis_value * 10
        
        if event.type == pygame.JOYBUTTONDOWN:
            playerSnd.play()          

    # BACKGROUND
    gameDisplay.fill(BLACK)

    # PLAYER
    pl1.action()
    check_bounce(pl1, None)

    # ASTEROIDS
    for asteroid in asteroids:
        check_bounce(asteroid, None)
        asteroid.action()

    # MISSILES AND OTHER NON BOUNCING OBJECTS
    detect_off_boundaries(pl1.fire_list)
    #detect_fire_collision(pl1.fire_list, asteroids)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()