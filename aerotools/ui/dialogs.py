import os
import numpy as np
from PyQt5 import QtWidgets, QtGui, uic
from PyQt5.QtGui import QDoubleValidator

import aerotools.core.calculations as calc
import aerotools.core.plotting as plotting
import aerotools.core.export as export

# Constants
UI_DIR = os.path.join(os.path.dirname(__file__), 'resources')
COLORS = {'Black': 'k', 'Blue': 'b', 'Red': 'r', 'Green': 'g'}

class BaseDialog(QtWidgets.QDialog):
    """Base class for all dialogs to handle common initialization."""
    def __init__(self, ui_filename):
        super(BaseDialog, self).__init__()
        ui_path = os.path.join(UI_DIR, ui_filename)
        uic.loadUi(ui_path, self)
        self.double_validator = QDoubleValidator()
    
    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def show_message(self, title, message, icon=QtWidgets.QMessageBox.Information):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setIcon(icon)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.setStyleSheet("QMessageBox {font: 12pt Ubuntu}")
        
        # Check if icon exists, otherwise skip or use default
        icon_path = "icons/check.png"
        
        button = msg_box.addButton(QtWidgets.QMessageBox.Ok)
        if os.path.exists(icon_path):
             button.setIcon(QtGui.QIcon(icon_path))
        button.setFixedSize(75, 35)
        button.setStyleSheet("QPushButton {font: 10pt Ubuntu}")
        
        msg_box.setDefaultButton(button)
        msg_box.exec_()

class ClvsVelocityDialog(BaseDialog):
    def __init__(self, weight, wing_area, rho):
        super().__init__('clvsVelDialog.ui')
        self.weight = weight
        self.wing_area = wing_area
        self.rho = rho
        
        self.setFixedSize(300, 285)
        self.center()
        self.pull_children()
        self.set_validators()
        self.adjust_line_color_property()
        
        self.apply_button.clicked.connect(self.apply)
        self.reject_button.clicked.connect(self.close)

    def pull_children(self):
        self.minv_edit = self.findChild(QtWidgets.QLineEdit, 'clminVel_lineEdit')
        self.maxv_edit = self.findChild(QtWidgets.QLineEdit, 'clmaxVel_lineEdit')
        self.linecolor_combo = self.findChild(QtWidgets.QComboBox, 'clvsVel_linecolor_comboBox')
        self.lineweight_spin = self.findChild(QtWidgets.QSpinBox, 'clvsVel_lw_spinBox')
        self.export_checkbox = self.findChild(QtWidgets.QCheckBox, 'exportData_checkBox')
        self.button_box = self.findChild(QtWidgets.QDialogButtonBox, 'clvsVels_buttonBox')
        self.apply_button = self.button_box.button(QtWidgets.QDialogButtonBox.Apply)
        self.reject_button = self.button_box.button(QtWidgets.QDialogButtonBox.Cancel)

    def set_validators(self):
        self.minv_edit.setValidator(self.double_validator)
        self.maxv_edit.setValidator(self.double_validator)

    def adjust_line_color_property(self):
        self.linecolor_combo.addItems(COLORS.keys())

    def apply(self):
        try:
            min_v = float(self.minv_edit.text())
            max_v = float(self.maxv_edit.text())
            
            cl = calc.lift_coefficient_range(min_v, max_v, self.weight, self.wing_area, self.rho)
            
            if self.export_checkbox.isChecked():
                export.export_cl_vs_velocity(cl, np.arange(min_v, max_v, 0.1))
                self.show_message("DATA HAVE BEEN EXPORTED SUCCESSFULLY", 
                                "All data have been exported inside 'XLSX Workbooks' folder.")

            plotting.plot_cl_vs_velocity(cl, min_v, max_v, 0.1, 
                                       COLORS.get(self.linecolor_combo.currentText()), 
                                       int(self.lineweight_spin.value()), True)

            # self.minv_edit.clear()
            # self.maxv_edit.clear()
            # self.close() # Original behavior closed the dialog
        except ValueError:
             self.show_message("Error", "Invalid Input Parameters", QtWidgets.QMessageBox.Warning)


