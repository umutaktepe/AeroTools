#!/usr/bin/python3

from PyQt5 import QtWidgets, QtGui
from PyQt5 import uic
import numpy as np
import webbrowser
import sys
from modules.aerographs import Plot as agplot
from modules.aerocalculate import Calculate as acalculate
from modules.aeroexport import Export as aeroexport

double_validator = QtGui.QDoubleValidator()
colors = {'Black': 'k', 'Blue': 'b', 'Red': 'r', 'Green': 'g'}


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):

        super(MainWindow, self).__init__()
        uic.loadUi('modules/ui/main.ui', self)

        self.center()
        self.pullChildren()
        self.setValidators()
        self.setFixedSize(1100, 620)

        self.statBar = QtWidgets.QStatusBar()
        self.statBar.setStyleSheet("QStatusBar {color: dimgray; font: italic 14px}")
        self.setStatusBar(self.statBar)
        self.statBar.showMessage("Ready to operate...")

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

        memorize.clicked.connect(self.memorize)
        toLand_calculate.clicked.connect(self.toandLandingData_compute)
        thrustpowerReq_calculate.clicked.connect(self.thrustpowerReq_compute)

        credit_github.triggered.connect(self.visitGithub)
        credit_linkedin.triggered.connect(self.visitLinkedin)
        credit_instagram.triggered.connect(self.visitInstagram)

        clvsVel_button.clicked.connect(self.showClvsVelDialog)
        thrvsVel_button.clicked.connect(self.showThrReqvsVelDialog)
        powvsVel_button.clicked.connect(self.showPwrReqvsVelDialog)
        dragvsVel_button.clicked.connect(self.showDragvsVelDialog)
        ltodvsVel_button.clicked.connect(self.showLtodvsVelDialog)
        travvsThrReq_button.clicked.connect(self.showAvthrvsThrReqDialog)

    def center(self):

        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()

        qr.moveCenter(cp)

        self.move(qr.topLeft())

    def pullChildren(self):

        global weight, wingspan, wingarea, rho, cd0, oef_db, memorize, rfc, maxcl_db, avthr, toLand_calculate
        global toDist_edit, toSpeed_edit, landingDist_edit, landingSpeed_edit, thrustpowerReq_vel
        global thrustpowerReq_calculate, thrustReq_edit, powerReq_edit, wingLoading_edit, aspectRatio_edit
        global clvsVel_button, thrvsVel_button, powvsVel_button, dragvsVel_button, ltodvsVel_button, travvsThrReq_button

        #####################
        # Input lines start #

        weight = self.findChild(QtWidgets.QLineEdit, 'weight_lineEdit')
        wingspan = self.findChild(QtWidgets.QLineEdit, 'wingspan_lineEdit')
        wingarea = self.findChild(QtWidgets.QLineEdit, 'wingarea_lineEdit')
        rho = self.findChild(QtWidgets.QLineEdit, 'rho_lineEdit')
        cd0 = self.findChild(QtWidgets.QLineEdit, 'cd0_lineEdit')
        oef_db = self.findChild(QtWidgets.QDoubleSpinBox, 'oswalden_doubleSpinBox')
        memorize = self.findChild(QtWidgets.QPushButton, 'memorize_pushButton')
        rfc = self.findChild(QtWidgets.QDoubleSpinBox, 'rollingFriction_doubleSpinBox')
        maxcl_db = self.findChild(QtWidgets.QDoubleSpinBox, 'maxcl_doubleSpinBox')
        avthr = self.findChild(QtWidgets.QLineEdit, 'avthrust_lineEdit')
        toLand_calculate = self.findChild(QtWidgets.QPushButton, 'toLandingDataCalculate_pushButton')
        toDist_edit = self.findChild(QtWidgets.QLabel, 'toDistance_EditLabel')
        toSpeed_edit = self.findChild(QtWidgets.QLabel, 'toSpeed_EditLabel')
        landingDist_edit = self.findChild(QtWidgets.QLabel, 'landingDistance_EditLabel')
        landingSpeed_edit = self.findChild(QtWidgets.QLabel, 'landingSpeed_EditLabel')
        thrustpowerReq_vel = self.findChild(QtWidgets.QLineEdit, 'thrustPowerReqVel_lineEdit')
        thrustpowerReq_calculate = self.findChild(QtWidgets.QPushButton, 'thrustPowerReqVelCalc_pushButton')
        thrustReq_edit = self.findChild(QtWidgets.QLabel, 'thrustReq_EditLabel')
        powerReq_edit = self.findChild(QtWidgets.QLabel, 'powerReq_EditLabel')
        wingLoading_edit = self.findChild(QtWidgets.QLabel, 'wingLoading_EditLabel')
        aspectRatio_edit = self.findChild(QtWidgets.QLabel, 'aspectRatio_EditLabel')

        # Input lines end #
        ###################

        ####################################
        # Performance Graphs Buttons start #

        clvsVel_button = self.findChild(QtWidgets.QPushButton, 'clvsvel_button')
        thrvsVel_button = self.findChild(QtWidgets.QPushButton, 'thrvsvel_button')
        powvsVel_button = self.findChild(QtWidgets.QPushButton, 'powvsvel_button')
        dragvsVel_button = self.findChild(QtWidgets.QPushButton, 'dragvsvel_button')
        ltodvsVel_button = self.findChild(QtWidgets.QPushButton, 'ltodvsvel_button')
        travvsThrReq_button = self.findChild(QtWidgets.QPushButton, 'thravvsthrreq_button')

        # Performance Graphs Buttons end #
        ##################################

    @staticmethod
    def setValidators():

        weight.setValidator(double_validator)
        wingspan.setValidator(double_validator)
        wingarea.setValidator(double_validator)
        rho.setValidator(double_validator)
        cd0.setValidator(double_validator)
        avthr.setValidator(double_validator)
        thrustpowerReq_vel.setValidator(double_validator)

    @staticmethod
    def showValueError():

        errmsg = QtWidgets.QMessageBox()
        errmsg.setIcon(QtWidgets.QMessageBox.Critical)
        errmsg.setText("Input section cannot be empty or zero value. Please check the inputs.")
        errmsg.setWindowTitle("INPUT ERROR")
        errmsg.setStyleSheet("QMessageBox {font: 12pt Ubuntu}")
        button = errmsg.addButton(QtWidgets.QMessageBox.Ok)
        button.setIcon(QtGui.QIcon("icons/check.png"))
        button.setFixedSize(75, 35)
        button.setStyleSheet("QPushButton {font: 10pt Ubuntu}")
        errmsg.setDefaultButton(button)

        return errmsg.exec_()

    @staticmethod
    def showZeroDivisionError():

        errmsg = QtWidgets.QMessageBox()
        errmsg.setIcon(QtWidgets.QMessageBox.Critical)
        errmsg.setText("Some inputs are causing zero division problem. Please make sure you have non-zero inputs.")
        errmsg.setWindowTitle("ZERO DIVISION ERROR")
        errmsg.setStyleSheet("QMessageBox {font: 12pt Ubuntu}")
        button = errmsg.addButton(QtWidgets.QMessageBox.Ok)
        button.setIcon(QtGui.QIcon("icons/check.png"))
        button.setFixedSize(75, 35)
        button.setStyleSheet("QPushButton {font: 10pt Ubuntu}")
        errmsg.setDefaultButton(button)

        return errmsg.exec_()

    @staticmethod
    def showNameError():

        name_errmsg = QtWidgets.QMessageBox()
        name_errmsg.setIcon(QtWidgets.QMessageBox.Critical)
        name_errmsg.setText("You cannot reach plotting functions before the inputs have been memorized.")
        name_errmsg.setWindowTitle("MEMORIZING ERROR")
        name_errmsg.setStyleSheet("QMessageBox {font: 12pt Ubuntu}")
        button = name_errmsg.addButton(QtWidgets.QMessageBox.Ok)
        button.setIcon(QtGui.QIcon("icons/check.png"))
        button.setFixedSize(75, 35)
        button.setStyleSheet("QPushButton {font: 10pt Ubuntu}")
        name_errmsg.setDefaultButton(button)

        return name_errmsg.exec_()

    def memorize(self):

        global input_list, clinterface, thrReqVelinterface, pwrReqVelinterface, dragVelinterface, lift2dragVelinterface, avthrThrReqinterface

        try:
            self.wingLoadingandAr()

            clinterface = ClvsVelocityDialog(c_weight=float(weight.text()), c_wingarea=float(wingarea.text()), c_rho=float(rho.text()))
            thrReqVelinterface = ThrustReqvsVelocityDialog(t_weight=float(weight.text()), t_wingarea=float(wingarea.text()), t_rho=float(rho.text()), t_cd0=float(cd0.text()), t_wingspan=float(wingspan.text()))
            pwrReqVelinterface = PowerReqvsVelocityDialog(p_weight=float(weight.text()), p_wingarea=float(wingarea.text()), p_rho=float(rho.text()), p_cd0=float(cd0.text()), p_wingspan=float(wingspan.text()))
            dragVelinterface = DragvsVelocity(d_weight=float(weight.text()), d_wingarea=float(wingarea.text()), d_rho=float(rho.text()), d_cd0=float(cd0.text()), d_wingspan=float(wingspan.text()))
            lift2dragVelinterface = Lift2dragvsVelocityDialog(ltod_weight=float(weight.text()), ltod_wingarea=float(wingarea.text()), ltod_rho=float(rho.text()), ltod_cd0=float(cd0.text()), ltod_wingspan=float(wingspan.text()))
            avthrThrReqinterface = AvailthrvsThrustReqDialog(avthr_weight=float(weight.text()), avthr_wingarea=float(wingarea.text()), avthr_rho=float(rho.text()), avthr_cd0=float(cd0.text()), avthr_wingspan=float(wingspan.text()))

            memorize.setStyleSheet(
                "QPushButton {font-weight: bold; font-size: 10pt; border-style: outset; border-width: 4px; border-radius: 6px; background-color: springgreen; border-color: green}"
                "QPushButton:pressed {font-weight: bold; font-size: 9pt; border-style: inset; border-width: 3px; background-color: lavenderblush; border-color: red;}")
            memorize.setText("UNMEMORIZE")
            self.statBar.showMessage("Data have been memorized. All set for other tools. ")

            input_list = [weight, wingspan, wingarea, rho, cd0, oef_db]

            for i in input_list:
                i.setDisabled(True)

            memorize.clicked.connect(self.unmemorize)

        except (ValueError, ZeroDivisionError) as error:
            if len(error.args) > 0 and error.args[0] == 'could not convert string to float: ':
                self.showValueError()
            else:
                self.showZeroDivisionError()

    def unmemorize(self):

        memorize.setStyleSheet(
            "QPushButton {font-weight: bold; font-size: 10pt; border-style: outset; border-width: 4px; border-radius: 6px; background-color: lavenderblush; border-color: darkslateblue}"
            "QPushButton:pressed {font-weight: bold; font-size: 9pt; border-style: inset; border-width: 3px; background-color: lavenderblush; border-color: green;}")
        memorize.setText("MEMORIZE")
        self.statBar.showMessage("Data have been erased. Enter data to operate...")

        for i in input_list:
            i.setEnabled(True)

        toDist_edit.setText("""
                                                <html> 
                                                <head/> 
                                                <body> 
                                                <p><span style=" font-size:14pt; color:#3465a4;">________ m</span></p>
                                                </body> 
                                                </html>""")

        toSpeed_edit.setText("""
                                        <html> 
                                        <head/> 
                                        <body> 
                                        <p><span style=" font-size:14pt; color:#3465a4;">________ m/s</span></p>
                                        </body> 
                                        </html>""")

        landingDist_edit.setText("""
                                        <html> 
                                        <head/> 
                                        <body> 
                                        <p><span style=" font-size:14pt; color:#3465a4;">________ m</span></p>
                                        </body> 
                                        </html>""")

        landingSpeed_edit.setText("""
                                        <html> 
                                        <head/> 
                                        <body> 
                                        <p><span style=" font-size:14pt; color:#3465a4;">________ m/s</span></p>
                                        </body> 
                                        </html>""")

        thrustReq_edit.setText("""
                                                <html> 
                                                <head/> 
                                                <body> 
                                                <p><span style=" font-size:14pt; color:#3465a4;">________ N</span></p>
                                                </body> 
                                                </html>""")

        powerReq_edit.setText("""
                                                <html> 
                                                <head/> 
                                                <body> 
                                                <p><span style=" font-size:14pt; color:#3465a4;">________ W</span></p>
                                                </body> 
                                                </html>""")

        memorize.clicked.connect(self.memorize)

    def toandLandingData_compute(self):

        try:
            todistance = acalculate()
            todistance = todistance.takeoffDistance(weight=float(weight.text()), wingspan=float(wingspan.text()), wingarea=float(wingarea.text()), rho=float(rho.text()), cd0=float(cd0.text()), rfriction_coef=float(rfc.text()), availthrust=float(avthr.text()), max_cl=float(maxcl_db.value()), oef=float(oef_db.value()))
            toDist_edit.setText("""
                            <html> 
                            <head/> 
                            <body> 
                            <p><span style=" font-size:14pt; color:#3465a4;">{0:.1f} m</span></p>
                            </body> 
                            </html>""".format(todistance))

            tospeed = acalculate()
            tospeed = tospeed.takeoffSpeed(weight=float(weight.text()), wingarea=float(wingarea.text()), rho=float(rho.text()), max_cl=float(maxcl_db.value()))
            toSpeed_edit.setText("""
                            <html> 
                            <head/> 
                            <body> 
                            <p><span style=" font-size:14pt; color:#3465a4;">{0:.1f} m/s</span></p>
                            </body> 
                            </html>""".format(tospeed))

            landingdistance = acalculate()
            landingdistance = landingdistance.landingDistance(weight=float(weight.text()), wingspan=float(wingspan.text()), wingarea=float(wingarea.text()), rho=float(rho.text()), cd0=float(cd0.text()), rfriction_coef=float(rfc.text()), max_cl=float(maxcl_db.value()))
            landingDist_edit.setText("""
                            <html> 
                            <head/> 
                            <body> 
                            <p><span style=" font-size:14pt; color:#3465a4;">{0:.1f} m</span></p>
                            </body> 
                            </html>""".format(landingdistance))

            landingspeed = acalculate()
            landingspeed = landingspeed.landingSpeed(weight=float(weight.text()), wingarea=float(wingarea.text()), rho=float(rho.text()), max_cl=float(maxcl_db.value()))
            landingSpeed_edit.setText("""
                            <html> 
                            <head/> 
                            <body> 
                            <p><span style=" font-size:14pt; color:#3465a4;">{0:.1f} m/s</span></p>
                            </body> 
                            </html>""".format(landingspeed))

        except (ValueError, ZeroDivisionError) as error:
            if len(error.args) > 0 and error.args[0] == 'could not convert string to float: ':
                self.showValueError()
            else:
                self.showZeroDivisionError()

    def thrustpowerReq_compute(self):

        try:
            thrReq = acalculate()
            cd = acalculate()
            k = acalculate()
            k = k.kFactor(wingspan=float(wingspan.text()), wingarea=float(wingarea.text()), oef=float(oef_db.value()))
            cl = acalculate()
            cl = cl.liftcoefficient_C(v=float(thrustpowerReq_vel.text()), weight=float(weight.text()), wingarea=float(wingarea.text()), rho=float(rho.text()))
            cd = cd.dragcoefficient(cd0=float(cd0.text()), k=k, cl= cl)
            thrReq = thrReq.thrustReq_C(v=float(thrustpowerReq_vel.text()), wingarea=float(wingarea.text()), rho=float(rho.text()), cd=cd)
            thrustReq_edit.setText("""
                            <html> 
                            <head/> 
                            <body> 
                            <p><span style=" font-size:14pt; color:#3465a4;">{0:.1f} N</span></p>
                            </body> 
                            </html>""".format(thrReq))

            powReq = acalculate()
            powReq = powReq.powerReq_C(v=float(thrustpowerReq_vel.text()), wingarea=float(wingarea.text()), rho=float(rho.text()), cd=cd)
            powerReq_edit.setText("""
                            <html> 
                            <head/> 
                            <body> 
                            <p><span style=" font-size:14pt; color:#3465a4;">{0:.1f} W</span></p>
                            </body> 
                            </html>""".format(powReq))

        except (ValueError, ZeroDivisionError) as error:
            if len(error.args) > 0 and error.args[0] == 'could not convert string to float: ':
                self.showValueError()
            else:
                self.showZeroDivisionError()

    @staticmethod
    def wingLoadingandAr():

        wl = acalculate()
        wl = wl.wingLoading(weight=float(weight.text()), wingarea=float(wingarea.text()))
        wingLoading_edit.setText("""
                        <html>
                        <head/>
                        <body>
                        <p><span style=" font-size:14pt; color:#3465a4;">{0:.1f} kg/m</span>
                        <span style=" font-size:14pt; color:#3465a4; vertical-align:super;">2</span></p>
                        </body>
                        </html>""".format(wl))

        ar = acalculate()
        ar = ar.aspectRatio(wingspan=float(wingspan.text()), wingarea=float(wingarea.text()))
        aspectRatio_edit.setText("""
                        <html> 
                        <head/> 
                        <body> 
                        <p><span style=" font-size:14pt; color:#3465a4;">{0:.1f} : 1</span></p>
                        </body> 
                        </html>""".format(ar))

    def showClvsVelDialog(self):

        try:
            clinterface.show()
        except NameError:
            self.showNameError()

    def showThrReqvsVelDialog(self):

        try:
            thrReqVelinterface.show()
        except NameError:
            self.showNameError()

    def showPwrReqvsVelDialog(self):

        try:
            pwrReqVelinterface.show()
        except NameError:
            self.showNameError()

    def showDragvsVelDialog(self):

        try:
            dragVelinterface.show()
        except NameError:
            self.showNameError()

    def showLtodvsVelDialog(self):

        try:
            lift2dragVelinterface.show()
        except NameError:
            self.showNameError()

    def showAvthrvsThrReqDialog(self):

        try:
            avthrThrReqinterface.show()
        except NameError:
            self.showNameError()

    @staticmethod
    def visitGithub():
        webbrowser.open("https://github.com/umutaktepe?tab=repositories")

    @staticmethod
    def visitLinkedin():
        webbrowser.open("https://www.linkedin.com/in/umutaktepe")

    @staticmethod
    def visitInstagram():
        webbrowser.open("https://www.instagram.com/umut.space/")


