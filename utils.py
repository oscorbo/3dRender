from math import sqrt
import random

pi = 3.14

class temp():
    def __init__(self, vec):
        self.position = vec
        pass

class vector():
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z
        self.matrix = [x, y, z]

    def add(self, vector):
        self.x += vector.x
        self.y += vector.y
        self.z += vector.z

    def sub(self, vector):
        self.x -= vector.x
        self.y -= vector.y
        self.z -= vector.z

    def multiply(self, mult):
        self.x *= mult
        self.y *= mult
        self.z *= mult

    def divide(self, div):
        if div == 0:
            return
        self.x /= div
        self.y /= div
        self.z /= div

    def get_length(self):
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
    
    def setMagnitude(self, mag):
        self.normalize()
        self.multiply(mag)

    def normalize(self):
        vector_leng = sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
        if vector_leng == 0:
            self.x = 0
            self.y = 0
            self.z = 0
            return
        self.x = self.x/vector_leng
        self.y = self.y/vector_leng
        self.z = self.z/vector_leng

    def distance(self, vector):
        temp1 = (self.x - vector.x)
        temp2 = (self.y - vector.y)
        temp3 = (self.z - vector.z)
        try:
            return sqrt(temp1 + temp2 + temp3)
        except:
            return sqrt(-1 * (temp1 + temp2 + temp3))
    
    def setRandom(self, power):
        self.x = random.randrange(-power, power)
        self.y =  random.randrange(-power, power)
        self.z =  random.randrange(-power, power)

    def limit(self, limited):
        if self.get_length() > limited:
            self.normalize()
            self.multiply(limited)

    def dot_product(self, vec):
        return self.x * vec.x + self.y * vec.y + self.z * vec.z

    def clone(self):
        return vector(self.x, self.y, self.z)
    
    def printVector(self):
        print(f"x: {self.x} / y: {self.y} / z: {self.z}")
