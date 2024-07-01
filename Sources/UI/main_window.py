from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QFileDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, \
    QTextEdit,QToolButton, QScrollArea

from opengl_window import OpenGLWindow
from parameter_settings_window import ParameterSettingsWindow
from FFGL_creator_ui import FFGLCreatorUI
from manager import Manager
from Core import config_manager as config
from slider_widget import FFGLSlider

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
        self.shader_file_spliter = r"////saved sliders\\\\" #used fo splitting the saved file in a shader part and a parameter part


        #list of created parameter will need to move somwhere else, make a specific parameter object and add it to an ffgl object
        self.parameters = [] #list of FFGLParameter

        #ffgl core management
        self.ffgl_manager = Manager(config_data)

        self.parameter_settings_window = ParameterSettingsWindow(mode_title="Create",action_callback=self.create_slider_handler)
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
        load_button.clicked.connect(self.on_load_shader)
        menu_layout.addWidget(load_button)
        write_layout.addLayout(menu_layout)

        # ffgl parameter layout
        self.parameter_layout = QVBoxLayout()
        self.parameter_menu_layout = QHBoxLayout()
        self.create_slider_btn = QPushButton("Create Slider")
        self.create_slider_btn.clicked.connect(self.on_create_slider)
        self.parameter_menu_layout.addWidget(self.create_slider_btn)
        self.create_checkbox_btn = QPushButton("Create Checkbox")
        self.create_checkbox_btn.clicked.connect(self.create_checkbox)
        self.parameter_menu_layout.addWidget(self.create_checkbox_btn)
        self.parameter_layout.addLayout(self.parameter_menu_layout)

        #dynamic parameter section
        widget_param_container = QWidget()

        self.vlayout_param_container = QVBoxLayout()
        widget_param_container.setLayout(self.vlayout_param_container)
        scroll_bar = QScrollArea()
        scroll_bar.setWidgetResizable(True)
        scroll_bar.setMinimumSize(350,300)
        scroll_bar.setWidget(widget_param_container)
        self.parameter_layout.addWidget(scroll_bar)

        # opengl Layout
        self.opengl_layout = QVBoxLayout()
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
        glsl_dev_module_layout.addLayout(self.parameter_layout)
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

    def refresh_shader(self):
        self.opengl_widget.update()

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
            #save the parameters
            f.write(self.shader_file_spliter)
            for p in self.parameters:
                f.write(f"{p.name}\n")
            f.close()

    def on_load_shader(self):
        option = QFileDialog.ReadOnly
        file_dialog = QFileDialog.getOpenFileName(self, "Open Shader", "", "Shader Files (*.shd);;All Files (*)",
                                                  options=option)
        print(f"save path = {file_dialog[0]}")
        if file_dialog[0]:
            path = file_dialog[0]
            f = open(path, "r")
            params = self.parameters
            for i in params:
                self.remove_slider_handler(i.name)
            #split shader part and parameter part
            datas = f.read().split(self.shader_file_spliter)
            self.load_datas(datas)
            f.close()

    def load_datas(self, datas):
        """
        should be moved into the model part
        todo: define a rreal save format, with a shader text part and a param description structure (json) ?
        :param datas: [str]
        :return:
        """
        shader_text = datas[0]
        self.shader_txt_widget.setText(shader_text)
        if len(datas) >= 2:  # there is some parameters to load
            print(f"datas[1] = {datas[1]}")
            parameters = datas[1].split("\n")
            for p in parameters:
                if p is not "":
                    # todo: put that in a function and share it in 'parameter_settings_windows.on_create'
                    parameter_infos = {}
                    parameter_infos["type"] = "FF_TYPE_STANDARD"
                    parameter_infos["name"] = p
                    parameter_infos["isShader"] = True
                    parameter_infos["value"] = "0.5"
                    print(f"parameter_infos = {parameter_infos}")
                    self.create_slider_handler(parameter_infos)

    def on_create_slider(self):
        parameter_type = "FF_TYPE_STANDARD"
        print("create slider")
        self.parameter_settings_window.show()

        """slider_widget = QtWidgets.QSlider(Qt.Horizontal)
        slider_widget.setMinimum(0)
        slider_widget.setMaximum(100)
        slider_widget.setValue(50)
        slider_widget.setFixedWidth(150)
        slider_layout = QHBoxLayout()
        pref_button = QToolButton()
        pref_button.setIcon(QIcon("Icons/pref_icon.png"))
        pref_button.setFixedSize(20,20)
        slider_layout.addWidget(pref_button)
        slider_layout.addWidget(QLabel("name"))
        slider_layout.addWidget(QLabel(":"))
        slider_layout.addWidget(QLabel("value"))
        slider_layout.addWidget(slider_widget)
        remove_btn = QToolButton()
        remove_btn.setIcon(QIcon("Icons/remove_icon.png"))
        slider_layout.addWidget(remove_btn)
        self.parameter_layout.addLayout(slider_layout)
        self.parameter_layout.update()"""
        """parameter = FFGLParameter(parameter_type, parameter_infos["IsShader"], parameter_infos["Name"],
                                  parameter_infos["Value"], len(self.parameters))
        if parameter.m_bIsShader:
            self.shader_txt_widget.insertPlainText(f"uniform float {parameter.m_sParamName};\n")"""

    def create_checkbox(self):
        self.parameter_settings_window.show()

    def remove_slider_handler(self, p_name):
        print("remove slider")
        #find slider
        ffgl_slider = None
        for i in self.parameters:
            print(f"i.name = {i.name}, p_name = {p_name}")
            if i.name is p_name:
                ffgl_slider = i
        ffgl_slider.setParent(None)
        parameter_code = f"uniform float {p_name};"
        shader_code = self.shader_txt_widget.toPlainText()
        shader_code = shader_code.replace(parameter_code, "")
        self.shader_txt_widget.setText(shader_code)
        self.parameters.remove(ffgl_slider)

    def create_slider_handler(self, parameter_infos):
        """
        create a parameter according of the data passed in argument
        :param dictionary parameter_infos: dictionary containing info of the parameter name, type, value, min max
        :return:
        """
        success = True
        p_name = parameter_infos["name"]
        default_value = parameter_infos["value"]
        if self.has_parameter(p_name):
            success = False
            print("parameter already exist !!")
        else:
            ffgl_slider = FFGLSlider(index = len(self.parameters), param_name=p_name, param_value=default_value,
                                     param_manager=self, remove_handler = self.remove_slider_handler)
            self.vlayout_param_container.addWidget(ffgl_slider)
            if ffgl_slider.is_shader:
                self.add_shader_parameter(p_name)
            """print("create_parameter_handler")
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
            """
            self.parameters.append(ffgl_slider)
        return success
        """todo: gerer les unittest et parameters input"""

    def has_parameter(self, p_name):
        """
        Check if a parameter is already existing
        :param str p_name:
        :return FFGLSlider param: return the parameter if the parameter exist or None otherwise
        """
        param = None
        for p in self.parameters:
            if p.name == p_name:
                param = p
                break
        return param

    def add_shader_parameter(self,p_name):
        parameter_code = f"uniform float {p_name};"
        if parameter_code not in self.shader_txt_widget.toPlainText():
            self.shader_txt_widget.insertPlainText(f"{parameter_code}\n")
        else:
            print("parameter already exist in the shader code")
        self.opengl_widget.ffgl_parameters = self.parameters


    def update_shader_parameter(self,old_p_name, new_p_name):
        """
        trigg by the
        :param  dictionary parameter_infos: dictionary containing info of the parameter name, type, value, min max
        :return:
        """
        #print(slider.name)
        text = self.shader_txt_widget.toPlainText()
        text = text.replace(old_p_name, new_p_name)
        self.shader_txt_widget.setText(text)
        #self.update()
        """p_name = parameter_infos["name"]
        param = self.has_parameter(p_name)
        param.update_info(parameter_infos)
        """

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