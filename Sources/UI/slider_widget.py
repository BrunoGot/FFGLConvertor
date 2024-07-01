from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QHBoxLayout,QLabel, QWidget, QSlider, QToolButton

from parameter_settings_window import ParameterSettingsWindow
from Core.ffgl_parameter import FFGLParameter

class FFGLSlider(QWidget):
    def __init__(self, index, param_name = "", param_value=0.5, is_shader=True, param_manager=None, parent = None, remove_handler=None):
        super(FFGLSlider, self).__init__(parent)
        self.name = param_name
        self.default_value = param_value
        self.is_shader = is_shader
        self.param_manager = param_manager
        self.param_settings_window = ParameterSettingsWindow(mode_title="Update",action_callback=self.update_slider)
        #add ffgl_parameter class as model part of the ffglSliderView
        icon_size = 30
        #pref button
        main_layout = QHBoxLayout()
        pref_button = QToolButton()
        pref_button.setIcon(QIcon("Icons/pref_icon.png"))
        pref_button.setFixedSize(icon_size, icon_size)
        pref_button.clicked.connect(self.on_pref_button)
        main_layout.addWidget(pref_button)

        #slider
        self.widget_name = QLabel(f"{self.name} : {self.default_value}")
        main_layout.addWidget(self.widget_name)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setFixedWidth(150)
        self.slider.valueChanged.connect(self.on_slider_change)
        self.slider.setValue(float(self.default_value))
        main_layout.addWidget(self.slider)
        self.setLayout(main_layout)

        #remove button
        remove_btn = QToolButton()
        remove_btn.setIcon(QIcon("Icons/remove_icon.png"))
        remove_btn.setFixedSize(icon_size, icon_size)
        remove_btn.clicked.connect(lambda b = True, name= self.name : remove_handler(name))
        main_layout.addWidget(remove_btn)

        #todo : refectorr this class into a FFGLSlider that contain a QSlider and a FFGLPArameter (View/Model)
        self.ffgl_parameter = FFGLParameter("FF_TYPE_STANDARD", self.is_shader, self.name,
                                  self.default_value, index)

    @property
    def value(self):
        return self.slider.value()/100

    def on_slider_change(self,value):
        self.widget_name.setText(f"{self.name} : {self.value}")
        if self.is_shader:
            self.param_manager.refresh_shader()
        #self.widget_name.update()

    def on_pref_button(self):
        self.param_settings_window.show()

    def update_slider(self, parameter_infos):
        print(f"current name = {self.name}")
        print("new name = "+parameter_infos["name"])
        name = parameter_infos["name"]
        success = True
        if (name != self.name) and self.param_manager.has_parameter(name):
            print("name already exist")
            success = False
        else :
            self.param_manager.update_shader_parameter(old_p_name=self.name,new_p_name=name)
            self.name = name
            self.is_shader = parameter_infos["isShader"]
            self.default_value = parameter_infos["value"]
            self.widget_name.setText(f"{self.name} : {self.default_value}")
        return success

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            print("reset value")
            self.slider.setValue(float(self.default_value))
        else:
            super().mousePressEvent()