class ClvsVelocityDialog(QtWidgets.QDialog):

    def __init__(self, c_weight, c_wingarea, c_rho):
        super(ClvsVelocityDialog, self).__init__()
        uic.loadUi('modules/ui/clvsVelDialog.ui', self)

        self.weight = c_weight
        self.wingarea = c_wingarea
        self.rho = c_rho

        self.setFixedSize(300, 285)

        self.center()
        self.pullChildren()
        self.setValidators()
        self.adjustLineColorProperty()

        applybutton = cl_dialogbuttons.button(QtWidgets.QDialogButtonBox.Apply)
        rejectbutton = cl_dialogbuttons.button(QtWidgets.QDialogButtonBox.Cancel)

        applybutton.clicked.connect(self.apply)
        rejectbutton.clicked.connect(self.close)

    def center(self):

        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()

        qr.moveCenter(cp)

        self.move(qr.topLeft())

    def pullChildren(self):

        global cl_minv_edit, cl_maxv_edit, cl_linecolor_combo, cl_lineweight_spin, cl_exportdata_checkbox, cl_dialogbuttons

        cl_minv_edit = self.findChild(QtWidgets.QLineEdit, 'clminVel_lineEdit')
        cl_maxv_edit = self.findChild(QtWidgets.QLineEdit, 'clmaxVel_lineEdit')
        cl_linecolor_combo = self.findChild(QtWidgets.QComboBox, 'clvsVel_linecolor_comboBox')
        cl_lineweight_spin = self.findChild(QtWidgets.QSpinBox, 'clvsVel_lw_spinBox')
        cl_exportdata_checkbox = self.findChild(QtWidgets.QCheckBox, 'exportData_checkBox')
        cl_dialogbuttons = self.findChild(QtWidgets.QDialogButtonBox, 'clvsVels_buttonBox')

    @staticmethod
    def setValidators():

        cl_minv_edit.setValidator(double_validator)
        cl_maxv_edit.setValidator(double_validator)

    @staticmethod
    def adjustLineColorProperty():

        cl_linecolor_combo.addItems(colors.keys())

    def apply(self):

        cl = acalculate()
        cl = cl.liftcoefficient(float(cl_minv_edit.text()), float(cl_maxv_edit.text()), self.weight, self.wingarea, self.rho)

        if cl_exportdata_checkbox.isChecked():
            cl_export_xlsx = aeroexport()
            cl_export_xlsx.clvsVelocity(cl, np.arange(float(cl_minv_edit.text()), float(cl_maxv_edit.text()), 0.1))

            cl_info_msg = QtWidgets.QMessageBox()
            cl_info_msg.setIcon(QtWidgets.QMessageBox.Information)
            cl_info_msg.setText("All data have been exported inside 'XLSX Workbooks' folder.")
            cl_info_msg.setWindowTitle("DATA HAVE BEEN EXPORTED SUCCESSFULLY")
            cl_info_msg.setStyleSheet("QMessageBox {font: 12pt Ubuntu}")
            cl_button = cl_info_msg.addButton(QtWidgets.QMessageBox.Ok)
            cl_button.setIcon(QtGui.QIcon("icons/check.png"))
            cl_button.setFixedSize(75, 35)
            cl_button.setStyleSheet("QPushButton {font: 10pt Ubuntu}")
            cl_info_msg.setDefaultButton(cl_button)
            cl_info_msg.exec_()
        else:
            pass

        plotcl_velocity = agplot()
        plotcl_velocity.clvsvelocity(cl, float(cl_minv_edit.text()), float(cl_maxv_edit.text()), 0.1, colors.get(cl_linecolor_combo.currentText()), int(cl_lineweight_spin.value()), True)

        cl_minv_edit.clear()
        cl_maxv_edit.clear()
        self.close()


