import sys, pygame
from world import Sphere, World
from vector2d import Vector2D
import cProfile, pstats, StringIO
import random
pygame.init()

size = width, height = 800,600
black = 0, 0, 0
white = 255, 255, 255
clock = pygame.time.Clock()

world = World()

class KSphere(object):
    def __init__(self, *arg, **argv):
        body = Sphere(*arg, **argv)
        self.bodyTag = world.addBody(body)

    def render(self):
        body = world.getBody(tag=self.bodyTag)
        x,y = body.getPosition()
        pygame.draw.circle(screen, white, [int(x),int(y)], body.getRadius(), 1)

screen = pygame.display.set_mode(size)

circles = []
for x in xrange(10):
    circles.append(KSphere(bodyType='dynamic', radius=random.randrange(20,50), position=Vector2D(random.randrange(800),random.randrange(300))))

for x in xrange(10):
    circles.append(KSphere(bodyType='static', radius=random.randrange(20,50), position=Vector2D(random.randrange(800),random.randrange(400,600))))

pr = cProfile.Profile()
pr.enable()

def exitSim():
    pr.disable()
    s = StringIO.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print s.getvalue()
    sys.exit()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exitSim()
    ms = clock.tick(60) / 1000.0
    world.update(ms)
    print 'dt:' + str(ms)
    screen.fill(black)
    for circle in circles:
        circle.render()
    pygame.display.flip()