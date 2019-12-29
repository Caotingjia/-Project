from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import matplotlib.image as PngImage
import numpy as np
import math



def Bottle_Function(x):
    m = 0.25
    n = 0.5
    c = 5/4*math.pi
    return m * math.sin(x+c) + n


class Bottle:
    def __init__(self):
        self.texture = glGenTextures(1)

        # 初始化光线
        parray = [-1.5, -2, 0.5, 1.0]
        sarray = [1.0, 1.0, 1.0, 0.7]
        glLightfv(GL_LIGHT0, GL_POSITION, parray)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, sarray)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        # 设置texture
        img = PngImage.imread('TexturesCom_WindowsBacklit0016_M.jpg')
        img = np.asarray(img * 255, dtype=np.uint8)
        color = GL_RGBA
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP | GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP | GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, color, img.shape[0], img.shape[1], 0, color, GL_UNSIGNED_BYTE, img)
        glEnable(GL_TEXTURE_2D)

        # 初始化setting
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_POLYGON_SMOOTH)


    def Circle(self, z, r, tex=True):
        if not tex:
            glDisable(GL_TEXTURE_2D)
        glBegin(GL_POLYGON)
        glNormal3f(0.0, 0.0, 1.0)
        for a in range(0, 360,2):
            theta = a * math.pi / 180
            x = math.sin(theta)
            y = math.cos(theta)
            if tex:
                glTexCoord2fv([x, y])
            glVertex3fv([x * r, y * r, z])
        glEnd()

        if not tex:
            glEnable(GL_TEXTURE_2D)

    # 自变量 R, 因变量 圆的半径 在每一个位置R, 画出不同半径的圆
    def Draw_Process(self):
        delta = 1 / 512
        R = 0.9
        z = -R
        while z <= -R + 4 * delta:
            l = (z + R) / R * math.pi
            r = Bottle_Function(l)/2
            self.Circle(z=z, r=r, tex=False)
            z += delta
        while z <= -R/4:
            r = Bottle_Function(0)/2
            self.Circle(z=z, r=r)
            z += delta
        while z <= 0:
            l = (-z*2 + R/2) / R * math.pi - 5/4*math.pi
            r = Bottle_Function(l)/2 - Bottle_Function(3/4*math.pi)/2 + Bottle_Function(0)/2
            self.Circle(z=z, r=r)
            z += delta
        while z <= R:
            self.Circle(z=z, r=r)
            z += delta

    def start(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glMatrixMode(GL_MODELVIEW)
        glRotatef(125.0, 1.0, 0.0, 0.0)
        self.Draw_Process()
        glPopMatrix()
        glFlush()

if __name__ == "__main__":
    glutInit()
    glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE | GLUT_DEPTH)
    glutInitWindowSize(768, 768)
    glutCreateWindow('MyBottle')
    MyBottle = Bottle()
    glutDisplayFunc(MyBottle.start)
    glutMainLoop()