class ThrustReqvsVelocityDialog(BaseDialog):
    def __init__(self, weight, wing_area, wingspan, rho, cd0):
        super().__init__('thrReqvsVelDialog.ui')
        self.weight = weight
        self.wing_area = wing_area
        self.wingspan = wingspan
        self.rho = rho
        self.cd0 = cd0

        self.setFixedSize(300, 285)
        self.center()
        self.pull_children()
        self.set_validators()
        self.adjust_line_color_property()

        self.apply_button.clicked.connect(self.apply)
        self.reject_button.clicked.connect(self.close)

    def pull_children(self):
        self.minv_edit = self.findChild(QtWidgets.QLineEdit, 'thrReqminVel_lineEdit')
        self.maxv_edit = self.findChild(QtWidgets.QLineEdit, 'thrReqmaxVel_lineEdit')
        self.linecolor_combo = self.findChild(QtWidgets.QComboBox, 'thrReqvsVel_linecolor_comboBox')
        self.lineweight_spin = self.findChild(QtWidgets.QSpinBox, 'thrReqvsVel_lw_spinBox')
        self.export_checkbox = self.findChild(QtWidgets.QCheckBox, 'exportData_checkBox')
        self.button_box = self.findChild(QtWidgets.QDialogButtonBox, 'thrReqvsVels_buttonBox')
        self.apply_button = self.button_box.button(QtWidgets.QDialogButtonBox.Apply)
        self.reject_button = self.button_box.button(QtWidgets.QDialogButtonBox.Cancel)

    def set_validators(self):
        self.minv_edit.setValidator(self.double_validator)
        self.maxv_edit.setValidator(self.double_validator)

    def adjust_line_color_property(self):
        self.linecolor_combo.addItems(COLORS.keys())
        self.linecolor_combo.setCurrentIndex(1)

    def apply(self):
        try:
            min_v = float(self.minv_edit.text())
            max_v = float(self.maxv_edit.text())
            
            ar = calc.aspect_ratio(self.wingspan, self.wing_area)
            oef = calc.oswald_efficiency_estimate(ar)
            k = calc.k_factor(ar, oef)
            
            cl = calc.lift_coefficient_range(min_v, max_v, self.weight, self.wing_area, self.rho)
            cd = calc.drag_coefficient(self.cd0, k, cl)
            
            thrust_req = calc.thrust_required_range(min_v, max_v, self.wing_area, self.rho, cd)

            if self.export_checkbox.isChecked():
                export.export_thrust_req_vs_velocity(thrust_req, np.arange(min_v, max_v, 0.1))
                self.show_message("DATA HAVE BEEN EXPORTED SUCCESSFULLY", 
                                "All data have been exported inside 'XLSX Workbooks' folder.")

            plotting.plot_thrust_req_vs_velocity(thrust_req, min_v, max_v, 0.1, 
                                               COLORS.get(self.linecolor_combo.currentText()), 
                                               int(self.lineweight_spin.value()), True)
        except ValueError:
             self.show_message("Error", "Invalid Input Parameters", QtWidgets.QMessageBox.Warning)


