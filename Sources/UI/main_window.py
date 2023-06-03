import json
from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton

from opengl_window import OpenGLWindow
from parameter_settings_window import ParameterSettingsWindow
from FFGL_creator_ui import FFGLCreatorUI
from manager import Manager
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

        #config
        config_file_path = "D:\Documents\Code\Python\FFGLConvertor\Sources\config.json"
        with open(config_file_path) as json_file:
            config_file = json_file.read()
        config_data = json.loads(config_file)
        #ffgl core management
        self.ffgl_manager = Manager(config_data)

        self.parameter_settings_window = ParameterSettingsWindow(create_param_callback=self.create_parameter_handler)
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


        self.create_parameter_btn = QPushButton("Create Parameter")
        self.create_parameter_btn.clicked.connect(self.create_parameter)
        self.opengl_layout.addWidget(self.create_parameter_btn)
        self.parameter_layout = QVBoxLayout()

        self.opengl_layout.addWidget(self.create_parameter_btn)
        self.opengl_layout.addLayout(self.parameter_layout)

        self.opengl_widget = OpenGLWindow(shader_base_text)
        self.opengl_widget.setFixedSize(300, 300)
        self.opengl_layout.addWidget(self.opengl_widget)

        main_ffgl_layout = QVBoxLayout()
        glsl_dev_module_layout = QHBoxLayout()
        glsl_dev_module_layout.addLayout(write_layout)
        glsl_dev_module_layout.addLayout(self.opengl_layout)
        main_ffgl_layout.addLayout(glsl_dev_module_layout)
        self.ffgl_creator_module = FFGLCreatorUI()
        main_ffgl_layout.addWidget(self.ffgl_creator_module)

        self.create_ffgl_button = QPushButton("CreateFFGL")
        self.create_ffgl_button.clicked.connect(self.on_create_FFGL)
        main_ffgl_layout.addWidget(self.create_ffgl_button)

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

    def create_parameter(self):
        self.parameter_settings_window.show()

    def create_parameter_handler(self, parameter_infos):
        """
        create a parameter according of the data passed in argument
        :param dictionary parameter_infos: dictionary containing info of the parameter name, type, value, min max
        :return:
        """
        print("create_parameter_handler")
        print(parameter_infos)
        type = parameter_infos.get("type")
        if type.lower() == "slider":
            print("create slider")
            slider_widget = QtWidgets.QSlider(Qt.Horizontal)
            slider_widget.setMinimum(0)
            slider_widget.setMaximum(10)
            slider_widget.setValue(5)
            self.parameter_layout.addWidget(slider_widget)
            self.parameter_layout.update()

    """todo: gerer les template et connecter aux input avec ffgl_creator_module.check_input():"""

    def on_create_FFGL(self):
        """
        handler trigged when click on the button "Create FFGL"
        :return:
        """
        if self.ffgl_creator_module.check_input():
            pass
            #    print("check input")
            #glsl_code = ""
        ffgl_info = {"ffgl_type" : "FX", "paramNumber" : "1", "paramName" : "test", "paramType" : "1", "paramVal" : "0", "pluginDescription" : "", "pluginNote" : "", "pluginName" : "testYoua"}
        self.ffgl_manager.CreateFFGL("2", ffgl_info["ffgl_type"], ffgl_info["paramNumber"], ffgl_info["paramName"], ffgl_info["paramType"], ffgl_info["paramVal"], ffgl_info["pluginDescription"], ffgl_info["pluginNote"], ffgl_info["pluginName"])