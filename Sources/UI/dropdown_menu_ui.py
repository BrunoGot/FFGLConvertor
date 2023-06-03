from PySide2 import QtWidgets
class DropDownMenuUI(QtWidgets.QPushButton):
    def __init__(self, menu_name):
        super(DropDownMenuUI, self).__init__(menu_name)
        # parameter type menu
        self.parameter_type_menu = QtWidgets.QMenu(menu_name, self)
        # drop down for paramter type
        self.setMenu(self.parameter_type_menu)

    def add_option(self, action_name,callback ):
        option = QtWidgets.QAction(action_name, self)
        option.triggered.connect(callback)
        self.parameter_type_menu.addAction(option)