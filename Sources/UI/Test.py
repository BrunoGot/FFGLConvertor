import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QOpenGLWidget, QVBoxLayout, QWidget
from PySide2.QtGui import QSurfaceFormat
from opengl_window import OpenGLWindow

"""class OpenGLWindow(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def initializeGL(self):
        pass

    def paintGL(self):
        pass
"""
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.gl_widget = OpenGLWindow()
        self.gl_widget.setMinimumWidth(540)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        layout.addWidget(self.gl_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    """format = QSurfaceFormat()
    format.setVersion(3, 3)
    format.setProfile(QSurfaceFormat.CoreProfile)
    QSurfaceFormat.setDefaultFormat(format)"""

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
