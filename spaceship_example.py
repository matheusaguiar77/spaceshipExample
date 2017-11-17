import pygame
import math
import sys
from pygame.locals import *
import random

#init important modules of pygame
pygame.init()

#create game screen
screen = pygame.display.set_mode((800, 640), DOUBLEBUF)
pygame.display.set_caption("Spaceship Example")

#create a clock to manage time (FPS)
clock = pygame.time.Clock()

#Class representing the spaceship support base
class PitStopSprite(pygame.sprite.Sprite):
    image = './img/pitstop.png'
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)

        self.position = position
        self.src_image = pygame.image.load( self.image )
        self.image = self.src_image
        self.rect = self.image.get_rect()


#Class representing the Asteroids objects
class AsteroidSprite(pygame.sprite.Sprite):
    images = {0 : ["./img/asteroid_normal.png", "./img/asteroid_hit.png"],
            2 : ["./img/asteroid_2.png", None],
            4 : ["./img/asteroid_4.png", None] }
    MAX_SPEED = 5
    MAX_LIFE = 5
    def __init__(self, position, level):
		pygame.sprite.Sprite.__init__(self)
		self.position = position
		self.level = level
		self.normal = pygame.image.load(self.images[level][0])
		self.destroyed = False
		if self.images[level][1] == None:
			self.hit = self.normal
		else:
			self.hit = pygame.image.load(self.images[level][1])
	
		self.rect = pygame.Rect(self.normal.get_rect())
		self.rect.center = self.position
		self.image = self.normal
		self.speed = random.randint(0, 4) + 1
		self.direction = random.uniform(0, 360)

		self.life = 0		
		if self.level == 0:
		    self.life = random.randint(1, 3)
		elif self.level == 2:
		    self.life = random.randint(2, self.MAX_LIFE)
    def update(self, hit_list, reset):
		x, y = self.position
		rad = self.direction * math.pi / 180
		
		#out of Screen
		if x < -20:
		    x = 820
		elif x > 820:
		    x = -20

		if y < -20:
		    y = 660
		elif y > 660:
		    y = -20
		
                  #move
		x -= self.speed * math.sin(rad)
		y -= self.speed * math.cos(rad)
		
		self.position = (x, y)
		self.rect.center = self.position
		
                  #detect hit and damage
		if self in hit_list:
			self.image = self.hit
			self.destroyed = True
			self.life -= 1
			if self.speed > 1:
			    self.speed -= 1
			
		if reset:
		    self.reset()
    def reset(self):
        self.image = self.normal
        self.destroyed = False

    def setSpeed(self,speed):
        self.speed = speed
        if(self.speed > self.MAX_SPEED):
            self.speed = self.MAX_SPEED

    def setDirection(self,direction):
        self.direction = direction

#Class representing a fire shot by the spaceship
class FireSprite(pygame.sprite.Sprite):
    img = "./img/fire.png"

    def __init__(self, position, velocity, direction):
        	pygame.sprite.Sprite.__init__(self)
        	self.position = position
        	self.speed = velocity
        	self.direction = direction
        	self.src_image = pygame.image.load(self.img)
        	self.image = pygame.transform.rotate(self.src_image, self.direction)
        	self.rect = self.image.get_rect()
        	self.rect.center = self.position
        	self.outScreen = False
        	
        	
    def update(self):
        x, y = self.position

        #out of screen
        if x < 0 or x > 800:
            self.outScreen = True
        if y < 0 or y > 640:
            self.outScreen = True
        #move
        if not self.outScreen:
            rad = self.direction * math.pi / 180
            x -= self.speed * math.sin(rad)
            y -= self.speed * math.cos(rad)
            self.position = (x, y)

            self.rect.center = self.position
        	
        	