class PowerReqvsVelocityDialog(BaseDialog):
    def __init__(self, weight, wing_area, wingspan, rho, cd0):
        super().__init__('pwrReqvsVelDialog.ui')
        self.weight = weight
        self.wing_area = wing_area
        self.wingspan = wingspan
        self.rho = rho
        self.cd0 = cd0
        
        self.setFixedSize(300, 285)
        self.center()
        self.pull_children()
        self.set_validators()
        self.adjust_line_color_property()
        
        self.apply_button.clicked.connect(self.apply)
        self.reject_button.clicked.connect(self.close)

    def pull_children(self):
        self.minv_edit = self.findChild(QtWidgets.QLineEdit, 'pwrReqminVel_lineEdit')
        self.maxv_edit = self.findChild(QtWidgets.QLineEdit, 'pwrReqmaxVel_lineEdit')
        self.linecolor_combo = self.findChild(QtWidgets.QComboBox, 'pwrReqvsVel_linecolor_comboBox')
        self.lineweight_spin = self.findChild(QtWidgets.QSpinBox, 'pwrReqvsVel_lw_spinBox')
        self.export_checkbox = self.findChild(QtWidgets.QCheckBox, 'exportData_checkBox')
        self.button_box = self.findChild(QtWidgets.QDialogButtonBox, 'pwrReqvsVels_buttonBox')
        self.apply_button = self.button_box.button(QtWidgets.QDialogButtonBox.Apply)
        self.reject_button = self.button_box.button(QtWidgets.QDialogButtonBox.Cancel)
        
    def set_validators(self):
        self.minv_edit.setValidator(self.double_validator)
        self.maxv_edit.setValidator(self.double_validator)

    def adjust_line_color_property(self):
        self.linecolor_combo.addItems(COLORS.keys())
        self.linecolor_combo.setCurrentIndex(1)

    def apply(self):
        try:
            min_v = float(self.minv_edit.text())
            max_v = float(self.maxv_edit.text())
            
            ar = calc.aspect_ratio(self.wingspan, self.wing_area)
            oef = calc.oswald_efficiency_estimate(ar)
            k = calc.k_factor(ar, oef)
            cl = calc.lift_coefficient_range(min_v, max_v, self.weight, self.wing_area, self.rho)
            cd = calc.drag_coefficient(self.cd0, k, cl)
            
            power_req = calc.power_required_range(min_v, max_v, self.wing_area, self.rho, cd)

            if self.export_checkbox.isChecked():
                export.export_power_vs_velocity(power_req, np.arange(min_v, max_v, 0.1))
                self.show_message("DATA HAVE BEEN EXPORTED SUCCESSFULLY", 
                                "All data have been exported inside 'XLSX Workbooks' folder.")

            plotting.plot_power_req_vs_velocity(power_req, min_v, max_v, 0.1, 
                                              COLORS.get(self.linecolor_combo.currentText()), 
                                              int(self.lineweight_spin.value()), True)
        except ValueError:
             self.show_message("Error", "Invalid Input Parameters", QtWidgets.QMessageBox.Warning)


class DragvsVelocityDialog(BaseDialog):
    def __init__(self, weight, wing_area, wingspan, rho, cd0):
        super().__init__('dragvsVelDialog.ui')
        self.weight = weight
        self.wing_area = wing_area
        self.wingspan = wingspan
        self.rho = rho
        self.cd0 = cd0

        self.setFixedSize(300, 285)
        self.center()
        self.pull_children()
        self.set_validators()
        self.adjust_line_color_property()

        self.apply_button.clicked.connect(self.apply)
        self.reject_button.clicked.connect(self.close)

    def pull_children(self):
        self.minv_edit = self.findChild(QtWidgets.QLineEdit, 'dragminVel_lineEdit')
        self.maxv_edit = self.findChild(QtWidgets.QLineEdit, 'dragmaxVel_lineEdit')
        self.linecolor_combo = self.findChild(QtWidgets.QComboBox, 'dragvsVel_linecolor_comboBox')
        self.lineweight_spin = self.findChild(QtWidgets.QSpinBox, 'dragvsVel_lw_spinBox')
        self.export_checkbox = self.findChild(QtWidgets.QCheckBox, 'exportData_checkBox')
        self.button_box = self.findChild(QtWidgets.QDialogButtonBox, 'dragvsVels_buttonBox')
        self.apply_button = self.button_box.button(QtWidgets.QDialogButtonBox.Apply)
        self.reject_button = self.button_box.button(QtWidgets.QDialogButtonBox.Cancel)
        
    def set_validators(self):
        self.minv_edit.setValidator(self.double_validator)
        self.maxv_edit.setValidator(self.double_validator)

    def adjust_line_color_property(self):
        self.linecolor_combo.addItems(COLORS.keys())
        self.linecolor_combo.setCurrentIndex(1)

    def apply(self):
        try:
            min_v = float(self.minv_edit.text())
            max_v = float(self.maxv_edit.text())
            
            ar = calc.aspect_ratio(self.wingspan, self.wing_area)
            oef = calc.oswald_efficiency_estimate(ar)
            k = calc.k_factor(ar, oef)
            cl = calc.lift_coefficient_range(min_v, max_v, self.weight, self.wing_area, self.rho)
            cd = calc.drag_coefficient(self.cd0, k, cl)
            
            drag = calc.drag_range(min_v, max_v, self.wing_area, self.rho, cd)

            if self.export_checkbox.isChecked():
                export.export_drag_vs_velocity(drag, np.arange(min_v, max_v, 0.1))
                self.show_message("DATA HAVE BEEN EXPORTED SUCCESSFULLY", 
                                "All data have been exported inside 'XLSX Workbooks' folder.")

            plotting.plot_drag_vs_velocity(drag, min_v, max_v, 0.1, 
                                         COLORS.get(self.linecolor_combo.currentText()), 
                                         int(self.lineweight_spin.value()), True)
        except ValueError:
             self.show_message("Error", "Invalid Input Parameters", QtWidgets.QMessageBox.Warning)


