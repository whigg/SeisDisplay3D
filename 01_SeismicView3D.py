'''
   Despliegue de seccion sisimica en 3D usando OpenGL
   Por AJ Ovalles Feb 2016
'''
'''
https://pythonprogramming.net/adding-ground-pyopengl-tutorial/?completed=/multiple-opengl-cubes/
'''
from matplotlib import cm
import read_segy
import numpy as np
import random
import pdb
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

ns=100  # numero de muestras a desplegar
nt=50  # numero de trazas a desplegar

'''
   Se lee el archivo SEGY y se carga en la matriz Section
'''
Section = read_segy.read_segy('PP554_t506s751.sgy')
Section = Section.T

'''
   Se define la funcion que convierte los valores de amplitud
   en colores RGB
'''

def amp2rgb(Amp, minAmp,maxAmp):
    if Amp >= maxAmp:
        cindex = float(255)
    elif Amp <= minAmp:
        cindex = float(0)
    else:
        cindex = float(((255.0/(maxAmp-minAmp))*(Amp-minAmp)))

    vrgb=cm.seismic(int(cindex))
    return vrgb
#pdb.set_trace()
'''
   Primero se crean los vertices  y se asocia a cada
   vertice un color, cada nodo i,j es un par muestra,traza. 
   Luego se le indica a openGL
   la primitiva glBegin(GL_QUADS) que le dice que cuatro
   verticies consecutivos forman un cuadrado
   (esto es hacer los vertex)
   https://www3.ntu.edu.sg/home/ehchua/programming/opengl/CG_Introduction.html
'''


verticies = []
color = []
for j in range(nt):
    for i in range(ns):
        verticies.append((j,-1*i,-1))
        verticies.append((j,-1*(i+1),-1))
        verticies.append((j+1,-1*(i+1),-1))
        verticies.append((j+1,-1*i,-1))

        color.append(amp2rgb(Section[i][j],-10,10))
        color.append(amp2rgb(Section[i+1][j],-10,10))
        color.append(amp2rgb(Section[i+1][j+1],-10,10))
        color.append(amp2rgb(Section[i][j+1],-10,10))

verticies = tuple(verticies)
verticies = np.array(verticies)*(2.0/nt)
verticies = tuple(verticies)
#pdb.set_trace()
color = tuple(color)
#pdb.set_trace()
'''
   La funcion cube convierte los verticies en vertex
   y le asigna el color a cada vertex. Llamada render function
'''

def Cube():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    glBegin(GL_QUADS)    
    for vertex in range(len(verticies)):
        glColor3f(color[vertex][0],color[vertex][1],color[vertex][2])
        glVertex3fv(verticies[vertex]) 
        '''
           Para 3D use glVertex3fv, agregue z a verticies
           Ejm: verticies.append((j,-1*i,Z))
        '''    
    glEnd()

    glutSwapBuffers()
    return

def main():
    
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(600,400)
    glutCreateWindow("Seismic")

    gluPerspective(45, (600/400), 0, 15) #3D effect
    glTranslatef(-1,1,-4)  # Ocurre el pocicionamiento
    glRotatef(55, 0, 1, 0) #vector de rotacion  (degrees,(eje-vector))

    glutDisplayFunc(Cube) #Aqui se llama a la render function
    glutMainLoop()
    return

if __name__ == '__main__': main()