#Class representing the spaceship
class SpaceShipSprite(pygame.sprite.Sprite):
	MAX_UP_SPEED = 4
	MAX_DOWN_SPEED = 4
	ACCELERATION = 0.5
	TURN_SPEED = 2
	FRICTION = 0.01
	MAX_LIFE = 2
	
	image = './img/spaceshipv3.png'
	hit_image = './img/spaceshipv3_hit.png'

	def __init__(self,position):
		pygame.sprite.Sprite.__init__(self)
		self.fire = False
		self.src_image = self.normal = pygame.image.load(self.image)
		self.image = self.normal
		if self.hit_image == None:
			self.hit_image = self.normal
		else:
			self.hit_image = pygame.image.load(self.hit_image)

		x, y = position

		
		self.exploded = pygame.image.load("./img/ship_explosion.png")
		
		self.position = position
		self.speed = self.direction = self.move_direction = 0
		self.k_left = self.k_right = self.k_down = self.k_up = 0
		self.rect = self.image.get_rect()
            	self.speed_change = False
            	self.life = self.MAX_LIFE
            	self.destroyed = False
            	self.imune = 0


	def update(self, deltat, hit, fix):
             #move
	    if not self.destroyed:
		current_speed = self.speed
		self.speed += (self.k_up + self.k_down)
		if self.speed != current_speed:
                    self.speed_change = True

		self.speed -= self.FRICTION * self.speed

		if(self.speed > self.MAX_UP_SPEED):
			self.speed = self.MAX_UP_SPEED
		if (self.speed < -self.MAX_DOWN_SPEED):
			self.speed = -self.MAX_DOWN_SPEED


		self.direction += (self.k_right + self.k_left)


		x, y = self.position
		#out of Screen
		if x < -20:
		    x = 820
		elif x > 820:
		    x = -20

		if y < -20:
		    y = 660
		elif y > 660:
		    y = -20

		#change direction
		if self.speed_change:
		    self.move_direction += self.direction
		    self.move_direction /= 2

		rad = self.move_direction  * math.pi / 180
		x += self.speed * math.sin(rad)
		y += self.speed * math.cos(rad)

		self.position = (x, y)
		
#		print self.move_direction
                  #detect hit and damage
		if hit:
		    if self.imune <= 0:
		        self.imune = 5000
		        self.src_image = self.hit_image
		        self.life -= 1
		        if self.life < 0:
		            self.src_image = self.exploded
		            self.destroyed = True
                  #detect repair
		if fix:
			self.src_image = self.normal
			self.life = self.MAX_LIFE

		self.image = pygame.transform.rotate(self.src_image, self.direction)


		self.rect.center = self.position
		
		self.speed_change = False
		
		self.imune -= deltat

#Information Bar -- Points
class PointsInfoSprite(pygame.sprite.Sprite):

    SIZE = (120, 30)
    BG_COLOR = (200, 0, 0)
    TEXT_COLOR = (255, 255, 255)
    def __init__(self, position, points):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.background = pygame.Surface( self.SIZE )
        self.background.fill ( self.BG_COLOR )
        self.image = self.background
        self.points = points
        self.text = "POINTS " + str( self.points )
        self.font = pygame.font.Font(None, 30)
        self.image.blit( self.font.render(self.text, 1, self.TEXT_COLOR ), (2,2) )
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.dirty = True

    def update(self):
        if self.dirty:
            self.text = "POINTS " + str( self.points )
            self.image.fill (self.BG_COLOR)
            self.image.blit( self.font.render(self.text, 1, self.TEXT_COLOR ), (2, 2) )
            self.dirty = False

    def setPoints(self,points):
        self.dirty = True
        self.points = points

#Information Bar -- Life
class StatusBarSprite(pygame.sprite.Sprite):

    SIZE = (75, 30)
    BG_COLOR = (0, 200, 0)
    TEXT_COLOR = (0, 100, 200)
    def __init__(self, position, lifeText):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.background = pygame.Surface( self.SIZE )
        self.background.fill ( self.BG_COLOR )
        self.image = self.background
        self.lifeText = lifeText
        self.text = "LIFE " + self.lifeText
        self.font = pygame.font.Font(None, 30)
        self.image.blit( self.font.render(self.text, 1, self.TEXT_COLOR ), (2,2) )
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.dirty = True

    def update(self):
        if self.dirty:
            self.text = "LIFE " + self.lifeText
            self.image.fill (self.BG_COLOR)
            self.image.blit( self.font.render(self.text, 1, self.TEXT_COLOR ), (2, 2) )
            self.dirty = False

    def setLifeText(self,text):
        self.dirty = True
        self.lifeText = text

#Creates a list of asteroids with pre-fixed positions
def createAsteroids():
    return  [
	AsteroidSprite( (x + 200, y), 0),
	AsteroidSprite( (x -250, y), 0),
	AsteroidSprite( (x, y + 200), 0),
	AsteroidSprite( (x + 100, y - 278), 0),
	AsteroidSprite( (x + 180, y + 200), 0),
	AsteroidSprite( (x + 260, y - 190), 0),
	AsteroidSprite( (x - 220, y + 150), 0),
            ]



