import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
print("import successfull")

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

glutInit() #initialize a glut instance to customize the windows
glutInitDisplayMode(GLUT_RGBA) #set the display mode to be colored
glutInitWindowSize(500,500)
glutInitWindowPosition(0,0)
window = glutCreateWindow("test OpenGL")
glutDisplayFunc(showScreen) #Tell OpenGL to call the showScreen method continuously
glutIdleFunc(showScreen) #draw any graphics or shapes in the showScreen function at all time#glutMainLoop() #keep the windows created above displaying/running ina loop


#
"""
import OpenGL.GL as gl

from PySide2.QtWidgets import QApplication, QOpenGLWidget
from PySide2.QtGui import QSurfaceFormat
from PySide2.QtOpenGL import QGL

class OpenGLWindow(QOpenGLWidget):
    def initializeGL(self):
        format = QSurfaceFormat()
        format.setVersion(2, 1)
        format.setProfile(QSurfaceFormat.CoreProfile)
        self.setFormat(format)

        vertex_shader_source = '''
            #version 410

            in vec3 position;

            void main()
            {
                gl_Position = vec4(position, 1.0);
            }
        '''

        fragment_shader_source = '''
            #version 410

            out vec4 out_color;

            void main()
            {
                out_color = vec4(0.0, 1.0, 1.0, 1.0);
            }
        '''

        vertex_shader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        gl.glShaderSource(vertex_shader, vertex_shader_source)
        gl.glCompileShader(vertex_shader)
        success = gl.glGetShaderiv(vertex_shader, gl.GL_COMPILE_STATUS)
        if not success:
            print("shader error on vertex shader : ")
            print(gl.glGetShaderInfoLog(vertex_shader).decode())

        fragment_shader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        gl.glShaderSource(fragment_shader, fragment_shader_source)
        gl.glCompileShader(fragment_shader)
        success = gl.glGetShaderiv(fragment_shader, gl.GL_COMPILE_STATUS)
        if not success:
            print("shader error on fragment shader : ")
            print(gl.glGetShaderInfoLog(fragment_shader).decode())

        self.shader_program = gl.glCreateProgram()
        gl.glAttachShader(self.shader_program, vertex_shader)
        gl.glAttachShader(self.shader_program, fragment_shader)
        gl.glLinkProgram(self.shader_program)
        success = gl.glGetShaderiv(self.shader_program, gl.GL_LINK_STATUS)
        if not success:
            print("shader program link failed : ")
            print(gl.glGetShaderInfoLog(self.shader_program).decode())

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        gl.glUseProgram(self.shader_program)
        # Add your draw calls here
        gl.glUseProgram(0)
"""