from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QFileDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit

from opengl_window import OpenGLWindow
from parameter_settings_window import ParameterSettingsWindow
from FFGL_creator_ui import FFGLCreatorUI
from manager import Manager
from Core.ffgl_parameter import FFGLParameter
from Core import config_manager as config

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
                                out_color = vec4(uv.x);
                            }"""

        config_data = config.get_datas()

        #list of created parameter will need to move somwhere else, make a specific parameter object and add it to an ffgl object
        self.parameters = [] #list of FFGLParameter

        #ffgl core management
        self.ffgl_manager = Manager(config_data)

        self.parameter_settings_window = ParameterSettingsWindow(create_param_callback=self.create_parameter_handler)
        #Write layout
        write_layout = QVBoxLayout()
        self.shader_txt_widget = QTextEdit()
        self.shader_txt_widget.setText(shader_base_text)
        write_layout.addWidget(self.shader_txt_widget)
        menu_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_shader)
        menu_layout.addWidget(save_button)
        load_button = QPushButton("Load")
        load_button.clicked.connect(self.load_shader)
        menu_layout.addWidget(load_button)
        write_layout.addLayout(menu_layout)

        #opengl Layout
        self.opengl_layout = QVBoxLayout()

        self.parameter_menu_layout = QHBoxLayout()
        self.create_slider_btn = QPushButton("Create Slider")
        self.create_slider_btn.clicked.connect(self.create_slider)
        self.parameter_menu_layout.addWidget(self.create_slider_btn)
        self.create_checkbox_btn = QPushButton("Create Checkbox")
        self.create_checkbox_btn.clicked.connect(self.create_checkbox)
        self.parameter_menu_layout.addWidget(self.create_checkbox_btn)
        self.opengl_layout.addLayout(self.parameter_menu_layout)
        #dynamic parameter section
        self.parameter_layout = QVBoxLayout()
        self.opengl_layout.addLayout(self.parameter_layout)

        self.opengl_widget = OpenGLWindow(shader_base_text)
        self.opengl_widget.setFixedSize(300, 300)
        self.opengl_layout.addWidget(self.opengl_widget)
        self.log_error_consol = QTextEdit()
        self.opengl_layout.addWidget(QLabel("log error : "))
        self.opengl_layout.addWidget(self.log_error_consol)
        submit_button = QPushButton("update")
        submit_button.clicked.connect(self.update_shader)
        self.opengl_layout.addWidget(submit_button)

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
        self.log_error_consol.clear()
        success_info = self.opengl_widget.update_shader(self.shader_txt_widget.toPlainText())
        self.log_error_consol.setText(success_info)

    def save_shader(self):
        option = QFileDialog.ReadOnly
        file_dialog = QFileDialog.getSaveFileName(self, "Save Shader","", "Shader Files (*.shd);;All Files (*)", options = option)
        print(f"save path = {file_dialog[0]}")
        if file_dialog[0]:
            path = file_dialog[0]
            f = open(path,"w")
            f.write(self.shader_txt_widget.toPlainText())
            f.close()

    def load_shader(self):
        option = QFileDialog.ReadOnly
        file_dialog = QFileDialog.getOpenFileName(self, "Open Shader", "", "Shader Files (*.shd);;All Files (*)",
                                                  options=option)
        print(f"save path = {file_dialog[0]}")
        if file_dialog[0]:
            path = file_dialog[0]
            f = open(path, "r")
            self.shader_txt_widget.setText(f.read())
            f.close()

    def create_slider(self):
        self.parameter_settings_window.show()

    def create_checkbox(self):
        self.parameter_settings_window.show()

    def create_parameter_handler(self, parameter_infos):
        """
        create a parameter according of the data passed in argument
        :param dictionary parameter_infos: dictionary containing info of the parameter name, type, value, min max
        :return:
        """
        print("create_parameter_handler")
        print(parameter_infos)
        widget_type = parameter_infos.get("Type")
        if widget_type.lower() == "slider":
            parameter_type = "FF_TYPE_STANDARD"
            print("create slider")
            slider_widget = QtWidgets.QSlider(Qt.Horizontal)
            slider_widget.setMinimum(0)
            slider_widget.setMaximum(10)
            slider_widget.setValue(5)
            self.parameter_layout.addWidget(slider_widget)
            self.parameter_layout.update()
        parameter = FFGLParameter(parameter_type, parameter_infos["IsShader"], parameter_infos["Name"], parameter_infos["Value"], len(self.parameters))
        if parameter.m_bIsShader:
            self.shader_txt_widget.insertPlainText(f"uniform float {parameter.m_sParamName};\n")

        self.parameters.append(parameter)
    """todo: gerer les unittest et parameters input"""

    def on_create_FFGL(self):
        """
        handler trigged when click on the button "Create FFGL"
        :return:
        """
        if self.ffgl_creator_module.check_input():
            ffgl_info = self.ffgl_creator_module.get_input_datas()
            #    print("check input")
            #glsl_code = ""
            #ffgl_info = {"ffgl_type" : "FX", "paramNumber" : "1", "paramName" : "test", "paramType" : "1", "paramVal" : "0", "pluginDescription" : "", "pluginNote" : "", "pluginName" : "testYoua"}
            print("create FFGL....")
            self.ffgl_manager.CreateFFGL("2", ffgl_info["Type"], self.parameters, ffgl_info["pluginDescription"], ffgl_info["pluginNote"], ffgl_info["pluginName"], self.shader_txt_widget.toPlainText(), ffgl_info["pluginID"])
            print("export FFGL....")
            self.ffgl_manager.export_ffgl(ffgl_info["pluginName"])