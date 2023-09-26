from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QSurfaceFormat
from opengl_window import OpenGLWindow
from main_window import MainWindow

def GUI_Style(app):
    file_qss = open("Styles/Combinear.qss")
    with file_qss:
        qss = file_qss.read()
        #print("QSS = "+qss)
        app.setStyleSheet(qss)

if __name__ == '__main__':
    app = QApplication([])

    GUI_Style(app)
    widget = MainWindow()
    widget.show()
    app.exec_()