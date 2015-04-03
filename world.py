from vector2d import Vector2D

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
            return dp.magsqr() < (self.radius + other.radius) ** 2

class AABBTree(object):
    def __init__(self):
        self.objects = {}
        self.staticObjects = {}
        self.initCount = 0

    def copy(self):
        copied = AABBTree()
        copied.objects = self.objects.copy()
        copied.staticObjects = self.staticObjects.copy()
        copied.initCount = self.initCount
        return copied

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

    def getStaticCollisions(self):
        collisions = []
        for k,obj in self.objects.iteritems():
            for _,staticOther in self.staticObjects.iteritems():
                if obj.collide(staticOther):
                    collisions.append([obj, staticOther])
        return collisions

class World(object):
    def __init__(self):
        self.bodies = AABBTree()
        self.gravity = Vector2D(0,1)

    def addBody(self, body):
        return self.bodies.addObject(body)

    def getBody(self, tag):
        return self.bodies.getBody(tag=tag)

    def update(self, dt):
        evolved = self.bodies.copy()
        evolved.evolve(dt, self.gravity)

        collisions = evolved.getStaticCollisions()
        for a, b in collisions:
            normal = (b.position - a.position).norm()
            colPlane = Vector2D(-normal.y, normal.x)
            nVer = a.velocity.dot(normal)
            nCol = a.velocity.dot(colPlane)
            a.velocity = colPlane * nCol - normal * nVer
        self.bodies = evolved