class Lift2dragvsVelocityDialog(BaseDialog):
    def __init__(self, weight, wing_area, wingspan, rho, cd0):
        super().__init__('lift2dragvsVelDialog.ui')
        self.weight = weight
        self.wing_area = wing_area
        self.wingspan = wingspan
        self.rho = rho
        self.cd0 = cd0

        self.setFixedSize(300, 285)
        self.center()
        self.pull_children()
        self.set_validators()
        self.adjust_line_color_property()

        self.apply_button.clicked.connect(self.apply)
        self.reject_button.clicked.connect(self.close)

    def pull_children(self):
        self.minv_edit = self.findChild(QtWidgets.QLineEdit, 'lift2dragminVel_lineEdit')
        self.maxv_edit = self.findChild(QtWidgets.QLineEdit, 'lift2dragmaxVel_lineEdit')
        self.linecolor_combo = self.findChild(QtWidgets.QComboBox, 'lift2dragvsVel_linecolor_comboBox')
        self.lineweight_spin = self.findChild(QtWidgets.QSpinBox, 'lift2dragvsVel_lw_spinBox')
        self.export_checkbox = self.findChild(QtWidgets.QCheckBox, 'exportData_checkBox')
        self.button_box = self.findChild(QtWidgets.QDialogButtonBox, 'lift2dragvsVel_buttonBox')
        self.apply_button = self.button_box.button(QtWidgets.QDialogButtonBox.Apply)
        self.reject_button = self.button_box.button(QtWidgets.QDialogButtonBox.Cancel)
        
    def set_validators(self):
        self.minv_edit.setValidator(self.double_validator)
        self.maxv_edit.setValidator(self.double_validator)

    def adjust_line_color_property(self):
        self.linecolor_combo.addItems(COLORS.keys())
        self.linecolor_combo.setCurrentIndex(1)

    def apply(self):
        try:
            min_v = float(self.minv_edit.text())
            max_v = float(self.maxv_edit.text())
            
            ar = calc.aspect_ratio(self.wingspan, self.wing_area)
            oef = calc.oswald_efficiency_estimate(ar)
            k = calc.k_factor(ar, oef)
            cl = calc.lift_coefficient_range(min_v, max_v, self.weight, self.wing_area, self.rho)
            cd = calc.drag_coefficient(self.cd0, k, cl)
            # Recalculate CL for range (it was already calculated but logic seems weird in original)
            # In original code they calculated cl again: `cl = cl.liftcoefficient(...)` and used it.
            # Here I reused cl.
            ltod = cl / cd # Be careful of element-wise division and zeros, but numpy handles it (inf)

            if self.export_checkbox.isChecked():
                export.export_lift2drag_vs_velocity(ltod, np.arange(min_v, max_v, 0.1))
                self.show_message("DATA HAVE BEEN EXPORTED SUCCESSFULLY", 
                                "All data have been exported inside 'XLSX Workbooks' folder.")

            plotting.plot_lift2drag_vs_velocity(ltod, min_v, max_v, 0.1, 
                                              COLORS.get(self.linecolor_combo.currentText()), 
                                              int(self.lineweight_spin.value()), True)
        except ValueError:
             self.show_message("Error", "Invalid Input Parameters", QtWidgets.QMessageBox.Warning)


