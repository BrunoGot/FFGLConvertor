
"""
Code from http://www.labri.fr/perso/nrougier/python-opengl/#the-hard-way
"""

import ctypes
import logging
import sys
import numpy as np


logger = logging.getLogger(__name__)


vertex_code = '''
attribute vec2 position;
void main()
{
  gl_Position = vec4(position, 0.0, 1.0);
}
'''





"""class OpenGLWindow(QOpenGLWidget):

    @property
    def frag_shader(self):
        return self._fragment_code

    def __init__(self,txt):
        QOpenGLWidget.__init__(self)

        if txt:
            self._fragment_code = txt
        else:
            self._fragment_code = '''
                        void main()
                        {
                          gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
                        }
                        '''

    def initializeGL(self):

        #QtWidgets.QWidget.__init__(self)
        self.program = gl.glCreateProgram()
        self.vertex = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        self.fragment = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)

        # Set shaders source
        gl.glShaderSource(self.vertex, vertex_code)
        gl.glShaderSource(self.fragment, self._fragment_code)

        # Compile shaders
        gl.glCompileShader(self.vertex)
        if not gl.glGetShaderiv(self.vertex, gl.GL_COMPILE_STATUS):
            error = gl.glGetShaderInfoLog(self.vertex).decode()
            logger.error("Vertex shader compilation error: %s", error)

        gl.glCompileShader(self.fragment)
        if not gl.glGetShaderiv(self.fragment, gl.GL_COMPILE_STATUS):
            error = gl.glGetShaderInfoLog(self.fragment).decode()
            print(error)
            raise RuntimeError("Fragment shader compilation error")

        gl.glAttachShader(self.program, self.vertex)
        gl.glAttachShader(self.program, self.fragment)
        gl.glLinkProgram(self.program)

        if not gl.glGetProgramiv(self.program, gl.GL_LINK_STATUS):
            print(gl.glGetProgramInfoLog(self.program))
            raise RuntimeError('Linking error')

        gl.glDetachShader(self.program, self.vertex)
        gl.glDetachShader(self.program, self.fragment)

        gl.glUseProgram(self.program)

        # Build data
        data = np.zeros((4, 2), dtype=np.float32)
        # Request a buffer slot from GPU
        buffer = gl.glGenBuffers(1)

        # Make this buffer the default one
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)

        stride = data.strides[0]

        offset = ctypes.c_void_p(0)
        loc = gl.glGetAttribLocation(self.program, "position")
        gl.glEnableVertexAttribArray(loc)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
        gl.glVertexAttribPointer(loc, 2, gl.GL_FLOAT, False, stride, offset)

        # Assign CPU data
        data[...] = [(-1, +1), (+1, +1), (+1, -1), (-1, -1)]

        # Upload CPU data to GPU buffer
        gl.glBufferData(
            gl.GL_ARRAY_BUFFER, data.nbytes, data, gl.GL_DYNAMIC_DRAW)

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glDrawArrays(gl.GL_QUAD_STRIP, 0, 4)
        #gl.glUseProgram(self.program)
        print("paint gl ! ")

    def resizeGL(self, w: int, h: int):
        side = min(w,h)
        if side<0:
            return
        #self.paintGL()
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        print("resize")
        #gl.glViewport((w-side)/2,(h-side)/2)

    def update_fragment_code(self,txt):
        self._fragment_code = txt
        QOpenGLWidget.__init__(self)
        self.paintGL()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = OpenGLWindow(None)
    widget.show()
    sys.exit(app.exec_())"""


"""import sys
import numpy as np
import OpenGL.GL as gl

from PySide2.QtWidgets import QApplication, QOpenGLWidget
from PySide2.QtGui import QSurfaceFormat

class OpenGLWindow(QOpenGLWidget):
    def initializeGL(self):
        # set the format for the OpenGL context
        format = QSurfaceFormat()
        format.setVersion(3, 3)
        format.setProfile(QSurfaceFormat.CoreProfile)
        self.setFormat(format)

        # create the vertex data
        self.vertices = np.array([-0.5, -0.5, 0.0,
                                  0.5, -0.5, 0.0,
                                  0.5,  0.5, 0.0
                                  -0.5, 1, 0.0], dtype=np.float32)

        # create a Vertex Buffer Object (VBO) to store the vertex data on the GPU
        self.vbo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, len(self.vertices)*4, (ctypes.c_float*len(self.vertices))(*self.vertices), gl.GL_STATIC_DRAW)
        position_location = 0  # This is the location of the position attribute in the shader
        gl.glVertexAttribPointer(position_location, 3, gl.GL_FLOAT, gl.GL_FALSE,0 , None)
        gl.glEnableVertexAttribArray(position_location)
        #gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)

    def paintGL(self):
        # clear the color and depth buffers
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        # bind the VBO
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)

        # specify the vertex data format
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, None)

        # enable the vertex attribute array
        gl.glEnableVertexAttribArray(0)

        # draw the primitives
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, len(self.vertices)//3)

        # disable the vertex attribute array
        gl.glDisableVertexAttribArray(0)

        # unbind the VBO
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = OpenGLWindow()
    window.show()

    sys.exit(app.exec_())"""

