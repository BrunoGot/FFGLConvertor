from PySide2 import QtWidgets
from ffgl_design_window import FFGLDesignWindow
from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from opengl_window import OpenGLWindow

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.init_ui()

    def init_ui(self):

        central_widget = QWidget()

        self.tab_widget = QtWidgets.QTabWidget()
        self.tab_widget.addTab(FFGL_write_window(), "ffgl design")
        #self.ffgl_

        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.tab_widget)



class FFGL_write_window(QWidget):
    def __init__(self):
        super(FFGL_write_window, self).__init__()
        shader_base_text = """void main()
                            {
                                out_color = vec4(pos.x);
                            }"""

        #Write layout
        write_layout = QVBoxLayout()
        self.shader_txt_widget = QtWidgets.QTextEdit()
        self.shader_txt_widget.setText(shader_base_text)
        write_layout.addWidget(self.shader_txt_widget)
        menu_layout = QHBoxLayout()
        submit_button = QPushButton("update")
        submit_button.clicked.connect(self.update_shader)
        menu_layout.addWidget(submit_button)
        write_layout.addLayout(menu_layout)

        #opengl Layout
        self.opengl_layout = QVBoxLayout()
        self.opengl_widget = OpenGLWindow(shader_base_text)
        self.opengl_widget.setFixedSize(300, 300)
        self.opengl_layout.addWidget(self.opengl_widget)

        main_ffgl_layout = QHBoxLayout()
        main_ffgl_layout.addLayout(write_layout)
        main_ffgl_layout.addLayout(self.opengl_layout)

        self.setLayout(main_ffgl_layout)


        """
        #ffgl_design = FFGLDesignWindow()
        self.tab_widget.addTab(ffgl_design,"ffgl design")
        test_button2 = QtWidgets.QLabel("test2")
        self.tab_widget.addTab(test_button2,"ffgl design")
        self.setCentralWidget(self.tab_widget)"""
        #self.main_layout.addWidget(test_button)
        #self.setLayout(self.main_layout)
        #self.setFixedSize(500,500)

    def update_shader(self):
        print("Update_shader")
        self.opengl_widget.update_shader(self.shader_txt_widget.toPlainText())
