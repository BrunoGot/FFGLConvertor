from PySide2 import QtWidgets

class ParameterSettingsWindow(QtWidgets.QWidget):
    def __init__(self, create_param_callback=None):
        super(ParameterSettingsWindow, self).__init__()
        self._create_param_callback = create_param_callback
        self.main_layout = QtWidgets.QVBoxLayout()
        #parameter type menu
        parameter_type_menu = QtWidgets.QMenu("parameter type", self)
        Slider_selection = QtWidgets.QAction("Slider", self)
        Slider_selection.triggered.connect(self.on_parameter_type_selected)
        Toggle_selection = QtWidgets.QAction("Toggle", self)
        Toggle_selection.triggered.connect(self.on_parameter_type_selected)
        parameter_type_menu.addAction(Slider_selection)
        parameter_type_menu.addAction(Toggle_selection)
        #drop down for paramter type
        self.dropdown_param_select = QtWidgets.QPushButton("Parameter Type")
        self.dropdown_param_select.setMenu(parameter_type_menu)
        self.main_layout.addWidget(self.dropdown_param_select)
        #application buttons
        layout_btn = QtWidgets.QHBoxLayout()
        self.create_btn = QtWidgets.QPushButton("Create")
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
        parameter_infos = {}
        parameter_infos["Type"] = self.dropdown_param_select.text()
        parameter_infos["Name"] = "Test"
        parameter_infos["IsShader"] = "True"
        parameter_infos["Value"] = "0.0"
        self._create_param_callback(parameter_infos)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    p = ParameterSettingsWindow()
    p.show()
    app.exec_()