class ThrustReqvsVelocityDialog(QtWidgets.QDialog):

    def __init__(self, t_weight, t_wingarea, t_wingspan, t_rho, t_cd0):
        super(ThrustReqvsVelocityDialog, self).__init__()
        uic.loadUi('modules/ui/thrReqvsVelDialog.ui', self)

        self.weight = t_weight
        self.wingarea = t_wingarea
        self.wingspan = t_wingspan
        self.rho = t_rho
        self.cd0 = t_cd0

        self.setFixedSize(300, 285)

        self.center()
        self.pullChildren()
        self.setValidators()
        self.adjustLineColorProperty()

        applybutton = thr_dialogbuttons.button(QtWidgets.QDialogButtonBox.Apply)
        rejectbutton = thr_dialogbuttons.button(QtWidgets.QDialogButtonBox.Cancel)

        applybutton.clicked.connect(self.apply)
        rejectbutton.clicked.connect(self.close)

    def center(self):

        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()

        qr.moveCenter(cp)

        self.move(qr.topLeft())

    def pullChildren(self):

        global thr_minv_edit, thr_maxv_edit, thr_linecolor_combo, thr_lineweight_spin, thr_exportdata_checkbox, thr_dialogbuttons

        thr_minv_edit = self.findChild(QtWidgets.QLineEdit, 'thrReqminVel_lineEdit')
        thr_maxv_edit = self.findChild(QtWidgets.QLineEdit, 'thrReqmaxVel_lineEdit')
        thr_linecolor_combo = self.findChild(QtWidgets.QComboBox, 'thrReqvsVel_linecolor_comboBox')
        thr_lineweight_spin = self.findChild(QtWidgets.QSpinBox, 'thrReqvsVel_lw_spinBox')
        thr_exportdata_checkbox = self.findChild(QtWidgets.QCheckBox, 'exportData_checkBox')
        thr_dialogbuttons = self.findChild(QtWidgets.QDialogButtonBox, 'thrReqvsVels_buttonBox')

    @staticmethod
    def setValidators():

        thr_minv_edit.setValidator(double_validator)
        thr_maxv_edit.setValidator(double_validator)

    @staticmethod
    def adjustLineColorProperty():

        thr_linecolor_combo.addItems(colors.keys())
        thr_linecolor_combo.setCurrentIndex(1)

    def apply(self):

        thr_k = acalculate()
        thr_oef = acalculate()
        thr_cd = acalculate()
        thr_cl = acalculate()
        thr_cd = thr_cd.dragcoefficient(self.cd0, thr_k.kFactor(self.wingspan, self.wingarea, thr_oef.oef_estimate(self.wingspan, self.wingarea)), thr_cl.liftcoefficient(float(thr_minv_edit.text()), float(thr_maxv_edit.text()), self.weight, self.wingarea, self.rho))

        thrustReq = acalculate()
        thrustReq = thrustReq.thrustReq(float(thr_minv_edit.text()), float(thr_maxv_edit.text()), self.wingarea, self.rho, thr_cd, 0.1)

        if thr_exportdata_checkbox.isChecked():

            thr_export_xlsx = aeroexport()
            thr_export_xlsx.thrReqvsVelocity(thrustReq, np.arange(float(thr_minv_edit.text()), float(thr_maxv_edit.text())))

            thr_info_msg = QtWidgets.QMessageBox()
            thr_info_msg.setIcon(QtWidgets.QMessageBox.Information)
            thr_info_msg.setText("All data have been exported inside 'XLSX Workbooks' folder.")
            thr_info_msg.setWindowTitle("DATA HAVE BEEN EXPORTED SUCCESSFULLY")
            thr_info_msg.setStyleSheet("QMessageBox {font: 12pt Ubuntu}")
            thr_button = thr_info_msg.addButton(QtWidgets.QMessageBox.Ok)
            thr_button.setIcon(QtGui.QIcon("icons/check.png"))
            thr_button.setFixedSize(75, 35)
            thr_button.setStyleSheet("QPushButton {font: 10pt Ubuntu}")
            thr_info_msg.setDefaultButton(thr_button)
            thr_info_msg.exec_()
        else:
            pass

        plotthr_vel = agplot()
        plotthr_vel.thrustrequiredvsvelocity(thrustReq, float(thr_minv_edit.text()), float(thr_maxv_edit.text()), 0.1, colors.get(thr_linecolor_combo.currentText()), int(thr_lineweight_spin.value()), True)

        thr_minv_edit.clear()
        thr_maxv_edit.clear()
        self.close()