class AvailthrvsThrustReqDialog(BaseDialog):
    def __init__(self, weight, wing_area, wingspan, rho, cd0):
        super().__init__('avthrvsThrReqDialog.ui')
        self.weight = weight
        self.wing_area = wing_area
        self.wingspan = wingspan
        self.rho = rho
        self.cd0 = cd0

        self.setFixedSize(304, 325)
        self.center()
        self.pull_children()
        self.set_validators()
        self.adjust_line_color_property()

        self.apply_button.clicked.connect(self.apply)
        self.reject_button.clicked.connect(self.close)

    def pull_children(self):
        self.minv_edit = self.findChild(QtWidgets.QLineEdit, 'avthrminVel_lineEdit')
        self.maxv_edit = self.findChild(QtWidgets.QLineEdit, 'avthrmaxVel_lineEdit')
        self.first_linecolor_combo = self.findChild(QtWidgets.QComboBox, 'avthrvsThrReq_firstlinecolor_comboBox')
        self.second_linecolor_combo = self.findChild(QtWidgets.QComboBox, 'avthrvsThrReq_secondlinecolor_comboBox')
        self.lineweight_spin = self.findChild(QtWidgets.QSpinBox, 'avthrvsThrReq_lw_spinBox')
        self.button_box = self.findChild(QtWidgets.QDialogButtonBox, 'avthrvsThrReq_buttonBox')
        self.availablethr_edit = self.findChild(QtWidgets.QLineEdit, 'avthrvsThrReq_avthr_lineEdit')
        
        self.apply_button = self.button_box.button(QtWidgets.QDialogButtonBox.Apply)
        self.reject_button = self.button_box.button(QtWidgets.QDialogButtonBox.Cancel)
        
    def set_validators(self):
        self.minv_edit.setValidator(self.double_validator)
        self.maxv_edit.setValidator(self.double_validator)
        self.availablethr_edit.setValidator(self.double_validator)

    def adjust_line_color_property(self):
        self.first_linecolor_combo.addItems(COLORS.keys())
        self.first_linecolor_combo.setCurrentIndex(1)
        self.second_linecolor_combo.addItems(COLORS.keys())
        self.second_linecolor_combo.setCurrentIndex(2)

    def apply(self):
        try:
            min_v = float(self.minv_edit.text())
            max_v = float(self.maxv_edit.text())
            avail_thr = float(self.availablethr_edit.text())
            
            ar = calc.aspect_ratio(self.wingspan, self.wing_area)
            oef = calc.oswald_efficiency_estimate(ar)
            k = calc.k_factor(ar, oef)
            cl = calc.lift_coefficient_range(min_v, max_v, self.weight, self.wing_area, self.rho)
            cd = calc.drag_coefficient(self.cd0, k, cl)
            
            thrust_req = calc.thrust_required_range(min_v, max_v, self.wing_area, self.rho, cd)

            plotting.plot_thrust_avail_vs_req(avail_thr, thrust_req, min_v, max_v, 0.1, 
                                            COLORS.get(self.first_linecolor_combo.currentText()), 
                                            COLORS.get(self.second_linecolor_combo.currentText()), 
                                            int(self.lineweight_spin.value()), True)
        except ValueError:
             self.show_message("Error", "Invalid Input Parameters", QtWidgets.QMessageBox.Warning)
