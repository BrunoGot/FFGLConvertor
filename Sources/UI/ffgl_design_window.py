from PySide2 import QtWidgets
from opengl_window import OpenGLWindow
class FFGLDesignWindow(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.init_gui()

    def init_gui(self):
        self.main_layout = QtWidgets.QHBoxLayout()

        self.text_layout = QtWidgets.QVBoxLayout()

        self.fragment_shad_txt = QtWidgets.QPlainTextEdit()
        self.text_layout.addWidget(self.fragment_shad_txt)
        self.update_btn = QtWidgets.QPushButton("Update")
        self.update_btn.clicked.connect(self.update_shader)
        self.text_layout.addWidget(self.update_btn)
        #self.main_layout.addLayout(self.text_layout)

        self.openGL_layout = QtWidgets.QVBoxLayout()
        self.openGL_view = OpenGLWindow("")
        self.openGL_view.setFixedSize(300,300)
        self.openGL_layout.addWidget(self.openGL_view)
        self.label = QtWidgets.QLabel("test")
        self.openGL_layout.addWidget(self.label)
        self.main_layout.addLayout(self.openGL_layout)
        self.main_layout.addLayout(self.text_layout)
        self.setLayout(self.main_layout)

        #init text with the shader code
        self.fragment_shad_txt.setPlainText(self.openGL_view.fragment_shader_source)


    def update_shader(self):
        """bad coded improve this later"""
        self.label.setText("upadted")

        frag_shader = self.fragment_shad_txt.toPlainText()

        self.openGL_view.deleteLater()
        self.openGL_view = OpenGLWindow(frag_shader)
        self.openGL_view.setFixedSize(300, 300)
        self.openGL_layout.insertWidget(0,self.openGL_view)
