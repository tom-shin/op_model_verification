# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_widget.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(831, 625)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.scenario_checkBox = QtWidgets.QCheckBox(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.scenario_checkBox.setFont(font)
        self.scenario_checkBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.scenario_checkBox.setAutoFillBackground(False)
        self.scenario_checkBox.setObjectName("scenario_checkBox")
        self.verticalLayout_4.addWidget(self.scenario_checkBox)
        self.verticalLayout_3.addLayout(self.verticalLayout_4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.questioin_groupBox = QtWidgets.QGroupBox(self.frame)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.questioin_groupBox.setFont(font)
        self.questioin_groupBox.setObjectName("questioin_groupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.questioin_groupBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pathlineEdit = QtWidgets.QLineEdit(self.questioin_groupBox)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.pathlineEdit.setFont(font)
        self.pathlineEdit.setReadOnly(True)
        self.pathlineEdit.setObjectName("pathlineEdit")
        self.horizontalLayout_2.addWidget(self.pathlineEdit)
        self.open_terminal_pushButton = QtWidgets.QPushButton(self.questioin_groupBox)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.open_terminal_pushButton.setFont(font)
        self.open_terminal_pushButton.setObjectName("open_terminal_pushButton")
        self.horizontalLayout_2.addWidget(self.open_terminal_pushButton)
        self.verticalLayout_5.addWidget(self.questioin_groupBox)
        self.contexts_groupBox = QtWidgets.QGroupBox(self.frame)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.contexts_groupBox.setFont(font)
        self.contexts_groupBox.setObjectName("contexts_groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.contexts_groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.contexts_textEdit = QtWidgets.QTextEdit(self.contexts_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.contexts_textEdit.sizePolicy().hasHeightForWidth())
        self.contexts_textEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.contexts_textEdit.setFont(font)
        self.contexts_textEdit.setReadOnly(True)
        self.contexts_textEdit.setObjectName("contexts_textEdit")
        self.verticalLayout.addWidget(self.contexts_textEdit)
        self.verticalLayout_5.addWidget(self.contexts_groupBox)
        self.horizontalLayout.addWidget(self.frame)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_6.addWidget(self.lineEdit)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem)
        self.horizontalLayout.addWidget(self.groupBox_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.line = QtWidgets.QFrame(Form)
        self.line.setMidLineWidth(4)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_3.addWidget(self.line)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.scenario_checkBox.setText(_translate("Form", "CheckBox"))
        self.questioin_groupBox.setTitle(_translate("Form", "Target Path"))
        self.open_terminal_pushButton.setText(_translate("Form", "Open"))
        self.contexts_groupBox.setTitle(_translate("Form", "Result"))
        self.groupBox_2.setTitle(_translate("Form", "Pass/Fail/Error"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
