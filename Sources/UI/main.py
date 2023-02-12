from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QSurfaceFormat
from opengl_window import OpenGLWindow
from main_window import MainWindow

if __name__ == '__main__':
    app = QApplication([])


    widget = MainWindow()
    widget.show()
    app.exec_()