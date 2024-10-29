#!/usr/bin/env python3

import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

import os
import sys
import logging

from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5 import QtWidgets, QtCore, QtGui

from source.single_op_verification.single_op_verifier import ctrl_single_op_verify_class
from source.__init__ import keyword_ctrl, Version, ssh_server_information, SSH_Ctrl_Class, Checking_Directory

# BASE_DIR 설정: EXE 또는 리눅스 ./ 실행 여부에 따라 경로 설정
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 일반 Python 스크립트 실행 시

logging.basicConfig(level=logging.INFO)


def PRINT_(*args):
    logging.info(args)


def load_module_func(module_name):
    mod = __import__(f"{module_name}", fromlist=[module_name])
    return mod


class EmittingStream(QObject):
    textWritten = pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

    def flush(self):
        pass


class Single_OPs_Verification_MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.directory = None
        self.main_single_op_ctrl = None
        self.ssh_class_instance = None

        """ for main frame & widget """
        self.mainFrame_ui = None
        self.widget_ui = None

        self.setupUi()

    def setupUi(self):
        # Load the main window's UI module
        rt = load_module_func(module_name="source.ui_designer.main_frame")
        self.mainFrame_ui = rt.Ui_MainWindow()
        self.mainFrame_ui.setupUi(self)

        element_list = [fmt.strip() for fmt in keyword_ctrl["target_format"]]
        text_concatenation = ', '.join(element_list)
        self.mainFrame_ui.targetformat_lineedit.setText(text_concatenation)

        element_list = [fmt.strip() for fmt in keyword_ctrl["error_keyword"]]
        text_concatenation = ', '.join(element_list)
        self.mainFrame_ui.error_lineedit.setText(text_concatenation)

        element_list = [fmt.strip() for fmt in keyword_ctrl["op_exe_cmd"]]
        text_concatenation = ', '.join(element_list)
        self.mainFrame_ui.command_lineedit.setText(text_concatenation)

        element_list = [fmt.strip() for fmt in keyword_ctrl["exclusive_dir"]]
        text_concatenation = ', '.join(element_list)
        self.mainFrame_ui.exclusivelineEdit.setText(text_concatenation)

        self.mainFrame_ui.iplineEdit.setText(ssh_server_information["serverip"])
        self.mainFrame_ui.portlineEdit.setText(ssh_server_information["port"])
        self.mainFrame_ui.usernamelineEdit.setText(ssh_server_information["username"])
        self.mainFrame_ui.pwdlineEdit.setText(ssh_server_information["password"])
        self.mainFrame_ui.containerlineEdit.setText(ssh_server_information["container_name"])

        self.setWindowTitle(Version)

        self.mainFrame_ui.frame.hide()

    def closeEvent(self, event):
        answer = QtWidgets.QMessageBox.question(self,
                                                "Confirm Exit...",
                                                "Are you sure you want to exit?\nAll data will be lost.",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if answer == QtWidgets.QMessageBox.Yes:
            event.accept()

            self.main_ssh_disconnection()
        else:
            event.ignore()

    def normalOutputWritten(self, text):
        cursor = self.mainFrame_ui.logtextbrowser.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)

        # 기본 글자 색상 설정
        color_format = cursor.charFormat()

        color_format.setForeground(QtCore.Qt.red if "><" in text or "error" in text.lower() else QtCore.Qt.black)

        cursor.setCharFormat(color_format)
        cursor.insertText(text)

        # 커서를 최신 위치로 업데이트
        self.mainFrame_ui.logtextbrowser.setTextCursor(cursor)
        self.mainFrame_ui.logtextbrowser.ensureCursorVisible()

    def cleanLogBrowser(self):
        self.mainFrame_ui.logtextbrowser.clear()

    def log_browser_ctrl(self):
        sender = self.sender()
        if sender:
            if sender.objectName() == "actionOff_2":
                self.mainFrame_ui.logtextbrowser.hide()
            else:
                self.mainFrame_ui.logtextbrowser.show()

    def connectSlotSignal(self):
        """ sys.stdout redirection """
        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)
        self.mainFrame_ui.log_clear_pushButton.clicked.connect(self.cleanLogBrowser)

        # evaluation tab
        self.mainFrame_ui.open_pushButton.clicked.connect(self.open_directory)
        self.mainFrame_ui.analyze_pushButton.clicked.connect(self.start_analyze)
        self.mainFrame_ui.all_check_scenario.clicked.connect(self.check_all_scenario)
        self.mainFrame_ui.all_uncheck_scenario.clicked.connect(self.check_all_scenario)
        self.mainFrame_ui.save_pushButton.clicked.connect(self.save_result)

        self.mainFrame_ui.actionOff_2.triggered.connect(self.log_browser_ctrl)
        self.mainFrame_ui.actionOn_2.triggered.connect(self.log_browser_ctrl)

        self.mainFrame_ui.actionShow.triggered.connect(self.ssh_control_groupbox)
        self.mainFrame_ui.actionHide.triggered.connect(self.ssh_control_groupbox)

        self.mainFrame_ui.connectpushButton.clicked.connect(self.main_ssh_connection)
        self.mainFrame_ui.disconnectpushButton.clicked.connect(self.main_ssh_disconnection)

        if getattr(sys, 'frozen', False):
            # EXE 파일이 있는 디렉토리로 설정
            Checking_Directory(path_=os.path.dirname(sys.executable))
        else:
            # 일반 Python 스크립트 실행 시
            Checking_Directory(path_=os.path.dirname(os.path.abspath(__file__)))  # 일반 Python 스크립트 실행 시

        # self.mainFrame_ui.logtextbrowser.hide()

    def main_ssh_connection(self):
        ip = self.mainFrame_ui.iplineEdit.text()
        port = self.mainFrame_ui.portlineEdit.text()
        username = self.mainFrame_ui.usernamelineEdit.text()
        pwd = self.mainFrame_ui.pwdlineEdit.text()

        self.ssh_class_instance = SSH_Ctrl_Class(ip=ip, port=port, username=username, pwd=pwd)
        ret = self.ssh_class_instance.ssh_connect()

        if ret:
            self.mainFrame_ui.frame.show()
            self.main_single_op_ctrl = ctrl_single_op_verify_class(ssh=self.ssh_class_instance, parent=self,
                                                                   grand_parent=self.mainFrame_ui)

    def main_ssh_disconnection(self):
        if self.ssh_class_instance is not None:
            ret = self.ssh_class_instance.ssh_disconnect()

            if ret:
                self.mainFrame_ui.frame.hide()
                del self.main_single_op_ctrl

    def ssh_control_groupbox(self):
        sender = self.sender()
        if sender:
            if sender.objectName() == "actionShow":
                self.mainFrame_ui.sshgroupBox.show()
            else:
                self.mainFrame_ui.sshgroupBox.hide()

    def open_directory(self):
        if self.ssh_class_instance is None:
            return

        open_path = self.ssh_class_instance.ssh_remote_diropenbox()
        if open_path.endswith("/"):
            self.directory = open_path[:-1]  # 마지막 '\' 문자 제거

        PRINT_(self.directory)

        if self.directory is None:
            return

        self.main_single_op_ctrl.open_file(ssh_client=self.ssh_class_instance, BASE_DIR=BASE_DIR)
        self.ssh_class_instance.set_container_name_f(container=self.mainFrame_ui.containerlineEdit.text().strip())

    def start_analyze(self):
        self.main_single_op_ctrl.op_analyze(ssh_client=self.ssh_class_instance)

    def check_all_scenario(self):
        if self.main_single_op_ctrl is not None:
            sender = self.sender()
            check = False

            if sender:
                if sender.objectName() == "all_check_scenario":
                    check = True
                elif sender.objectName() == "all_uncheck_scenario":
                    check = False

            self.main_single_op_ctrl.select_all_scenario(check=check)

    def save_result(self):

        if self.main_single_op_ctrl is None:
            return

        if getattr(sys, 'frozen', False):
            # EXE 파일이 있는 디렉토리로 설정
            save_path = os.path.dirname(sys.executable)
        else:
            # 일반 Python 스크립트 실행 시
            save_path = os.path.dirname(os.path.abspath(__file__))  # 일반 Python 스크립트 실행 시

        self.main_single_op_ctrl.save_analyze_result(BASE_DIR_=os.path.join(save_path, "Result"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)  # QApplication 생성 (필수)

    app.setStyle("Fusion")
    ui = Single_OPs_Verification_MainWindow()
    ui.showMaximized()
    ui.connectSlotSignal()

    sys.exit(app.exec_())
