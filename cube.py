
from utilsmath import *
from utils import *
import data

# refact core

class cube():
    size = 500
    # pi radians | make this private
    # fix angle im tirred of tht sht
    angle = 0
    angle_x = 0
    angle_y = 0
    angle_z = 0

    def __init__(self, batch) -> None:
        self.batch = batch
        self.vertexs = [
            # 0 1
            vertex(vector(1, 1, 1), self),
            vertex(vector(-1, 1, 1), self),
            # 2 3
            vertex(vector(-1, -1, 1), self),
            vertex(vector(1, -1, 1), self),
            # 4 5
            vertex(vector(1, 1, -1), self),
            vertex(vector(-1, 1, -1), self),
            # 6 7
            vertex(vector(-1, -1, -1), self),
            vertex(vector(1, -1, -1), self),
        ]

        self.connection = [ ]
        self.faces = [ ]

        for i in range(4):
            self.connection.append(connectEdges(self.vertexs, i, (i+1) % 4, batch))
            self.connection.append(connectEdges(self.vertexs, i + 4, ((i+1) % 4) + 4, batch))
            self.connection.append(connectEdges(self.vertexs, i, i+4, batch))

        tempface = face(
            self.vertexs[0], self.vertexs[1], 
            self.vertexs[3], self.vertexs[2], 
            batch)
        self.faces.append(tempface)
        tempface = face(
            self.vertexs[2], self.vertexs[3], 
            self.vertexs[6], self.vertexs[7], 
            batch)
        self.faces.append(tempface)
        tempface = face(
            self.vertexs[0], self.vertexs[3], 
            self.vertexs[4], self.vertexs[7], 
            batch)
        self.faces.append(tempface)


        tempface = face(
            self.vertexs[4], self.vertexs[5], 
            self.vertexs[6], self.vertexs[7], 
            batch)
        self.faces.append(tempface)
        tempface = face(
            self.vertexs[0], self.vertexs[1], 
            self.vertexs[4], self.vertexs[5], 
            batch)
        self.faces.append(tempface)
        tempface = face(
            self.vertexs[1], self.vertexs[2], 
            self.vertexs[5], self.vertexs[6], 
            batch)
        self.faces.append(tempface)


    def update(self):
        self.angle = .01

        for vertex_ in self.vertexs:
            rotated = vector(
                vertex_.position_no_perspective.x, 
                vertex_.position_no_perspective.y, 
                vertex_.position_no_perspective.z
                )

            rotated = matrix_multiply2d(rotate_y(self.angle + .03), rotated.matrix)
            rotated = matrix_multiply2d(rotate_x(self.angle), rotated.matrix)
            rotated = matrix_multiply2d(rotate_z(self.angle), rotated.matrix)
            
            distance = 5
            perspective_value = 1 / (distance - (rotated.z / self.size))
            projection_orthogonal = [
                [perspective_value, 0, 0],
                [0, perspective_value, 0], 
                [0, 0, perspective_value] 
            ] 

            projected2D = matrix_multiply2d(projection_orthogonal, rotated.matrix)
            vertex_.update_tiny(projected2D)
            # debug : vertex_.position = rotated
            vertex_.position = projected2D
            vertex_.position_no_perspective = rotated

        for edge_ in self.connection:
            edge_.update_edge()

        for faces_ in self.faces:
            faces_.update()


class sphere():
    size = 200
    # pi radians | make this private
    angle = 0
    angle_x = 0
    angle_y = 0
    angle_z = 0
    def __init__(self, batch) -> None:
        self.batch = batch

        self.vertexs = [ ]
        self.connection = [ ]
        self.faces = [ ]
        
        i = 0
        while i < pi:
            i += pi / 8
            radius = sin(i)
            y = cos(i)

            j = 0
            while j < 2 * pi:
                j += pi / (5 * radius)
                x = cos(j) * radius
                z = sin(j) * radius
                actual_index = len(self.vertexs)
                self.vertexs.append(vertex(vector(x, y, z), self))
                self.connection.append(edge(self.vertexs[actual_index], self.vertexs[actual_index - 1], batch))

        for i in range(0, len(self.vertexs), 1):
            self.faces.append(connectFaces(self.vertexs, i, i-1, i-2, i-3, batch))


    def update(self):
        self.angle = .03

        for vertex_ in self.vertexs:
            rotated = vector(vertex_.position.x, vertex_.position.y, vertex_.position.z)

            rotated = matrix_multiply2d(rotate_y(self.angle + .03), rotated.matrix)
            rotated = matrix_multiply2d(rotate_x(self.angle), rotated.matrix)
            rotated = matrix_multiply2d(rotate_z(self.angle), rotated.matrix)
            
            distance = 2
            perspective_value = 1 / (distance - (rotated.z / self.size))
            projection_orthogonal = [
                [perspective_value, 0, 0],
                [0, perspective_value, 0], 
                [0, 0, perspective_value] 
            ] 
            
            projected2D = matrix_multiply2d(projection_orthogonal, rotated.matrix)
            vertex_.update_tiny(projected2D)
            vertex_.position = rotated


        for edge_ in self.connection:
            edge_.update_edge()
        
        for face in self.faces:
            face.update()