class PowerReqvsVelocityDialog(QtWidgets.QDialog):

    def __init__(self, p_weight, p_wingarea, p_wingspan, p_rho, p_cd0):
        super(PowerReqvsVelocityDialog, self).__init__()
        uic.loadUi('modules/ui/pwrReqvsVelDialog.ui', self)

        self.weight = p_weight
        self.wingarea = p_wingarea
        self.wingspan = p_wingspan
        self.rho = p_rho
        self.cd0 = p_cd0

        self.setFixedSize(300, 285)

        self.center()
        self.pullChildren()
        self.setValidators()
        self.adjustLineColorProperty()

        applybutton = pwr_dialogbuttons.button(QtWidgets.QDialogButtonBox.Apply)
        rejectbutton = pwr_dialogbuttons.button(QtWidgets.QDialogButtonBox.Cancel)

        applybutton.clicked.connect(self.apply)
        rejectbutton.clicked.connect(self.close)

    def center(self):

        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()

        qr.moveCenter(cp)

        self.move(qr.topLeft())

    def pullChildren(self):

        global pwr_minv_edit, pwr_maxv_edit, pwr_linecolor_combo, pwr_lineweight_spin, pwr_exportdata_checkbox, pwr_dialogbuttons

        pwr_minv_edit = self.findChild(QtWidgets.QLineEdit, 'pwrReqminVel_lineEdit')
        pwr_maxv_edit = self.findChild(QtWidgets.QLineEdit, 'pwrReqmaxVel_lineEdit')
        pwr_linecolor_combo = self.findChild(QtWidgets.QComboBox, 'pwrReqvsVel_linecolor_comboBox')
        pwr_lineweight_spin = self.findChild(QtWidgets.QSpinBox, 'pwrReqvsVel_lw_spinBox')
        pwr_exportdata_checkbox = self.findChild(QtWidgets.QCheckBox, 'exportData_checkBox')
        pwr_dialogbuttons = self.findChild(QtWidgets.QDialogButtonBox, 'pwrReqvsVels_buttonBox')

    @staticmethod
    def setValidators():

        pwr_minv_edit.setValidator(double_validator)
        pwr_maxv_edit.setValidator(double_validator)

    @staticmethod
    def adjustLineColorProperty():

        pwr_linecolor_combo.addItems(colors.keys())
        pwr_linecolor_combo.setCurrentIndex(1)

    def apply(self):

        pwr_k = acalculate()
        pwr_oef = acalculate()
        pwr_cd = acalculate()
        pwr_cl = acalculate()
        pwr_cd = pwr_cd.dragcoefficient(self.cd0, pwr_k.kFactor(self.wingspan, self.wingarea, pwr_oef.oef_estimate(self.wingspan, self.wingarea)), pwr_cl.liftcoefficient(float(pwr_minv_edit.text()), float(pwr_maxv_edit.text()), self.weight, self.wingarea, self.rho))

        powerRequired = acalculate()
        powerRequired = powerRequired.powerReq(float(pwr_minv_edit.text()), float(pwr_maxv_edit.text()), self.wingarea, self.rho, pwr_cd, 0.1)

        if pwr_exportdata_checkbox.isChecked():

            pwr_export_xlsx = aeroexport()
            pwr_export_xlsx.powervsVelocity(powerRequired, np.arange(float(thr_minv_edit.text()), float(thr_maxv_edit.text())))

            pwr_info_msg = QtWidgets.QMessageBox()
            pwr_info_msg.setIcon(QtWidgets.QMessageBox.Information)
            pwr_info_msg.setText("All data have been exported inside 'XLSX Workbooks' folder.")
            pwr_info_msg.setWindowTitle("DATA HAVE BEEN EXPORTED SUCCESSFULLY")
            pwr_info_msg.setStyleSheet("QMessageBox {font: 12pt Ubuntu}")
            pwr_button = pwr_info_msg.addButton(QtWidgets.QMessageBox.Ok)
            pwr_button.setIcon(QtGui.QIcon("icons/check.png"))
            pwr_button.setFixedSize(75, 35)
            pwr_button.setStyleSheet("QPushButton {font: 10pt Ubuntu}")
            pwr_info_msg.setDefaultButton(pwr_button)
            pwr_info_msg.exec_()
        else:
            pass

        plotpwr_vel = agplot()
        plotpwr_vel.thrustrequiredvsvelocity(powerRequired, float(pwr_minv_edit.text()), float(pwr_maxv_edit.text()), 0.1, colors.get(pwr_linecolor_combo.currentText()), int(pwr_lineweight_spin.value()), True)

        pwr_minv_edit.clear()
        pwr_maxv_edit.clear()
        self.close()