import sys
import OpenGL.GL as gl

from PySide2.QtWidgets import QApplication, QOpenGLWidget, QWidget
from PySide2.QtGui import QSurfaceFormat

class OpenGLWindow(QOpenGLWidget):
    def __init__(self, text=None):
        super(OpenGLWindow, self).__init__()
        if text:
            self.fragment_shader_source = text
            print("text = {}".format(text))
        else:
            self.fragment_shader_source = '''
                            void main()
                            {
                                out_color = vec4(uv.x);
                            }
                        '''

    def initializeGL(self):
        format = QSurfaceFormat()
        format.setVersion(4, 6)
        format.setProfile(QSurfaceFormat.CoreProfile)
        self.setFormat(format)

        vertex_shader_source = '''
                    #version 410

                    in vec3 position;
                    out vec2 uv;
                    void main()
                    {
                        uv = position.xy*0.5+0.5;
                        gl_Position = vec4(position, 1.0);
                    }
                '''

        self.vertex_shader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        gl.glShaderSource(self.vertex_shader, vertex_shader_source)
        gl.glCompileShader(self.vertex_shader)
        success = gl.glGetShaderiv(self.vertex_shader, gl.GL_COMPILE_STATUS)
        if not success:
            print("shader error on vertex shader : ")
            print(gl.glGetShaderInfoLog(self.vertex_shader).decode())

        self.load_shader()
        """success = gl.glGetShaderiv(self.shader_program, gl.GL_LINK_STATUS)
        if not success:
            print("shader program link failed : ")
            print(gl.glGetShaderInfoLog(self.shader_program).decode())"""

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        gl.glUseProgram(self.shader_program)
        gl.glBegin(gl.GL_QUADS)
        gl.glVertex2f(-1.0, -1.0)
        gl.glVertex2f(1.0, -1.0)
        gl.glVertex2f(1.0, 1.0)
        gl.glVertex2f(-1.0, 1.0)
        gl.glEnd()


    def load_shader(self):
        """
        compile a new shader and link it to the current program if succes
        :return success_info : a description string about the success of the operation
        """
        success_info = ""
        self.fragment_shader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        print("self.format_shader(self.fragment_shader_source) = {}".format(self.format_shader(self.fragment_shader_source)))
        gl.glShaderSource(self.fragment_shader, self.format_shader(self.fragment_shader_source))
        gl.glCompileShader(self.fragment_shader)
        success = gl.glGetShaderiv(self.fragment_shader, gl.GL_COMPILE_STATUS)
        if not success:
            success_info = f"shader error on fragment shader : {gl.glGetShaderInfoLog(self.fragment_shader).decode()}"
        else:
            self.shader_program = gl.glCreateProgram()
            gl.glAttachShader(self.shader_program, self.vertex_shader)
            gl.glAttachShader(self.shader_program, self.fragment_shader)
            gl.glLinkProgram(self.shader_program)
            success_info = "shader compiled successfully"

        return success_info
        """success = gl.glGetShaderiv(self.shader_program, gl.GL_LINK_STATUS)
        if not success:
            print("shader program link failed : ")
            print(gl.glGetShaderInfoLog(self.shader_program).decode())"""

    def update_shader(self, shader_text):
        print("shader_text = {0}".format(shader_text))
        self.fragment_shader_source = shader_text
        #gl.glDetachShader(self.shader_program, self.fragment_shader)
        success_info = self.load_shader()
        self.update()
        #self.initializeGL()
        return success_info

    def format_shader(self, text):
        return """#version 410
        in vec2 uv;
        out vec4 out_color;
        {0}
        """.format(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OpenGLWindow()
    window.show()
    sys.exit(app.exec_())