#MAIN LOOP
rect = screen.get_rect()

ship = SpaceShipSprite(rect.center)

ship_group = pygame.sprite.RenderPlain(ship)

x, y = rect.center

asteroids = createAsteroids()

asteroid_group = pygame.sprite.RenderPlain(*asteroids)

pitStop = PitStopSprite((x + 300, y + 200))

pitStop_group = pygame.sprite.RenderPlain(pitStop)

fireShots = []
fireGroup = pygame.sprite.Group(*fireShots)

statusBar = StatusBarSprite((650, 625), str(ship.life) )
statusBarGroup = pygame.sprite.RenderPlain(statusBar)

pointsBar = PointsInfoSprite( (740, 625), str(0) )
pointsBarGroup = pygame.sprite.RenderPlain(pointsBar)

bg = pygame.image.load( './img/sky_bg.png' )
screen.blit( bg, (0, 0) )

points = 0
while 1:
         #Ensure FPS = 30
	deltat = clock.tick(30)
	#check user input
	for event in pygame.event.get():

		if hasattr(event, 'key') :
			down = ( event.type == KEYDOWN)
			if( event.key == K_RIGHT):
				ship.k_right = down * -ship.TURN_SPEED
			elif( event.key == K_LEFT):
				ship.k_left = down * ship.TURN_SPEED
			elif( event.key == K_UP):
				ship.k_up = down * -ship.ACCELERATION
			elif( event.key == K_DOWN):
				ship.k_down = down * ship.ACCELERATION
			elif( event.key == K_SPACE ):
				ship.fire = down and True
			elif( event.key == K_ESCAPE):
				sys.exit(0)
		elif(event.type == QUIT):
			sys.exit(0)

        #check collisions (ship - asteroids)
        shipCollisions  = pygame.sprite.spritecollide(ship_group.sprites()[0], asteroid_group, False)
        ship_hit = False	
        if shipCollisions:
            ship_hit = True
        #check collisions (fire - asteroids)
        collisions = pygame.sprite.groupcollide(fireGroup, asteroid_group, True, False)
        fired = []
        for collided in collisions.values():
            fired.append(collided[0])

        #repair only when asteroids number is zero and spaceship is over support base
        ship_fix = (len( pygame.sprite.spritecollide(ship_group.sprites()[0], pitStop_group, False) ) > 0 )
        asteroids_number = len (asteroid_group.sprites())
        if ship_fix and asteroids_number == 0:
            asteroids = createAsteroids()
            asteroid_group = None
            asteroid_group = pygame.sprite.RenderPlain(*asteroids)

        #Spaceship is firing
        if ship.fire:
            ship.fire = False
            x, y = ship.position
            fire = FireSprite((x, y), 12, ship.direction)
            fireGroup.add(fire)
            fire = None
        #remove fire objects out of screen
        for fire in fireGroup.sprites():
            if fire.outScreen:
                fireGroup.remove(fire)

        #update life and points
        statusBar.setLifeText(str(ship.life) )
        pointsBar.setPoints(str(points) )

        #remove sprites from the background
    	fireGroup.clear(screen, bg)
    	asteroid_group.clear(screen, bg)
	ship_group.clear(screen, bg)
	statusBarGroup.clear(screen, bg)
	pointsBarGroup.clear(screen, bg)


        #update position and other information
	asteroid_group.update(fired, ship_fix)
	ship_group.update(deltat, ship_hit, ship_fix)
	fireGroup.update()
	statusBarGroup.update()
	pointsBarGroup.update()
	
        #destroy asteroids
	for asteroid in asteroid_group.sprites():
	    if asteroid.life < 0:
	        #destroy asteroid and create new ones if possible
	        asteroid_group.remove(asteroid)
	        points += 1
	        print "Points: ", points
	        if asteroid.level == 4:
	            continue
	        #create new ones
	        for i in range(2):
	            new = AsteroidSprite(asteroid.position, asteroid.level + 2)
	            new.setSpeed(random.randint(1, asteroid.speed))
	            new.setDirection(random.uniform(asteroid.direction - 180, asteroid.direction + 180) )
	            asteroid_group.add(new)

        #draw sprites over the background
	asteroid_group.draw(screen)
	pitStop_group.draw(screen)
	ship_group.draw(screen)
	fireGroup.draw(screen)
	statusBarGroup.draw(screen)
	pointsBarGroup.draw(screen)

        #update the screen
	pygame.display.flip()

