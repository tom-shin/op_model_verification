import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

import os
import sys
import logging
import easygui

from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5 import QtWidgets, QtCore, QtGui

from source.single_op_verification.single_op_verifier import ctrl_single_op_verify_class
from source.__init__ import keyword_ctrl, CheckDir

if getattr(sys, 'frozen', False):
    # PyInstaller로 패키징된 실행 파일일 경우
    BASE_EXE = os.path.dirname(sys.executable)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if getattr(sys, 'frozen', False):
    file_path = os.path.join(BASE_EXE, "version.txt")
else:
    file_path = os.path.join(BASE_DIR, "version.txt")

with open(file_path, "r") as file_:
    Version_ = file_.readline()

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
        self.single_op_ctrl = None

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

        self.setWindowTitle(Version_)

    def closeEvent(self, event):
        answer = QtWidgets.QMessageBox.question(self,
                                                "Confirm Exit...",
                                                "Are you sure you want to exit?\nAll data will be lost.",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if answer == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def normalOutputWritten(self, text):
        cursor = self.mainFrame_ui.logtextbrowser.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)

        # 기본 글자 색상 설정
        color_format = cursor.charFormat()
        color_format.setForeground(QtCore.Qt.red if "><" in text else QtCore.Qt.black)

        cursor.setCharFormat(color_format)
        cursor.insertText(text)

        # 커서를 최신 위치로 업데이트
        self.mainFrame_ui.logtextbrowser.setTextCursor(cursor)
        self.mainFrame_ui.logtextbrowser.ensureCursorVisible()

    def cleanLogBrowser(self):
        self.mainFrame_ui.logtextbrowser.clear()

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

        self.mainFrame_ui.actionOn.triggered.connect(self.log_browser_ctrl)
        self.mainFrame_ui.actionOff.triggered.connect(self.log_browser_ctrl)

        self.single_op_ctrl = ctrl_single_op_verify_class(parent=self, grand_parent=self.mainFrame_ui)

        if getattr(sys, 'frozen', False):
            CheckDir(os.path.join(BASE_EXE, "Result"))
        else:
            CheckDir(os.path.join(BASE_DIR, "Result"))
            
        self.mainFrame_ui.logtextbrowser.hide()

    def log_browser_ctrl(self):
        sender = self.sender()
        if sender:
            if sender.objectName() == "actionOff":
                self.mainFrame_ui.logtextbrowser.hide()
            else:
                self.mainFrame_ui.logtextbrowser.show()

    def open_directory(self):
        self.directory = easygui.diropenbox()

        if self.directory is None:
            return

        self.single_op_ctrl.open_file()

    def start_analyze(self):
        self.single_op_ctrl.op_analyze()

    def check_all_scenario(self):
        if self.single_op_ctrl is not None:
            sender = self.sender()
            check = False

            if sender:
                if sender.objectName() == "all_check_scenario":
                    check = True
                elif sender.objectName() == "all_uncheck_scenario":
                    check = False

            self.single_op_ctrl.select_all_scenario(check=check)

    def save_result(self):
        if self.single_op_ctrl is None:
            return

        if getattr(sys, 'frozen', False):
            self.single_op_ctrl.save_analyze_result(basedir=os.path.join(BASE_EXE, "Result"))
        else:
            self.single_op_ctrl.save_analyze_result(basedir=os.path.join(BASE_DIR, "Result"))



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)  # QApplication 생성 (필수)

    app.setStyle("Fusion")
    ui = Single_OPs_Verification_MainWindow()
    ui.showMaximized()
    ui.connectSlotSignal()

    sys.exit(app.exec_())
