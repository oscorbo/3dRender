from math import cos, sin
from utils import *
from pyglet import shapes
import data

projection_direction = vector(0, 0, 1)
# projection_direction.normalize()

projection_orthogonal_general = [
    [1, 0, 0],
    [0, 1, 0], 
    [0, 0, 1]
] 

def rotate_z(angle):
    rot = [
        [cos(angle), -sin(angle), 0], 
        [sin(angle), cos(angle), 0], 
        [0, 0, 1]
    ]
    return rot

def rotate_x(angle):
    rot = [
        [1, 0, 0],
        [0, cos(angle), -sin(angle)], 
        [0, sin(angle), cos(angle)]
    ]
    return rot

def rotate_y(angle):
    rot = [
        [cos(angle), 0, sin(angle)], 
        [0, 1, 0],
        [-sin(angle), 0, cos(angle)]
    ]
    return rot


#  should be 2 row 3 column, 1 row 3 column | i guess
def matrix_multiply2d(table, coords):
    x = table[0][0] * coords[0] + table[0][1] * coords[1] + table[0][2] * coords[2]
    y = table[1][0] * coords[0] + table[1][1] * coords[1] + table[1][2] * coords[2]
    z = table[2][0] * coords[0] + table[2][1] * coords[1] + table[2][2] * coords[2]
    return vector(x, y, z)

class vertex():
    def __init__(self, position: vector, shape) -> None:
        self.ishide = False
        self.position_no_perspective = vector(position.x * shape.size, position.y * shape.size, position.z * shape.size, )
        self.position = vector(position.x * shape.size, position.y * shape.size, position.z * shape.size, )

        self.shape = shape
        self.circle = shapes.Circle(
            x=position.x + data.center_x, 
            y=position.y + data.center_y,
            radius=2, color=(255,255,255), batch=shape.batch)
    def update_tiny(self, vect):
        self.circle.x = (vect.x) + data.center_x
        self.circle.y = (vect.y) + data.center_y

class edge():
    def __init__(self, vertex1i: vertex, vertex2i: vertex, batch) -> None:
        self.vertex1 = vertex1i
        self.vertex2 = vertex2i
        self.att = shapes.Line(0, 0, 0, 0, width=2, batch=batch)

    def update_edge(self):
        self.att.x = self.vertex1.circle.x
        self.att.y = self.vertex1.circle.y
        self.att.x2 = self.vertex2.circle.x
        self.att.y2 = self.vertex2.circle.y

class face():

    amount_subdiv = 1
    width_face = 10
    def __init__(self, p1: vertex, p2: vertex, p3: vertex, p4: vertex, batch) -> None:
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.vertex_faces = [p1, p2, p3, p4]
        self.middle_point = vector(
            (p1.position.x + p2.position.x + p3.position.x + p4.position.x) / 4, 
            (p1.position.y + p2.position.y + p3.position.y + p4.position.y) / 4, 
            (p1.position.z + p2.position.z + p3.position.z + p4.position.z) / 4, )
        self.normal = self.middle_point.clone()
        # :D
        self.normal.multiply(-1)
        self.normal.normalize()

        self.angle = 0

        self.center_face = shapes.Circle(
            x=self.middle_point.x + data.center_x, 
            y=self.middle_point.y + data.center_y, 
            radius=5, color=(100,255,100), batch=batch)
        
        self.lit_face = [ ]
        for i in range(4):
            self.lit_face.append(shapes.Line(
                x=0, y=0, x2=0, y2=0,
                color=(255,255,255), 
                width=self.width_face,
                batch=batch))

        self.rectagle_face = shapes.Rectangle(
            x=self.middle_point.x + data.center_x, 
            y=self.middle_point.y + data.center_y, 
            height=100, width=100, color=(100,255,100), batch=batch)
        
        self.normal_line = shapes.Line(
            x=self.center_face.x, x2=0,
            y=self.center_face.y, y2=0,
            #width=2, 
            color=(100,255,100), batch=batch)
        # self.normal.sub(vector(data.center_x, data.center_y, self.middle_point.z))

    def update(self):
        self.middle_point = middle_point_and_divide([self.p1,self.p2,self.p3, self.p4], 4)
        self.middle_point.add(vector(data.center_x, data.center_y, 0))
        
        self.normal = vector(
            self.middle_point.x - data.center_x, 
            self.middle_point.y - data.center_y,
            self.middle_point.z)
        self.normal.normalize()

        dot_product = self.normal.dot_product(projection_direction) * 8

        for i in range(len(self.lit_face)):
            line = self.lit_face[i]
            near_vertex1 = self.vertex_faces[i]
            near_vertex2 = self.vertex_faces[i - 1]
            
            middle_of_middle = middle_point_and_divide([temp(self.middle_point), near_vertex1], 2)
            middle_of_middle.add(vector(data.center_x / 2, data.center_y / 2, 0))
            other_middle_of_middle = middle_point_and_divide([temp(self.middle_point), near_vertex2], 2)
            other_middle_of_middle.add(vector(data.center_x / 2, data.center_y / 2, 0))

            line.x = middle_of_middle.x
            line.y = middle_of_middle.y
            line.x2 = other_middle_of_middle.x
            line.y2 = other_middle_of_middle.y

            if dot_product < 0: 
                line.opacity = 0
                continue
            line.opacity = data.ligth_values[int(dot_product)]

        self.center_face.x = self.middle_point.x
        self.center_face.y = self.middle_point.y
        self.rectagle_face.x = self.middle_point.x
        self.rectagle_face.y = self.middle_point.y

        self.normal_line.x = self.center_face.x
        self.normal_line.y = self.center_face.y
        self.normal_line.x2 = self.center_face.x + (self.normal.x * 50)
        self.normal_line.y2 = self.center_face.y + (self.normal.y * 50)

        print(dot_product)
        if dot_product < 0: 
            self.rectagle_face.opacity = 0
            return
        self.rectagle_face.opacity = data.ligth_values[int(dot_product)]
        # :D
        

def middle_point_and_divide(vertexs, divide):
    x = 0
    for vertex_ in vertexs:
        x += vertex_.position.x
    y = 0
    for vertex_ in vertexs:
        y += vertex_.position.y
    z = 0
    for vertex_ in vertexs:
        z += vertex_.position.z
    return vector(x / divide, y / divide, z / divide)

def connectEdges(vertexs, vertex1, vertex2, batch):
    return edge(vertexs[vertex1], vertexs[vertex2], batch)

def connectFaces(vertexs, vertex1, vertex2, vertex3, vertex4, batch):
    return face(vertexs[vertex1], vertexs[vertex2], vertexs[vertex3], vertexs[vertex4], batch)
