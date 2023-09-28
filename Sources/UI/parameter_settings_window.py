from PySide2 import QtWidgets
from PySide2.QtWidgets import QCheckBox, QHBoxLayout, QLineEdit, QLabel

class ParameterSettingsWindow(QtWidgets.QWidget):
    def __init__(self, mode_title, action_callback):
        super(ParameterSettingsWindow, self).__init__()
        self.main_layout = QtWidgets.QVBoxLayout()
        self.action_callback = action_callback

        #parameter type menu
        #parameter_type_menu = QtWidgets.QMenu("parameter type", self)
        Slider_selection = QtWidgets.QAction("Slider", self)
        Slider_selection.triggered.connect(self.on_parameter_type_selected)
        Toggle_selection = QtWidgets.QAction("Toggle", self)
        Toggle_selection.triggered.connect(self.on_parameter_type_selected)
        param_input_layout = QHBoxLayout()
        param_input_layout.addWidget(QLabel("name : "))
        self.param_name_widget = QLineEdit()
        param_input_layout.addWidget(self.param_name_widget)
        param_input_layout.addWidget(QLabel("shader linked : "))
        self.is_shader_widget = QCheckBox()
        self.is_shader_widget.setChecked(True)
        param_input_layout.addWidget(self.is_shader_widget)
        #parameter_type_menu.addAction(Slider_selection)
        #parameter_type_menu.addAction(Toggle_selection)
        #drop down for paramter type
        #self.dropdown_param_select = QtWidgets.QPushButton("Parameter Type")
        #self.dropdown_param_select.setMenu(parameter_type_menu)
        self.main_layout.addLayout(param_input_layout)
        #application buttons
        layout_btn = QtWidgets.QHBoxLayout()
        self.create_btn = QtWidgets.QPushButton(mode_title)
        self.create_btn.clicked.connect(self.on_create)
        layout_btn.addWidget(self.create_btn)
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.on_cancel)
        layout_btn.addWidget(self.cancel_btn)
        self.main_layout.addLayout(layout_btn)
        self.setLayout(self.main_layout)

    def on_parameter_type_selected(self):
        action = self.sender()
        option_text = action.text()
        self.dropdown_param_select.setText(option_text)
        print(option_text)

    def on_cancel(self):
        self.close()

    def on_create(self):
        param_name = self.param_name_widget.text()
        parameter_infos = {}
        parameter_infos["type"] = "FF_TYPE_STANDARD"
        parameter_infos["name"] = param_name
        parameter_infos["isShader"] = self.is_shader_widget.isChecked()
        parameter_infos["value"] = "0.5"
        success = self.action_callback(parameter_infos)
        if not success: #self.manager.has_parameter(param_name):
            print("parameter already exist !")
        else:
            self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    p = ParameterSettingsWindow()
    p.show()
    app.exec_()
