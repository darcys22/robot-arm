import pygame
import math
from decimal import *
import sys

pygame.init()
screen = pygame.display.set_mode((700,700))
clock = pygame.time.Clock()


class Robot:
    def __init__(self):
        self.arms = [ [(350,680),(550,681)],[(550,681),(360,681)]]
        self.speed = 1000

        self.moving = False
        self.desiredAngles = [0,0]
        self.target = (0,0)

    def currentLocation(self):
        return self.arms[len(self.arms) -1][1]

    def armLen(self, arm):
        return self.distance((self.arms[arm][1][0] - self.arms[arm][0][0]) ,(self.arms[arm][1][1] - self.arms[arm][0][1]))

    def distance(self,x,y):
        return math.sqrt(x*x + y*y)

    def update(self):
        if self.moving:
            origin = self.arms[0][0]

            x = self.arms[1][1][0] - origin[0]
            y = self.arms[1][1][1] - origin[1]

            print(x)
            print(y)

            dist = self.distance(x,y)
            print(dist)

            d1 = math.atan2(y,x)

            d2 = self.lawOfCosines(dist, self.armLen(0), self.armLen(1))

            a1 = d1 + d2

            # print(self.armLen(1))
            # print(self.armLen(0), self.armLen(1),dist)

            a2 = self.lawOfCosines(self.armLen(0), self.armLen(1), dist)

            if self.desiredAngles[0] - math.degrees(a1) > 1:
                self.rotateArm(0,1)
            if self.desiredAngles[0] - math.degrees(a1) < 1:
                self.rotateArm(0,-1)
            if self.desiredAngles[1] - math.degrees(a2) > 1:
                self.rotateArm(1,1)
            if self.desiredAngles[1] - math.degrees(a2) < 1:
                self.rotateArm(1,-1)

            if self.distance(self.target[0] - origin[0], self.target[1] - origin[1]) < 5:
                self.moving = False

        return 0

    def lawOfCosines(self, a,b,c):
        # Law of Cosines c^2 = a^2 + b^2 - 2ab cos C
        # C = arccos( (a^2+b^2-c^2)/2ab )
        a = round(a,4)
        b = round(c,4)
        c = round(c,4)
        return math.acos((a*a + b*b - c*c) / (2 * a * b))

    return def revKine(self, location):
        # robot.revKine((200, 600))
        # (350,600)
        self.target = location
        origin = self.arms[0][0]

        x = location[0] - origin[0]
        y = location[1] - origin[1]

        # x = 150
        # y = 0

        dist = self.distance(x,y)

        d1 = math.atan2(y,x)

        d2 = self.lawOfCosines(dist, self.armLen(0), self.armLen(1))

        a1 = d1 + d2

        a2 = self.lawOfCosines(self.armLen(0), self.armLen(1), dist)

        self.desiredAngles = [a1,a2]
        self.moving = True
        self.update()



    def rotateArm(self,arm, degrees):
        points = self.arms[arm]

        s = math.sin(math.radians(degrees))
        c = math.cos(math.radians(degrees))
        origin = points[0]
        extension = points[1]

        newpoints = []

        for point in points:
            x = point[0] - origin[0]
            y = point[1] - origin[1]
            xnew = x * c - y * s
            ynew = x * s + y * c
            newpoints.append( (xnew + origin[0], ynew + origin[1]) )

        self.arms[arm] = newpoints
        if (len(self.arms) > arm+1):
            movement = (newpoints[1][0] - extension[0] , newpoints[1][1] - extension[1] )
            self.moveArm(arm+1,movement)

    def moveArm(self,arm, movement):
        points = self.arms[arm]

        origin = points[0]
        extension = points[1]

        newpoints = []

        for point in points:
            x = point[0] + movement[0]
            y = point[1] + movement[1]
            newpoints.append( (x, y) )

        self.arms[arm] = newpoints
        if (len(self.arms) > arm+1):
            movement = (newpoints[1][0] - extension[0] , newpoints[1][1] - extension[1] )
            self.moveArm(arm+1,movement)

    def up(self):
        self.rotateArm(0,-1)
        return 0
    def down(self):
        self.rotateArm(0,1)
        return 0
    def left(self):
        self.rotateArm(1,-1)
        return 0
    def right(self):
        self.rotateArm(1,1)
        return 0



def draw_arm(arm):
    color = (0, 128, 255)
    pygame.draw.lines(screen, color, False, arm, 4)


def draw():
    done = False

    robot = Robot()
    # if (len(sys.argv) > 2):
        # robot.revKine((sys.argv[1], sys.argv[2]))
    robot.revKine((200, 600))
    args = sys.argv[1:]

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        #Key Pressed
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_j]:
            robot.down()
        if pressed[pygame.K_k]:
            robot.up()
        if pressed[pygame.K_l]:
            robot.right()
        if pressed[pygame.K_h]:
            robot.left()


        # Putting Stuff on screen
        screen.fill((0,0,0))

        color = (0,128,255)
        myfont = pygame.font.SysFont("monospace", 15)
        target = myfont.render("Target: ({},{})".format(robot.target[0], robot.target[1]),1,color)
        screen.blit(target, (520, 10))
        current = myfont.render("current: ({0:.1f},{0:.1f})".format(robot.arms[1][1][0], robot.arms[1][1][1]),1,color)
        screen.blit(current, (520, 35))

        robot.update()

        for a in robot.arms:
            draw_arm(a)

        pygame.display.flip()
        clock.tick(20)

draw()