class DragvsVelocity(QtWidgets.QDialog):

    def __init__(self, d_weight, d_wingarea, d_wingspan, d_rho, d_cd0):
        super(DragvsVelocity, self).__init__()
        uic.loadUi('modules/ui/dragvsVelDialog.ui', self)

        self.weight = d_weight
        self.wingarea = d_wingarea
        self.wingspan = d_wingspan
        self.rho = d_rho
        self.cd0 = d_cd0

        self.setFixedSize(300, 285)

        self.center()
        self.pullChildren()
        self.setValidators()
        self.adjustLineColorProperty()

        applybutton = drag_dialogbuttons.button(QtWidgets.QDialogButtonBox.Apply)
        rejectbutton = drag_dialogbuttons.button(QtWidgets.QDialogButtonBox.Cancel)

        applybutton.clicked.connect(self.apply)
        rejectbutton.clicked.connect(self.close)

    def center(self):

        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()

        qr.moveCenter(cp)

        self.move(qr.topLeft())

    def pullChildren(self):

        global drag_minv_edit, drag_maxv_edit, drag_linecolor_combo, drag_lineweight_spin, drag_exportdata_checkbox, drag_dialogbuttons

        drag_minv_edit = self.findChild(QtWidgets.QLineEdit, 'dragminVel_lineEdit')
        drag_maxv_edit = self.findChild(QtWidgets.QLineEdit, 'dragmaxVel_lineEdit')
        drag_linecolor_combo = self.findChild(QtWidgets.QComboBox, 'dragvsVel_linecolor_comboBox')
        drag_lineweight_spin = self.findChild(QtWidgets.QSpinBox, 'dragvsVel_lw_spinBox')
        drag_exportdata_checkbox = self.findChild(QtWidgets.QCheckBox, 'exportData_checkBox')
        drag_dialogbuttons = self.findChild(QtWidgets.QDialogButtonBox, 'dragvsVels_buttonBox')

    @staticmethod
    def setValidators():

        drag_minv_edit.setValidator(double_validator)
        drag_maxv_edit.setValidator(double_validator)

    @staticmethod
    def adjustLineColorProperty():

        drag_linecolor_combo.addItems(colors.keys())
        drag_linecolor_combo.setCurrentIndex(1)

    def apply(self):

        drag_k = acalculate()
        drag_oef = acalculate()
        drag_cd = acalculate()
        drag_cl = acalculate()
        drag_cd = drag_cd.dragcoefficient(self.cd0, drag_k.kFactor(self.wingspan, self.wingarea, drag_oef.oef_estimate(self.wingspan, self.wingarea)), drag_cl.liftcoefficient(float(drag_minv_edit.text()), float(drag_maxv_edit.text()), self.weight, self.wingarea, self.rho))

        drag_force = acalculate()
        drag_force = drag_force.drag(float(drag_minv_edit.text()), float(drag_maxv_edit.text()), self.wingarea, self.rho, drag_cd, 0.1)

        if drag_exportdata_checkbox.isChecked():

            drag_export_xlsx = aeroexport()
            drag_export_xlsx.dragvsVelocity(drag_force, np.arange(float(drag_minv_edit.text()), float(drag_maxv_edit.text())))

            drag_info_msg = QtWidgets.QMessageBox()
            drag_info_msg.setIcon(QtWidgets.QMessageBox.Information)
            drag_info_msg.setText("All data have been exported inside 'XLSX Workbooks' folder.")
            drag_info_msg.setWindowTitle("DATA HAVE BEEN EXPORTED SUCCESSFULLY")
            drag_info_msg.setStyleSheet("QMessageBox {font: 12pt Ubuntu}")
            drag_button = drag_info_msg.addButton(QtWidgets.QMessageBox.Ok)
            drag_button.setIcon(QtGui.QIcon("icons/check.png"))
            drag_button.setFixedSize(75, 35)
            drag_button.setStyleSheet("QPushButton {font: 10pt Ubuntu}")
            drag_info_msg.setDefaultButton(drag_button)
            drag_info_msg.exec_()
        else:
            pass

        plotdrag_vel = agplot()
        plotdrag_vel.dragvsvelocity(drag_force, float(drag_minv_edit.text()), float(drag_maxv_edit.text()), 0.1, colors.get(drag_linecolor_combo.currentText()), int(drag_lineweight_spin.value()), True)

        drag_minv_edit.clear()
        drag_maxv_edit.clear()
        self.close()


