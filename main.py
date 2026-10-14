import pygame
import asyncio
import random
import math
async def main():
    pygame.init()
    WIDTH = 600
    HEIGHT = 400
    Screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Asteroid destroyer")
    clock = pygame.time.Clock()
    Aster = []
    MissleSpeed = 7
    angle = 90
    thrust = .15
    MaxSpeed = 30
    
    
    ##### Asteroid ######
    class Asteroid:
        def __init__ (self,center, VectM, r , color):
            self.center = center
            self.VectM = VectM 
            self.r = r
            self.color = color
        def move(self):
            self.center += self.VectM
    
            if self.center.x + self.r > WIDTH or self.center.x - self.r < 0:
                self.VectM.x = -self.VectM.x
                
            if self.center.y + self.r > HEIGHT or self.center.y - self.r < 0:
                self.VectM.y = -self.VectM.y
        def draw(self, screen):
            pygame.draw.circle(screen, self.color, self.center, self.r )
        def collision(self, other):
            distance = self.center.distance_to(other.center)
            if distance < self.r + other.r:
                 normal = (other.center - self.center).normalize()
                 mass1 = self.r ** 2
                 mass2 = other.r ** 2 
                 v1 = self.VectM.dot(normal)
                 v2 = other.VectM.dot(normal)
                 new_v1 = (v1 * (mass1 - mass2) + 2 * mass2 * v2) / (mass1 + mass2)
                 new_v2 = (v2 * (mass2 - mass1) + 2 * mass1 * v1) / (mass1 + mass2)
        
                 self.VectM += (new_v1 - v1) * normal
                 other.VectM += (new_v2 - v2) * normal
    ###############################################################
    class ShipVessel:
        def __init__(self, positions):
            self.postion = pygame.Vector2(positions)
        def getPos(self):
            return self.postion
        def drawShip(self, postion, color, angles):
            x = int(self.postion.x)
            y = int(self.postion.y)
            points = [pygame.Vector2(0, -22),pygame.Vector2( -17, 18),pygame.Vector2(0,  10),pygame.Vector2(17, 18)]
            rotated_points = []
    
            for point in points:
                rotated = point.rotate(-(angles - 90))
                rotated_points.append((x + rotated.x, y + rotated.y))
    
            pygame.draw.polygon(Screen, color, rotated_points, 2 )
        def update(self, postion, speed, Max):
            postion += speed
            if speed.length() > Max:
             speed.scale_to_length(Max)
            if postion.x > WIDTH:
                postion.x = 0
            
            if postion.x < 0:
                postion.x = WIDTH
            
            if postion.y > HEIGHT:
                postion.y = 0
            
            if postion.y < 0:
                postion.y = HEIGHT
        def updateE(self, postion, speed, Max, want):
            direction = want - postion
    
            if direction.length() != 0:
                direction = direction.normalize()
    
            speed = direction * Max
            postion += speed
    
    
        
            
        
    ##### Missle #####
    class Missle:
        def __init__(self, start_position, target_position):
            self.start_position = pygame.Vector2(start_position)
            self.target_position = pygame.Vector2(target_position) # making it Vector
            self.position = pygame.Vector2(start_position)
            self.radius = 5
            distance = self.target_position - self.start_position
            if distance.length() != 0:
                distance = distance.normalize()
            self.velocityM = distance * MissleSpeed
        def move(self):
            self.position += self.velocityM
        def draw(self):
            pygame.draw.circle(Screen, (93, 201, 50),(int(self.position.x), int(self.position.y)), self.radius)
        def is_off_screen(self):
            return (
                self.position.x < 0 or self.position.x > WIDTH or self.position.y < 0 or self.position.y > HEIGHT)
        def missile_hits_asteroid(missile, asteroid):
         
         distance = missile.position.distance_to(asteroid.center)
         return distance < missile.radius + asteroid.r
         
    
        
    
    ##################################################################################################################
    
    Ethrust = .01
    Ship_speed = 12
    enemySpeed = pygame.Vector2(0,0)
    rotation = 3
    enemy = ShipVessel(pygame.Vector2(50, 200))
    ENangle = 90
    ERADS = math.radians(ENangle)
    Eforward = pygame.Vector2(math.cos(ERADS),-math.sin(ERADS))
    ship = ShipVessel(pygame.Vector2( WIDTH/ 2, HEIGHT/ 2))
    ET = pygame.math.Vector2(0,0)
    missiles = []
    enemyAccel = Eforward * Ethrust
    score = 0
    
    while len(Aster) != 6:
        Vect = pygame.math.Vector2(random.randint(10, 530), random.randint(10, 350))
        VectMOVE = pygame.math.Vector2(random.randint(1, 6), random.randint(1, 6))
        Size = random.randint(10,20)
        TempAs = Asteroid(Vect,VectMOVE, Size, (125, 116, 115))
        Aster.append(TempAs)
    velocity = pygame.Vector2(0,0)
    acceleration = pygame.Vector2(0,0)
    enemyAccel = pygame.Vector2(0,0)
    drag = 0.9
    Running = True
    while Running:
         Screen.fill((0,0,0))
         font = pygame.font.SysFont(None, 30)
         score_text = font.render(f"Score: {score}", True, (255, 255, 255))
         Screen.blit(score_text, (10, 10))
         keys = pygame.key.get_pressed()
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                target_position = pygame.Vector2(event.pos)
                new_missile = Missle(ship.getPos(),target_position)
                missiles.append(new_missile)
            
         FromPlayer = ship.getPos() - enemy.getPos()
         FromPlayer = FromPlayer.normalize()
         dot = Eforward.dot(FromPlayer)
         distance = enemy.getPos().distance_to(ship.getPos())
         ET = -FromPlayer.angle_to(pygame.Vector2(1, 0))
         Patrol = True
         attack = False
         if dot > .6 and distance < 200:
            attack = True
            Patrol = False
         if Patrol:
            ENangle += 1.5
            ERADS = math.radians(ENangle)
            Eforward = pygame.Vector2(math.cos(ERADS),-math.sin(ERADS))
         if attack:
            ENangle = ET
            ERADS = math.radians(ENangle)
            Eforward = pygame.Vector2(math.cos(ERADS),-math.sin(ERADS))
            enemySpeed += enemyAccel
            enemy.updateE(enemy.getPos(),enemySpeed, 2, ship.getPos())
    
    
            
     
         if keys[pygame.K_LEFT]:
            angle += rotation
         if keys[pygame.K_RIGHT]:
             angle -= rotation
         radians = math.radians(angle)
         forward = pygame.Vector2(math.cos(radians),-math.sin(radians))
    
         if keys[pygame.K_UP]:
            acceleration = forward * thrust
         velocity += acceleration
         ship.update(ship.getPos(), velocity, MaxSpeed)
         velocity = velocity * drag
        
         enemy.drawShip(enemy.getPos(), (214, 59, 28), ENangle )
         ship.drawShip(ship.getPos(), (3, 252, 82), angle)
         for missile in missiles:
            missile.draw()
            missile.move()
            for aasteroid in Aster:
                if Missle.missile_hits_asteroid(missile, aasteroid):
                    Aster.remove(aasteroid)
                    missiles.remove(missile)
                    score += 10
                    Vect = pygame.Vector2(random.randint(10, WIDTH - 10),random.randint(10, HEIGHT - 10))
                    VectMOVE = pygame.Vector2(random.randint(1, 6),random.randint(1, 6))
                    Size = random.randint(10, 20)
                    Aster.append(Asteroid(Vect, VectMOVE, Size, (125, 116, 115)))
                    break
    
    
    
    
                
         pygame.display.flip()
    
    
         for aasteroid in Aster:
            aasteroid.move()
            aasteroid.draw(Screen)
         for i in range(len(Aster)):
            for j in range(i + 1, len(Aster)):
                Aster[i].collision(Aster[j])
         acceleration = pygame.Vector2(0,0)
         pygame.display.flip()
         clock.tick(30)
         await asyncio.sleep(0)
asyncio.run(main())
