from vector2d import Vector2D
import copy

class Body(object):
    def __init__(self, bodyType, position):
        self.position = Vector2D(position)
        self.velocity = Vector2D(0,0)
        self.acceleration = Vector2D(0,0)
        self.force = Vector2D(0,0)
        self.bodyType = bodyType

    def evolve(self, dt):
        self.acceleration += self.force * dt
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt

    def applyLinearForce(self, force):
        self.force += force

class Sphere(Body):
    def __init__(self, bodyType, position, radius):
        self.radius = radius
        super(Sphere, self).__init__(bodyType, position)

    def getRadius(self):
        return self.radius

    def getPosition(self):
        return self.position

    def collide(self, other):
        if other.__class__ == Sphere:
            dp = other.position - self.position
            contactTime = dp.magsqr() / (self.radius + other.radius) ** 2
            return contactTime

class AABBTree(object):
    def __init__(self):
        self.objects = {}
        self.staticObjects = {}
        self.initCount = 0
    def addObject(self, obj):
        self.initCount += 1
        if obj.bodyType == 'static':
            self.staticObjects[self.initCount] = obj
        else:
            self.objects[self.initCount] = obj
        return self.initCount

    def getBody(self, tag):
        if tag in self.objects:
            return self.objects[tag]
        else:
            return self.staticObjects[tag]

    def evolve(self, dt, gravity = Vector2D(0,0)):
        for k,obj in self.objects.iteritems():
            obj.applyLinearForce(gravity)
            obj.evolve(dt)
            obj.acceleration = Vector2D(0,0)

    def getStaticCollisions(self):
        collisions = []
        for tagA,obj in self.objects.iteritems():
            for tagB,staticOther in self.staticObjects.iteritems():
                contactTime = obj.collide(staticOther)
                if contactTime <= 1:
                    collisions.append([tagA, tagB, contactTime])
        return collisions

class World(object):
    def __init__(self):
        self.bodies = AABBTree()
        self.gravity = Vector2D(0,10)

    def addBody(self, body):
        return self.bodies.addObject(body)

    def getBody(self, tag):
        return self.bodies.getBody(tag=tag)

    def update(self, dt):
        evolved = copy.deepcopy(self.bodies)
        evolved.evolve(dt, self.gravity)

        collisions = evolved.getStaticCollisions()
        for tagA, tagB, contactTime in collisions:
            prevA = self.bodies.getBody(tagA)
            prevB = self.bodies.getBody(tagB)
            a = evolved.getBody(tagA)
            b = evolved.getBody(tagB)
            normal = (b.position - a.position).norm()
            colPlane = Vector2D(-normal.y, normal.x)
            nVer = a.velocity.dot(normal)
            nCol = a.velocity.dot(colPlane)
            postVelocity = colPlane * nCol - normal * nVer
            dv = (a.velocity * contactTime + postVelocity * (1 - contactTime)) * dt
            a.position = prevA.position + dv
            a.velocity = postVelocity

        self.bodies = evolved