class Lift2dragvsVelocityDialog(QtWidgets.QDialog):

    def __init__(self, ltod_weight, ltod_wingarea, ltod_wingspan, ltod_rho, ltod_cd0):
        super(Lift2dragvsVelocityDialog, self).__init__()
        uic.loadUi('modules/ui/lift2dragvsVelDialog.ui', self)

        self.setFixedSize(300, 285)

        self.weight = ltod_weight
        self.wingarea = ltod_wingarea
        self.wingspan = ltod_wingspan
        self.rho = ltod_rho
        self.cd0 = ltod_cd0

        self.center()
        self.pullChildren()
        self.setValidators()
        self.adjustLineColorProperty()

        applybutton = lift2drag_dialogbuttons.button(QtWidgets.QDialogButtonBox.Apply)
        rejectbutton = lift2drag_dialogbuttons.button(QtWidgets.QDialogButtonBox.Cancel)

        applybutton.clicked.connect(self.apply)
        rejectbutton.clicked.connect(self.close)

    def center(self):

        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()

        qr.moveCenter(cp)

        self.move(qr.topLeft())

    def pullChildren(self):

        global lift2drag_minv_edit, lift2drag_maxv_edit, lift2drag_linecolor_combo, lift2drag_lineweight_spin, lift2drag_exportdata_checkbox, lift2drag_dialogbuttons

        lift2drag_minv_edit = self.findChild(QtWidgets.QLineEdit, 'lift2dragminVel_lineEdit')
        lift2drag_maxv_edit = self.findChild(QtWidgets.QLineEdit, 'lift2dragmaxVel_lineEdit')
        lift2drag_linecolor_combo = self.findChild(QtWidgets.QComboBox, 'lift2dragvsVel_linecolor_comboBox')
        lift2drag_lineweight_spin = self.findChild(QtWidgets.QSpinBox, 'lift2dragvsVel_lw_spinBox')
        lift2drag_exportdata_checkbox = self.findChild(QtWidgets.QCheckBox, 'exportData_checkBox')
        lift2drag_dialogbuttons = self.findChild(QtWidgets.QDialogButtonBox, 'lift2dragvsVel_buttonBox')

    @staticmethod
    def setValidators():

        lift2drag_minv_edit.setValidator(double_validator)
        lift2drag_maxv_edit.setValidator(double_validator)

    @staticmethod
    def adjustLineColorProperty():

        lift2drag_linecolor_combo.addItems(colors.keys())
        lift2drag_linecolor_combo.setCurrentIndex(1)

    def apply(self):

        lift2drag_k = acalculate()
        lift2drag_oef = acalculate()
        lift2drag_cd = acalculate()
        lift2drag_cl = acalculate()
        lift2drag_cd = lift2drag_cd.dragcoefficient(self.cd0, lift2drag_k.kFactor(self.wingspan, self.wingarea, lift2drag_oef.oef_estimate(self.wingspan, self.wingarea)), lift2drag_cl.liftcoefficient(float(lift2drag_minv_edit.text()), float(lift2drag_maxv_edit.text()), self.weight, self.wingarea, self.rho))

        lift2drag_cl = acalculate()
        lift2drag_cl = lift2drag_cl.liftcoefficient(float(lift2drag_minv_edit.text()), float(lift2drag_maxv_edit.text()), self.weight, self.wingarea, self.rho)

        ltod = lift2drag_cd/lift2drag_cl

        if lift2drag_exportdata_checkbox.isChecked():

            lift2drag_export_xlsx = aeroexport()
            lift2drag_export_xlsx.lift2dragvsVelocity(ltod, np.arange(float(lift2drag_minv_edit.text()), float(lift2drag_maxv_edit.text())))

            lift2drag_info_msg = QtWidgets.QMessageBox()
            lift2drag_info_msg.setIcon(QtWidgets.QMessageBox.Information)
            lift2drag_info_msg.setText("All data have been exported inside 'XLSX Workbooks' folder.")
            lift2drag_info_msg.setWindowTitle("DATA HAVE BEEN EXPORTED SUCCESSFULLY")
            lift2drag_info_msg.setStyleSheet("QMessageBox {font: 12pt Ubuntu}")
            lift2drag_button = lift2drag_info_msg.addButton(QtWidgets.QMessageBox.Ok)
            lift2drag_button.setIcon(QtGui.QIcon("icons/check.png"))
            lift2drag_button.setFixedSize(75, 35)
            lift2drag_button.setStyleSheet("QPushButton {font: 10pt Ubuntu}")
            lift2drag_info_msg.setDefaultButton(lift2drag_button)
            lift2drag_info_msg.exec_()
        else:
            pass

        plotlift2drag_vel = agplot()
        plotlift2drag_vel.lift2dragvsvelocity(ltod, float(lift2drag_minv_edit.text()), float(lift2drag_maxv_edit.text()), 0.1, colors.get(lift2drag_linecolor_combo.currentText()), int(lift2drag_lineweight_spin.value()), True)

        lift2drag_minv_edit.clear()
        lift2drag_maxv_edit.clear()
        self.close()


