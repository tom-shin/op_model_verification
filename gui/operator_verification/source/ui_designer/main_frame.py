# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_frame.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1214, 845)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.tabWidget = QtWidgets.QTabWidget(self.frame)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout.setObjectName("gridLayout")
        self.frame_2 = QtWidgets.QFrame(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.scenario_path_lineedit = QtWidgets.QLineEdit(self.frame_2)
        self.scenario_path_lineedit.setObjectName("scenario_path_lineedit")
        self.gridLayout_4.addWidget(self.scenario_path_lineedit, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setObjectName("label")
        self.gridLayout_4.addWidget(self.label, 0, 0, 1, 1)
        self.open_pushButton = QtWidgets.QPushButton(self.frame_2)
        self.open_pushButton.setObjectName("open_pushButton")
        self.gridLayout_4.addWidget(self.open_pushButton, 0, 2, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_4, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        self.scrollArea = QtWidgets.QScrollArea(self.frame_2)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1114, 288))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.verticalLayout_11.addLayout(self.formLayout)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 1, 0, 1, 1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.all_check_scenario = QtWidgets.QPushButton(self.frame_2)
        self.all_check_scenario.setObjectName("all_check_scenario")
        self.horizontalLayout_6.addWidget(self.all_check_scenario)
        self.all_uncheck_scenario = QtWidgets.QPushButton(self.frame_2)
        self.all_uncheck_scenario.setObjectName("all_uncheck_scenario")
        self.horizontalLayout_6.addWidget(self.all_uncheck_scenario)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.analyze_pushButton = QtWidgets.QPushButton(self.frame_2)
        self.analyze_pushButton.setObjectName("analyze_pushButton")
        self.horizontalLayout_6.addWidget(self.analyze_pushButton)
        self.save_pushButton = QtWidgets.QPushButton(self.frame_2)
        self.save_pushButton.setObjectName("save_pushButton")
        self.horizontalLayout_6.addWidget(self.save_pushButton)
        self.gridLayout_2.addLayout(self.horizontalLayout_6, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.tab_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.target_dir = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.target_dir.setFont(font)
        self.target_dir.setObjectName("target_dir")
        self.horizontalLayout.addWidget(self.target_dir)
        self.targetformat_lineedit = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.targetformat_lineedit.sizePolicy().hasHeightForWidth())
        self.targetformat_lineedit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.targetformat_lineedit.setFont(font)
        self.targetformat_lineedit.setObjectName("targetformat_lineedit")
        self.horizontalLayout.addWidget(self.targetformat_lineedit)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.command_lineedit = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.command_lineedit.sizePolicy().hasHeightForWidth())
        self.command_lineedit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.command_lineedit.setFont(font)
        self.command_lineedit.setObjectName("command_lineedit")
        self.horizontalLayout.addWidget(self.command_lineedit)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.error_lineedit = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.error_lineedit.sizePolicy().hasHeightForWidth())
        self.error_lineedit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.error_lineedit.setFont(font)
        self.error_lineedit.setObjectName("error_lineedit")
        self.horizontalLayout.addWidget(self.error_lineedit)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.tab_3)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.groupBox_5 = QtWidgets.QGroupBox(self.tab_3)
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.label_13 = QtWidgets.QLabel(self.groupBox_5)
        self.label_13.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_13.setText("")
        self.label_13.setObjectName("label_13")
        self.verticalLayout_12.addWidget(self.label_13)
        self.verticalLayout_9.addWidget(self.groupBox_5)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox_7 = QtWidgets.QGroupBox(self.tab)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_7.setFont(font)
        self.groupBox_7.setObjectName("groupBox_7")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.groupBox_7)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_13.addItem(spacerItem1)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_5 = QtWidgets.QLabel(self.groupBox_7)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_7.addWidget(self.label_5)
        self.dirlineEdit = QtWidgets.QLineEdit(self.groupBox_7)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.dirlineEdit.setFont(font)
        self.dirlineEdit.setObjectName("dirlineEdit")
        self.horizontalLayout_7.addWidget(self.dirlineEdit)
        self.dirpushButton = QtWidgets.QPushButton(self.groupBox_7)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.dirpushButton.setFont(font)
        self.dirpushButton.setObjectName("dirpushButton")
        self.horizontalLayout_7.addWidget(self.dirpushButton)
        self.verticalLayout_13.addLayout(self.horizontalLayout_7)
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox_7)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.n_lineEdit = QtWidgets.QLineEdit(self.groupBox_4)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.n_lineEdit.setFont(font)
        self.n_lineEdit.setObjectName("n_lineEdit")
        self.gridLayout_5.addWidget(self.n_lineEdit, 0, 1, 1, 1)
        self.reasonlineEdit = QtWidgets.QLineEdit(self.groupBox_4)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.reasonlineEdit.setFont(font)
        self.reasonlineEdit.setObjectName("reasonlineEdit")
        self.gridLayout_5.addWidget(self.reasonlineEdit, 2, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.groupBox_4)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.gridLayout_5.addWidget(self.label_8, 0, 0, 1, 1)
        self.simplelineEdit = QtWidgets.QLineEdit(self.groupBox_4)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.simplelineEdit.setFont(font)
        self.simplelineEdit.setObjectName("simplelineEdit")
        self.gridLayout_5.addWidget(self.simplelineEdit, 1, 1, 1, 1)
        self.multilineEdit = QtWidgets.QLineEdit(self.groupBox_4)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.multilineEdit.setFont(font)
        self.multilineEdit.setObjectName("multilineEdit")
        self.gridLayout_5.addWidget(self.multilineEdit, 3, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.groupBox_4)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.gridLayout_5.addWidget(self.label_9, 1, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.groupBox_4)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.gridLayout_5.addWidget(self.label_10, 2, 0, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.groupBox_4)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.gridLayout_5.addWidget(self.label_11, 3, 0, 1, 1)
        self.verticalLayout_6.addLayout(self.gridLayout_5)
        self.verticalLayout_13.addWidget(self.groupBox_4)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem2)
        self.gengenpushButton = QtWidgets.QPushButton(self.groupBox_7)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.gengenpushButton.setFont(font)
        self.gengenpushButton.setObjectName("gengenpushButton")
        self.horizontalLayout_10.addWidget(self.gengenpushButton)
        self.verticalLayout_13.addLayout(self.horizontalLayout_10)
        self.verticalLayout_3.addWidget(self.groupBox_7)
        self.groupBox_8 = QtWidgets.QGroupBox(self.tab)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_8.setFont(font)
        self.groupBox_8.setObjectName("groupBox_8")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.groupBox_8)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_14.addItem(spacerItem3)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.testset_label = QtWidgets.QLabel(self.groupBox_8)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.testset_label.setFont(font)
        self.testset_label.setObjectName("testset_label")
        self.horizontalLayout_13.addWidget(self.testset_label)
        self.testset_lineEdit = QtWidgets.QLineEdit(self.groupBox_8)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.testset_lineEdit.setFont(font)
        self.testset_lineEdit.setObjectName("testset_lineEdit")
        self.horizontalLayout_13.addWidget(self.testset_lineEdit)
        self.testset_pushButton = QtWidgets.QPushButton(self.groupBox_8)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.testset_pushButton.setFont(font)
        self.testset_pushButton.setObjectName("testset_pushButton")
        self.horizontalLayout_13.addWidget(self.testset_pushButton)
        self.verticalLayout_14.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem4)
        self.vector_env_pushButton = QtWidgets.QPushButton(self.groupBox_8)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.vector_env_pushButton.setFont(font)
        self.vector_env_pushButton.setObjectName("vector_env_pushButton")
        self.horizontalLayout_14.addWidget(self.vector_env_pushButton)
        self.vector_start_pushButton = QtWidgets.QPushButton(self.groupBox_8)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.vector_start_pushButton.setFont(font)
        self.vector_start_pushButton.setObjectName("vector_start_pushButton")
        self.horizontalLayout_14.addWidget(self.vector_start_pushButton)
        self.verticalLayout_14.addLayout(self.horizontalLayout_14)
        self.verticalLayout_3.addWidget(self.groupBox_8)
        self.tabWidget.addTab(self.tab, "")
        self.verticalLayout_8.addWidget(self.tabWidget)
        self.logtextbrowser = QtWidgets.QTextBrowser(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logtextbrowser.sizePolicy().hasHeightForWidth())
        self.logtextbrowser.setSizePolicy(sizePolicy)
        self.logtextbrowser.setObjectName("logtextbrowser")
        self.verticalLayout_8.addWidget(self.logtextbrowser)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.log_clear_pushButton = QtWidgets.QPushButton(self.frame)
        self.log_clear_pushButton.setObjectName("log_clear_pushButton")
        self.horizontalLayout_4.addWidget(self.log_clear_pushButton)
        self.popctrl_radioButton = QtWidgets.QRadioButton(self.frame)
        self.popctrl_radioButton.setObjectName("popctrl_radioButton")
        self.horizontalLayout_4.addWidget(self.popctrl_radioButton)
        self.verticalLayout_8.addLayout(self.horizontalLayout_4)
        self.verticalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1214, 26))
        self.menubar.setObjectName("menubar")
        self.menuBrowser = QtWidgets.QMenu(self.menubar)
        self.menuBrowser.setObjectName("menuBrowser")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOn = QtWidgets.QAction(MainWindow)
        self.actionOn.setObjectName("actionOn")
        self.actionOff = QtWidgets.QAction(MainWindow)
        self.actionOff.setObjectName("actionOff")
        self.menuBrowser.addAction(self.actionOn)
        self.menuBrowser.addAction(self.actionOff)
        self.menubar.addAction(self.menuBrowser.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Target Directory"))
        self.open_pushButton.setText(_translate("MainWindow", "Open"))
        self.all_check_scenario.setText(_translate("MainWindow", "Scenario All Check"))
        self.all_uncheck_scenario.setText(_translate("MainWindow", "Scenario All Uncheck"))
        self.analyze_pushButton.setText(_translate("MainWindow", "Analyze"))
        self.save_pushButton.setText(_translate("MainWindow", "Save"))
        self.groupBox.setTitle(_translate("MainWindow", "Keyword Ctrl."))
        self.target_dir.setText(_translate("MainWindow", "Target Format"))
        self.label_4.setText(_translate("MainWindow", "Command"))
        self.label_3.setText(_translate("MainWindow", "Error"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Single OP Verification"))
        self.groupBox_5.setTitle(_translate("MainWindow", "Embedding & Vectorization"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "reserved_1"))
        self.groupBox_7.setTitle(_translate("MainWindow", "Question/ Ground-Truth Generation"))
        self.label_5.setText(_translate("MainWindow", "Source Directory"))
        self.dirpushButton.setText(_translate("MainWindow", "Open (*.md/ *.txt file)"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Ctrl.params."))
        self.n_lineEdit.setText(_translate("MainWindow", "10"))
        self.reasonlineEdit.setText(_translate("MainWindow", "0.25"))
        self.label_8.setText(_translate("MainWindow", "Number of Scenario"))
        self.simplelineEdit.setText(_translate("MainWindow", "0.5"))
        self.multilineEdit.setText(_translate("MainWindow", "0.25"))
        self.label_9.setText(_translate("MainWindow", "Simple"))
        self.label_10.setText(_translate("MainWindow", "Reasoning"))
        self.label_11.setText(_translate("MainWindow", "Multi_Context"))
        self.gengenpushButton.setText(_translate("MainWindow", "Generate"))
        self.groupBox_8.setTitle(_translate("MainWindow", "Context/ Answer Generation"))
        self.testset_label.setText(_translate("MainWindow", "File"))
        self.testset_pushButton.setText(_translate("MainWindow", "Open"))
        self.vector_env_pushButton.setText(_translate("MainWindow", "Env. Setup"))
        self.vector_start_pushButton.setText(_translate("MainWindow", "Generate"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "reserved_2"))
        self.log_clear_pushButton.setText(_translate("MainWindow", "Log Clear"))
        self.popctrl_radioButton.setText(_translate("MainWindow", "pop control"))
        self.menuBrowser.setTitle(_translate("MainWindow", "Log Browser Ctrl."))
        self.actionOn.setText(_translate("MainWindow", "On"))
        self.actionOff.setText(_translate("MainWindow", "Off"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
