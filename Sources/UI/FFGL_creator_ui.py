import json
from PySide2 import QtWidgets

from dropdown_menu_ui import DropDownMenuUI

class FFGLCreatorUI(QtWidgets.QWidget):
    FFGL_type = "FX"
    FFGL_NAME = ""
    Param_NB = 1
    DESCRIPTION = ""
    COMMENT = ""

    def get_ui(self):
        pass

    def __init__(self):
        super(FFGLCreatorUI, self).__init__()


        self.main_layout = QtWidgets.QVBoxLayout()
        #Name & ID inputs
        name_input_layout = QtWidgets.QHBoxLayout()
        name_input_label = QtWidgets.QLabel("FFGL Name")
        name_input_layout.addWidget(name_input_label)
        self.ffgl_name_input = QtWidgets.QLineEdit()
        name_input_layout.addWidget(self.ffgl_name_input)
        #ID
        ffgl_id_label = QtWidgets.QLabel("FFGL Unique ID")
        name_input_layout.addWidget(ffgl_id_label)
        self.ffgl_id_input = QtWidgets.QLineEdit()
        name_input_layout.addWidget(self.ffgl_id_input)
        self.main_layout.addLayout(name_input_layout)
        #nb param
        ffgl_parm_num_label = QtWidgets.QLabel("param number : ")
        name_input_layout.addWidget(ffgl_parm_num_label)
        self.ffgl_parm_number = QtWidgets.QLabel("0")
        name_input_layout.addWidget(self.ffgl_parm_number)
        #type menu section
        self.ffgl_type_menu = DropDownMenuUI("Type")
        self.ffgl_type_menu.add_option("FX", self.on_ffgl_type_selected)
        self.ffgl_type_menu.add_option("Source", self.on_ffgl_type_selected)
        self.ffgl_type_menu.add_option("Mixer", self.on_ffgl_type_selected)
        self.main_layout.addWidget(self.ffgl_type_menu)
        #comment section
        self.comment_input, comm_layout = self.input_comment_console("Comment")
        self.main_layout.addLayout(comm_layout)
        #additional comment
        self.additional_com_input,additional_com_layout = self.input_comment_console("Additional Comment")
        self.main_layout.addLayout(additional_com_layout)
        self.setLayout(self.main_layout)

    def on_create_FFGL(self, parameter_number):
        pass
        #just connect with the manager.py code

    def on_ffgl_type_selected(self):
        action = self.sender()
        option_text = action.text()
        self.ffgl_type_menu.setText(option_text)
        #self.FFGL_type =

    def input_comment_console(self, label_name):
        label = QtWidgets.QLabel(label_name)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label)
        text_input = QtWidgets.QTextEdit()
        layout.addWidget(text_input)
        return text_input,layout

    def check_input(self):
        """
        check if all input are corrects
        :return bool: return true if all is correct false otherwise
        """

        val = True
        #here are all the description error message to the input field to test
        input_list = {}
        input_list[self.ffgl_name_input] =  "no input name"
        input_list[self.ffgl_id_input] =  "no input id"
        input_list[self.comment_input] =  "no input comment"
        for widget,error_val in input_list.items():
            text = widget.text() if hasattr(widget, "text") else widget.toPlainText()
            if not text:
                val = False
                self.trig_error(error_val)
                return val
        return val

    def trig_error(self, msg):
        print("error : {}".format(msg))

    def get_input_datas(self):
        """
        get all the input datas into a dictionary and return it
        :return:
        """
        ffgl_data = {}
        ffgl_data["pluginName"] = self.ffgl_name_input.text()
        ffgl_data["pluginID"] = self.ffgl_id_input.text()
        ffgl_data["pluginDescription"] = self.comment_input.toPlainText()
        ffgl_data["pluginNote"] = self.additional_com_input.toPlainText()
        ffgl_data["Type"] = self.ffgl_type_menu.text()
        return ffgl_data