class AvailthrvsThrustReqDialog(QtWidgets.QDialog):

    def __init__(self, avthr_weight, avthr_wingarea, avthr_wingspan, avthr_rho, avthr_cd0):
        super(AvailthrvsThrustReqDialog, self).__init__()
        uic.loadUi('modules/ui/avthrvsThrReqDialog.ui', self)

        self.weight = avthr_weight
        self.wingarea = avthr_wingarea
        self.wingspan = avthr_wingspan
        self.rho = avthr_rho
        self.cd0 = avthr_cd0

        self.setFixedSize(304, 325)

        self.center()
        self.pullChildren()
        self.setValidators()
        self.adjustLineColorProperty()

        applybutton = avthr_dialogbuttons.button(QtWidgets.QDialogButtonBox.Apply)
        rejectbutton = avthr_dialogbuttons.button(QtWidgets.QDialogButtonBox.Cancel)

        applybutton.clicked.connect(self.apply)
        rejectbutton.clicked.connect(self.close)

    def center(self):

        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()

        qr.moveCenter(cp)

        self.move(qr.topLeft())

    def pullChildren(self):

        global avthr_minv_edit, avthr_maxv_edit, avthr_firstlinecolor_combo, avthr_secondlinecolor_combo, avthr_lineweight_spin, avthr_exportdata_checkbox, avthr_dialogbuttons, avthr_availablethr_edit

        avthr_minv_edit = self.findChild(QtWidgets.QLineEdit, 'avthrminVel_lineEdit')
        avthr_maxv_edit = self.findChild(QtWidgets.QLineEdit, 'avthrmaxVel_lineEdit')
        avthr_firstlinecolor_combo = self.findChild(QtWidgets.QComboBox, 'avthrvsThrReq_firstlinecolor_comboBox')
        avthr_secondlinecolor_combo = self.findChild(QtWidgets.QComboBox, 'avthrvsThrReq_secondlinecolor_comboBox')
        avthr_lineweight_spin = self.findChild(QtWidgets.QSpinBox, 'avthrvsThrReq_lw_spinBox')
        avthr_dialogbuttons = self.findChild(QtWidgets.QDialogButtonBox, 'avthrvsThrReq_buttonBox')
        avthr_availablethr_edit = self.findChild(QtWidgets.QLineEdit, 'avthrvsThrReq_avthr_lineEdit')

    @staticmethod
    def setValidators():

        avthr_minv_edit.setValidator(double_validator)
        avthr_maxv_edit.setValidator(double_validator)

    @staticmethod
    def adjustLineColorProperty():

        avthr_firstlinecolor_combo.addItems(colors.keys())
        avthr_firstlinecolor_combo.setCurrentIndex(1)

        avthr_secondlinecolor_combo.addItems(colors.keys())
        avthr_secondlinecolor_combo.setCurrentIndex(2)

    def apply(self):

        avthr_k = acalculate()
        avthr_oef = acalculate()
        avthr_cd = acalculate()
        avthr_cl = acalculate()
        avthr_cd = avthr_cd.dragcoefficient(self.cd0, avthr_k.kFactor(self.wingspan, self.wingarea, avthr_oef.oef_estimate(self.wingspan, self.wingarea)), avthr_cl.liftcoefficient(float(avthr_minv_edit.text()), float(avthr_maxv_edit.text()), self.weight, self.wingarea, self.rho))

        avthr_thrustReq = acalculate()
        avthr_thrustReq = avthr_thrustReq.thrustReq(float(avthr_minv_edit.text()), float(avthr_maxv_edit.text()), self.wingarea, self.rho, avthr_cd, 0.1)

        plotthr_vel = agplot()
        plotthr_vel.thrustavailablevsthrustrequired(float(avthr_availablethr_edit.text()), avthr_thrustReq, float(avthr_minv_edit.text()), float(avthr_maxv_edit.text()), 0.1, colors.get(avthr_firstlinecolor_combo.currentText()), colors.get(avthr_secondlinecolor_combo.currentText()), int(avthr_lineweight_spin.value()), True)

        avthr_minv_edit.clear()
        avthr_maxv_edit.clear()
        self.close()


app = QtWidgets.QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon('icons/planeicon.png'))
interface = MainWindow()
interface.show()

sys.exit(app.exec_())
