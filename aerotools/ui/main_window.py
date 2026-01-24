import os
import webbrowser
import numpy as np
from PyQt5 import QtWidgets, QtGui, uic
from PyQt5.QtGui import QDoubleValidator

import aerotools.core.calculations as calc
from aerotools.ui.dialogs import (
    ClvsVelocityDialog, ThrustReqvsVelocityDialog, PowerReqvsVelocityDialog, 
    DragvsVelocityDialog, Lift2dragvsVelocityDialog, AvailthrvsThrustReqDialog,
    UI_DIR
)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        ui_path = os.path.join(UI_DIR, 'main.ui')
        uic.loadUi(ui_path, self)

        self.double_validator = QDoubleValidator()
        self.center()
        self.pull_children()
        self.set_validators()
        
        # Connect Signals
        self.memorize_btn.clicked.connect(self.memorize)
        self.compute_to_landing_btn.clicked.connect(self.compute_takeoff_landing)
        self.compute_thr_pwr_btn.clicked.connect(self.compute_thrust_power_req)
        
        self._create_menu()
        
        # Connect Graph Buttons
        if self.cl_btn: self.cl_btn.clicked.connect(self.show_cl_vs_vel_dialog)
        if self.thr_btn: self.thr_btn.clicked.connect(self.show_thr_req_vs_vel_dialog)
        if self.pwr_btn: self.pwr_btn.clicked.connect(self.show_pwr_req_vs_vel_dialog)
        if self.drag_btn: self.drag_btn.clicked.connect(self.show_drag_vs_vel_dialog)
        if self.ltod_btn: self.ltod_btn.clicked.connect(self.show_ltod_vs_vel_dialog)
        if self.avthr_btn: self.avthr_btn.clicked.connect(self.show_avthr_vs_thr_req_dialog)
        
        # Dialog references (to keep them alive)
        self.dialogs = {}

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def pull_children(self):
        # Inputs
        self.weight_edit = self.findChild(QtWidgets.QLineEdit, 'weight_lineEdit')
        self.wingspan_edit = self.findChild(QtWidgets.QLineEdit, 'wingspan_lineEdit')
        self.wingarea_edit = self.findChild(QtWidgets.QLineEdit, 'wingarea_lineEdit')
        self.rho_edit = self.findChild(QtWidgets.QLineEdit, 'rho_lineEdit')
        self.cd0_edit = self.findChild(QtWidgets.QLineEdit, 'cd0_lineEdit')
        self.avthr_edit = self.findChild(QtWidgets.QLineEdit, 'avthrust_lineEdit')
        self.rfc_spin = self.findChild(QtWidgets.QDoubleSpinBox, 'rollingFriction_doubleSpinBox')
        self.thr_pwr_vel_edit = self.findChild(QtWidgets.QLineEdit, 'thrustPowerReqVel_lineEdit')
        
        self.oef_spin = self.findChild(QtWidgets.QDoubleSpinBox, 'oswalden_doubleSpinBox')
        self.maxcl_spin = self.findChild(QtWidgets.QDoubleSpinBox, 'maxcl_doubleSpinBox')
        
        
        # Inputs list for enabling/disabling
        self.input_fields = [
            self.weight_edit, self.wingspan_edit, self.wingarea_edit, 
            self.rho_edit, self.cd0_edit, self.oef_spin, self.rfc_spin,
            self.avthr_edit, self.thr_pwr_vel_edit
        ]
        
        # Outputs
        self.to_dist_edit = self.findChild(QtWidgets.QLabel, 'toDistance_EditLabel')
        self.to_speed_edit = self.findChild(QtWidgets.QLabel, 'toSpeed_EditLabel')
        self.landing_dist_edit = self.findChild(QtWidgets.QLabel, 'landingDistance_EditLabel')
        self.landing_speed_edit = self.findChild(QtWidgets.QLabel, 'landingSpeed_EditLabel')
        self.thr_req_edit = self.findChild(QtWidgets.QLabel, 'thrustReq_EditLabel')
        self.pwr_req_edit = self.findChild(QtWidgets.QLabel, 'powerReq_EditLabel')
        self.wl_edit = self.findChild(QtWidgets.QLabel, 'wingLoading_EditLabel')
        self.ar_edit = self.findChild(QtWidgets.QLabel, 'aspectRatio_EditLabel')
        
        # Buttons
        self.memorize_btn = self.findChild(QtWidgets.QPushButton, 'memorize_pushButton')
        self.compute_to_landing_btn = self.findChild(QtWidgets.QPushButton, 'toLandingDataCalculate_pushButton')
        self.compute_thr_pwr_btn = self.findChild(QtWidgets.QPushButton, 'thrustPowerReqVelCalc_pushButton')
        
        # Graph Buttons
        self.cl_btn = self.findChild(QtWidgets.QPushButton, 'clvsvel_button')
        self.thr_btn = self.findChild(QtWidgets.QPushButton, 'thrvsvel_button')
        self.pwr_btn = self.findChild(QtWidgets.QPushButton, 'powvsvel_button')
        self.drag_btn = self.findChild(QtWidgets.QPushButton, 'dragvsvel_button')
        self.ltod_btn = self.findChild(QtWidgets.QPushButton, 'ltodvsvel_button')
        self.avthr_btn = self.findChild(QtWidgets.QPushButton, 'thravvsthrreq_button')
        
        # Status Bar
        try:
            self.stat_bar = self.findChild(QtWidgets.QStatusBar, 'statusbar')
            if not self.stat_bar:
                self.stat_bar = self.findChild(QtWidgets.QStatusBar, 'statBar')
            if not self.stat_bar:
                # self.stat_bar = self.statusBar() # This seems to crash
                self.stat_bar = None
        except:
            self.stat_bar = None

    def set_validators(self):
        for widget in [self.weight_edit, self.wingspan_edit, self.wingarea_edit, 
                       self.rho_edit, self.cd0_edit, self.avthr_edit, 
                       self.thr_pwr_vel_edit]:
            widget.setValidator(self.double_validator)

    def _create_menu(self):
        menubar = self.menuBar()
        menubar.setStyleSheet("QMenuBar {font: 11pt Ubuntu}")
        credit_menu = menubar.addMenu("Credits")

        credit_github = QtWidgets.QAction(QtGui.QIcon('icons/githubicon.png'), "Github: @umutaktepe", self)
        credit_linkedin = QtWidgets.QAction(QtGui.QIcon("icons/linkedinicon.png"), "LinkedIn: @umutaktepe", self)
        credit_instagram = QtWidgets.QAction(QtGui.QIcon("icons/instagramicon.png"), "Instagram: @umut.space", self)

        credit_menu.addAction(credit_github)
        credit_menu.addSeparator()
        credit_menu.addAction(credit_linkedin)
        credit_menu.addAction(credit_instagram)

        credit_github.triggered.connect(self.visit_github)
        credit_linkedin.triggered.connect(self.visit_linkedin)
        credit_instagram.triggered.connect(self.visit_instagram)

    def show_error(self, message):
         QtWidgets.QMessageBox.warning(self, "Input Error", message)

    def memorize(self):
        if self.memorize_btn.text() == "MEMORIZE":
            try:
                # Basic validation that inputs are numbers
                float(self.weight_edit.text())
                float(self.wingarea_edit.text())
                float(self.rho_edit.text())
                # ... check others if strictly required for *any* operation
                
                self.memorize_btn.setStyleSheet(
                    "QPushButton {font-weight: bold; font-size: 10pt; border-style: outset; border-width: 4px; border-radius: 6px; background-color: springgreen; border-color: green}"
                    "QPushButton:pressed {font-weight: bold; font-size: 9pt; border-style: inset; border-width: 3px; background-color: lavenderblush; border-color: red;}")
                self.memorize_btn.setText("UNMEMORIZE")
                if self.stat_bar:
                    self.stat_bar.showMessage("Data have been memorized. All set for other tools. ")
                
                for field in self.input_fields:
                    field.setDisabled(True)
            except ValueError:
                self.show_error("Please enter valid numeric data before memorizing.")
                
        else: # UNMEMORIZE
            self.memorize_btn.setStyleSheet(
                "QPushButton {font-weight: bold; font-size: 10pt; border-style: outset; border-width: 4px; border-radius: 6px; background-color: lavenderblush; border-color: darkslateblue}"
                "QPushButton:pressed {font-weight: bold; font-size: 9pt; border-style: inset; border-width: 3px; background-color: lavenderblush; border-color: green;}")
            self.memorize_btn.setText("MEMORIZE")
            if self.stat_bar:
                self.stat_bar.showMessage("Data have been erased. Enter data to operate...")
            
            for field in self.input_fields:
                field.setEnabled(True)
            
            # Clear outputs (optional, matching original behavior somewhat reset)
            # Keeping it simple for now or copying original '________ m' style if preferred.
            
    def compute_takeoff_landing(self):
        try:
            w = float(self.weight_edit.text())
            ws = float(self.wingspan_edit.text())
            wa = float(self.wingarea_edit.text())
            rho = float(self.rho_edit.text())
            cd0 = float(self.cd0_edit.text())
            rfc = self.rfc_spin.value()
            avthr = float(self.avthr_edit.text())
            max_cl = self.maxcl_spin.value()
            oef = self.oef_spin.value()
            
            to_dist = calc.takeoff_distance(w, ws, wa, rho, cd0, rfc, avthr, max_cl, oef)
            to_speed = calc.takeoff_speed(w, wa, rho, max_cl)
            ldg_dist = calc.landing_distance(w, ws, wa, rho, cd0, rfc, max_cl)
            ldg_speed = calc.landing_speed(w, wa, rho, max_cl)
            
            self.compute_wl_ar()
            
            self.to_dist_edit.setText(f"<html><head/><body><p><span style=\" font-size:14pt; color:#3465a4;\">{to_dist:.1f} m</span></p></body></html>")
            self.to_speed_edit.setText(f"<html><head/><body><p><span style=\" font-size:14pt; color:#3465a4;\">{to_speed:.1f} m/s</span></p></body></html>")
            self.landing_dist_edit.setText(f"<html><head/><body><p><span style=\" font-size:14pt; color:#3465a4;\">{ldg_dist:.1f} m</span></p></body></html>")
            self.landing_speed_edit.setText(f"<html><head/><body><p><span style=\" font-size:14pt; color:#3465a4;\">{ldg_speed:.1f} m/s</span></p></body></html>")

        except ValueError:
            self.show_error("Invalid Input Values")
        except ZeroDivisionError:
            self.show_error("Division by Zero Error")

    def compute_thrust_power_req(self):
        try:
            v_input = float(self.thr_pwr_vel_edit.text())
            w = float(self.weight_edit.text())
            ws = float(self.wingspan_edit.text())
            wa = float(self.wingarea_edit.text())
            rho = float(self.rho_edit.text())
            cd0 = float(self.cd0_edit.text())
            oef = self.oef_spin.value()
            
            ar = calc.aspect_ratio(ws, wa)
            k = calc.k_factor(ar, oef)
            cl = calc.lift_coefficient_at_v(v_input, w, wa, rho)
            cd = calc.drag_coefficient(cd0, k, cl)
            
            thr_req = calc.thrust_required_at_v(v_input, wa, rho, cd)
            pwr_req = calc.power_required_at_v(v_input, wa, rho, cd)
            
            self.thr_req_edit.setText(f"<html><head/><body><p><span style=\" font-size:14pt; color:#3465a4;\">{thr_req:.1f} N</span></p></body></html>")
            self.pwr_req_edit.setText(f"<html><head/><body><p><span style=\" font-size:14pt; color:#3465a4;\">{pwr_req:.1f} W</span></p></body></html>")
            
        except ValueError:
            self.show_error("Invalid Input Values")
        except ZeroDivisionError:
            self.show_error("Division by Zero Error")

    def compute_wl_ar(self):
        try:
            w = float(self.weight_edit.text())
            ws = float(self.wingspan_edit.text())
            wa = float(self.wingarea_edit.text())
            
            wl = calc.wing_loading(w, wa)
            ar = calc.aspect_ratio(ws, wa)
            
            self.wl_edit.setText(f"<html><head/><body><p><span style=\" font-size:14pt; color:#3465a4;\">{wl:.1f} kg/m<span style=\" font-size:14pt; color:#3465a4; vertical-align:super;\">2</span></span></p></body></html>")
            self.ar_edit.setText(f"<html><head/><body><p><span style=\" font-size:14pt; color:#3465a4;\">{ar:.1f} : 1</span></p></body></html>")
            
        except ValueError:
             self.show_error("Invalid Input Values")
        except ZeroDivisionError:
             self.show_error("Division by Zero Error")

    # Dialog Functions
    def _check_memorized(self):
        if self.memorize_btn.text() != "UNMEMORIZE":
             self.show_error("Please MEMORIZE data first.")
             return False
        return True
        
    def show_cl_vs_vel_dialog(self):
        if self._check_memorized():
            self.dialogs['cl'] = ClvsVelocityDialog(float(self.weight_edit.text()), float(self.wingarea_edit.text()), float(self.rho_edit.text()))
            self.dialogs['cl'].show()

    def show_thr_req_vs_vel_dialog(self):
        if self._check_memorized():
            self.dialogs['thr'] = ThrustReqvsVelocityDialog(float(self.weight_edit.text()), float(self.wingarea_edit.text()), float(self.wingspan_edit.text()), float(self.rho_edit.text()), float(self.cd0_edit.text()))
            self.dialogs['thr'].show()

    def show_pwr_req_vs_vel_dialog(self):
        if self._check_memorized():
            self.dialogs['pwr'] = PowerReqvsVelocityDialog(float(self.weight_edit.text()), float(self.wingarea_edit.text()), float(self.wingspan_edit.text()), float(self.rho_edit.text()), float(self.cd0_edit.text()))
            self.dialogs['pwr'].show()

    def show_drag_vs_vel_dialog(self):
        if self._check_memorized():
            self.dialogs['drag'] = DragvsVelocityDialog(float(self.weight_edit.text()), float(self.wingarea_edit.text()), float(self.wingspan_edit.text()), float(self.rho_edit.text()), float(self.cd0_edit.text()))
            self.dialogs['drag'].show()

    def show_ltod_vs_vel_dialog(self):
        if self._check_memorized():
            self.dialogs['ltod'] = Lift2dragvsVelocityDialog(float(self.weight_edit.text()), float(self.wingarea_edit.text()), float(self.wingspan_edit.text()), float(self.rho_edit.text()), float(self.cd0_edit.text()))
            self.dialogs['ltod'].show()

    def show_avthr_vs_thr_req_dialog(self):
        if self._check_memorized():
             self.dialogs['avthr'] = AvailthrvsThrustReqDialog(float(self.weight_edit.text()), float(self.wingarea_edit.text()), float(self.wingspan_edit.text()), float(self.rho_edit.text()), float(self.cd0_edit.text()))
             self.dialogs['avthr'].show()

    def visit_github(self):
        webbrowser.open("https://github.com/umutaktepe?tab=repositories")

    def visit_linkedin(self):
        webbrowser.open("https://www.linkedin.com/in/umutaktepe")

    def visit_instagram(self):
        webbrowser.open("https://www.instagram.com/umut.space/")
