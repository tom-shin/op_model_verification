import sys
import threading
import time
import re
import ast

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QObject, QThread

from .. import *
from ..ui_designer import main_widget
from ..ui_designer import fileedit


class Load_Target_Dir_Thread(QtCore.QThread):
    send_scenario_update_ui_sig = QtCore.pyqtSignal(int, tuple)
    send_finish_scenario_update_ui_sig = QtCore.pyqtSignal()

    def __init__(self, file_path, grand_parent):
        super().__init__()
        self.file_path = file_path
        self.grand_parent = grand_parent

    def run(self):
        for cnt, test_path in enumerate(self.file_path):
            self.send_scenario_update_ui_sig.emit(cnt, test_path)

        self.send_finish_scenario_update_ui_sig.emit()


class OP_Analyze_Thread(QThread):
    output_signal = pyqtSignal(str, tuple, int)
    finish_output_signal = pyqtSignal(bool)
    error_signal = pyqtSignal(str, tuple)
    send_max_progress_cnt = pyqtSignal(int)

    def __init__(self, parent=None, grand_parent=None, ssh_client=None):
        super().__init__()
        self.parent = parent
        self.grand_parent = grand_parent
        self._running = True
        self.ssh_client = ssh_client

    def run(self):
        max_cnt = sum(1 for widget in self.parent.added_scenario_widgets if widget[0].scenario_checkBox.isChecked())
        self.send_max_progress_cnt.emit(max_cnt)

        executed_cnt = 0
        for target_widget in self.parent.added_scenario_widgets:
            if not self._running:
                break

            if not target_widget[0].scenario_checkBox.isChecked():
                continue

            executed_cnt += 1

            cwd = target_widget[0].pathlineEdit.text()
            output_list = []
            error_check_flag = False

            cmd_list = [fmt.strip() for fmt in self.grand_parent.command_lineedit.text().split(",")]
            for cmd in cmd_list:
                if self.ssh_client is None:
                    try:
                        process = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                 text=True,
                                                 shell=True, check=True, )

                        if process.stdout:
                            output_list.append(process.stdout.strip())

                        if process.stderr:
                            error_check_flag = True
                            self.error_signal.emit(process.stderr.strip(), target_widget)
                            break

                    except subprocess.CalledProcessError as e:
                        error_check_flag = True
                        self.error_signal.emit(f"Command failed: {str(e)}", target_widget)
                        break
                    except Exception as e:
                        error_check_flag = True
                        self.error_signal.emit(f"{str(e)}", target_widget)
                        break
                else:
                    exe_cmd = f"cd {cwd} && {cmd}"
                    ret, result, error = self.ssh_client.ssh_cmd_execution(cmd=exe_cmd, execute_enntools=True)

                    if ret:
                        output_list.append(result)

                        if len(error) != 0:
                            error_check_flag = True
                            break
                    else:
                        error_check_flag = True
                        break

            if error_check_flag:
                continue

            output = "\n".join(output_list)

            self.output_signal.emit(output, target_widget, executed_cnt)

        self.finish_output_signal.emit(self._running)

    def stop(self):
        self._running = False
        self.quit()
        self.wait(3000)


class ctrl_single_op_verify_class(QObject):
    send_sig_delete_all_sub_widget = pyqtSignal()

    def __init__(self, ssh, parent, grand_parent):
        super().__init__()

        self.BASE_DIR = None
        self.ssh_client = None
        self.result_thread = None
        self.op_result_save_progress = None
        self.start_evaluation_time = None
        self.end_evaluation_time = None

        self.op_analyze_progress = None
        self.user_error_fmt = None
        self.op_analyze_thread = None
        self.added_scenario_widgets = None
        self.all_test_path = None
        self.insert_widget_thread = None
        self.insert_widget_progress = None
        self.dialogs = []  # 열린 팝업을 저장할 리스트

        self._ssh = ssh
        self.parent = parent
        self.grand_parent = grand_parent

        self.send_sig_delete_all_sub_widget.connect(self.update_all_sub_widget)

    def open_file(self, ssh_client=None, BASE_DIR=None):
        self.ssh_client = ssh_client
        self.BASE_DIR = BASE_DIR

        self.parent.mainFrame_ui.scenario_path_lineedit.setText(self.parent.directory)

        self.clear_sub_widget()

    def clear_sub_widget(self):
        while self.parent.mainFrame_ui.formLayout.count():
            item = self.parent.mainFrame_ui.formLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

        self.send_sig_delete_all_sub_widget.emit()

    def update_all_sub_widget(self):
        user_fmt = [fmt.strip() for fmt in self.grand_parent.targetformat_lineedit.text().split(",")]
        ret = get_directory_for_verification(ssh_client=self.ssh_client, base_dir=self.parent,
                                             grand_parent=self.grand_parent, user_defined_fmt=user_fmt,
                                             BASE_DIR=self.BASE_DIR)

        if ret is None:
            return

        # 각 원소에 대해 '/'가 있으면 제거 후, 결과를 j에 저장
        # self.all_test_path = [path.rstrip('/') for path in ret]
        self.all_test_path = [ast.literal_eval(path) for path in ret]

        if len(self.all_test_path) == 0:
            return

        if self.parent.mainFrame_ui.popctrl_radioButton.isChecked():
            self.insert_widget_progress = ModalLess_ProgressDialog(message="Loading Scenario")
        else:
            self.insert_widget_progress = Modal_ProgressDialog(message="Loading Scenario")

        self.insert_widget_progress.setProgressBarMaximum(max_value=len(self.all_test_path))

        self.added_scenario_widgets = []
        self.insert_widget_thread = Load_Target_Dir_Thread(self.all_test_path, self.parent)
        self.insert_widget_thread.send_scenario_update_ui_sig.connect(self.insert_widget_progress_status)
        self.insert_widget_thread.send_finish_scenario_update_ui_sig.connect(self.finish_insert_widget_progress_status)

        self.insert_widget_thread.start()

        self.insert_widget_progress.showModal_less()

    def save_changes(self, full_file, content, dialog):
        # 원격 서버에 파일 내용 저장
        cmd = f"echo '{content}' > {full_file}"  # 예시로 echo 명령을 사용
        result = self.ssh_client.ssh_cmd_execution(cmd=cmd)

        if result[0]:  # 성공적으로 저장 시
            QtWidgets.QMessageBox.information(dialog, "Success", "File saved successfully.")
            dialog.close()
        else:  # 저장 실패 시
            QtWidgets.QMessageBox.warning(dialog, "Error", "Failed to save file.")

    def on_item_double_clicked(self, item, sub_widget):
        file_name = item.text()  # 파일 이름
        path_ = sub_widget.pathlineEdit.text()  # 해당 파일이 존재하는 디렉토리 경로

        full_file = os.path.join(path_, file_name).replace("\\", "/")

        cmd = f"cat {full_file}"  # 파일 내용 가져 오기
        content = self.ssh_client.ssh_cmd_execution(cmd=cmd)

        use_modal = 0
        if use_modal == 0:  # 새로운 창이 계속 열리게 됨
            dialog = QtWidgets.QDialog(None)
            ui = fileedit.Ui_Dialog()
            ui.setupUi(dialog)
            dialog.setWindowTitle(full_file)

            # 시그널 슬롯 연결 람다 사용해서 직접 인자를 넘기자...........
            ui.fileedit_save.clicked.connect(lambda: self.save_changes(full_file, ui.textEdit.toPlainText(), dialog))
            ui.fileedit_cancel.clicked.connect(dialog.close)

            ui.textEdit.setPlainText(content[1])

            # 모달리스 다이얼로그로 설정
            dialog.setWindowModality(QtCore.Qt.NonModal)
            self.dialogs.append(dialog)

            dialog.show()

        elif use_modal == 1:  # 모달리스인데 창이 열리면 이전 열린 창이 사라지고 새로운 창이 열림
            self.dialog = QtWidgets.QDialog(None)
            self.ui = fileedit.Ui_Dialog()
            self.ui.setupUi(self.dialog)

            # 모달리스 다이얼로그로 설정
            self.dialog.setWindowModality(QtCore.Qt.NonModal)

            # 다이얼로그 표시
            self.dialog.show()

        elif use_modal == 2:  # 완전 모달형태로
            self.dialog = QtWidgets.QDialog()
            self.ui = fileedit.Ui_Dialog()
            self.ui.setupUi(self.dialog)

            self.dialog.setWindowModality(QtCore.Qt.ApplicationModal)
            self.dialog.show()

    def insert_widget_progress_status(self, cnt, test_path):
        if self.insert_widget_progress is not None:
            # print(f"{cnt}/{len(self.added_scenario_widgets)}")

            rt = main_widget  # load_module_func(module_name="common.ui_designer.main_widget")
            widget_ui = rt.Ui_Form()
            widget_instance = QtWidgets.QWidget()
            widget_ui.setupUi(widget_instance)

            scenario = os.path.basename(test_path[0])
            widget_ui.scenario_checkBox.setText(f"{scenario}")
            widget_ui.pathlineEdit.setText(f"{test_path[0]}")
            widget_ui.contexts_textEdit.setMinimumHeight(200)
            widget_ui.filelistWidget.addItems(test_path[1])
            # widget_ui.filelistWidget.itemDoubleClicked.connect(self.on_item_double_clicked)
            widget_ui.filelistWidget.itemDoubleClicked.connect(
                lambda item: self.on_item_double_clicked(item, widget_ui))

            self.parent.mainFrame_ui.formLayout.setWidget(cnt, QtWidgets.QFormLayout.FieldRole,
                                                          widget_instance)

            self.added_scenario_widgets.append((widget_ui, widget_instance))
            self.insert_widget_progress.onCountChanged(value=cnt)

            widget_ui.open_terminal_pushButton.hide()

    def finish_insert_widget_progress_status(self):
        if self.insert_widget_progress is not None:
            self.insert_widget_progress.close()
            print(f"총 테스트 할 OP 갯수: {len(self.added_scenario_widgets)}")

    def update_test_result(self, output_result, sub_widget, executed_cnt):

        def highlight_text(output, words_to_highlight):
            output = output.replace("\n", "<br>")
            found_highlight = False
            # HTML 형식으로 텍스트를 변경하기 위한 함수
            for word in words_to_highlight:
                if re.search(f'({re.escape(word)})', output):  # 변환될 단어가 있는지 확인
                    found_highlight = True  # 변환할 단어가 있으면 True로 설정

                # re.escape로 단어에 특수 문자가 있을 경우에도 처리
                output = re.sub(f'({re.escape(word)})', r'<span style="color:red;">\1</span>', output)

            return found_highlight, output

        found_highlight, colored_output_result = highlight_text(output_result, self.user_error_fmt)

        sub_widget[0].contexts_textEdit.setHtml(colored_output_result)

        if found_highlight:
            sub_widget[0].lineEdit.setText("Fail")
        else:
            sub_widget[0].lineEdit.setText("Pass")

        # sub_widget[0].contexts_textEdit.setText(output_result)
        if self.op_analyze_progress is not None:
            self.op_analyze_progress.onCountChanged(value=executed_cnt)

    def error_update_test_result(self, error_message, sub_widget):
        if self.op_analyze_progress is not None:
            self.op_analyze_progress.close()

        sub_widget[0].contexts_textEdit.setText(error_message)
        sub_widget[0].lineEdit.setText("Error")

    def finish_update_test_result(self, normal_stop):
        if self.op_analyze_progress is not None:
            self.op_analyze_progress.close()

            self.end_evaluation_time = time.time()
            elapsed_time = self.end_evaluation_time - self.start_evaluation_time
            days = elapsed_time // (24 * 3600)
            remaining_secs = elapsed_time % (24 * 3600)
            hours = remaining_secs // 3600
            remaining_secs %= 3600
            minutes = remaining_secs // 60
            seconds = remaining_secs % 60

            total_time = f"{int(days)}day {int(hours)}h {int(minutes)}m {int(seconds)}s"
            msg_box = QtWidgets.QMessageBox()

            if normal_stop:
                msg_box.setWindowTitle("Test Done...")
                msg_box.setText(f"All Test Done !\nSave Button to store result data\nElapsed time: {total_time}")
            else:
                msg_box.setWindowTitle("Stop Test...")
                msg_box.setText(f"User forcibly terminated !")

            msg_box.setStandardButtons(QtWidgets.QMessageBox.Yes)
            # Always show the message box on top
            if platform.system() == "Windows":
                msg_box.setWindowFlags(msg_box.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)

            # 메시지 박스를 최상단에 표시
            answer = msg_box.exec_()

    def set_max_progress_cnt(self, max_cnt):
        if self.op_analyze_progress is not None:
            self.op_analyze_progress.setProgressBarMaximum(max_value=max_cnt)

    def stop_analyze(self):
        if self.op_analyze_progress is not None:
            self.op_analyze_progress.close()

        if self.op_analyze_thread is not None:
            self.op_analyze_thread.stop()

    def op_analyze(self, ssh_client=None):
        if self.added_scenario_widgets is None:
            return

        if len(self.added_scenario_widgets) == 0:
            return

        check = False
        for cnt, target_widget in enumerate(self.added_scenario_widgets):
            if target_widget[0].scenario_checkBox.isChecked():
                check = True
                break

        if not check:
            msg_box = QtWidgets.QMessageBox()
            msg_box.setWindowTitle("Check Test Target")
            msg_box.setText(
                "test target directory are required.\nMark target directory")
            msg_box.setStandardButtons(QtWidgets.QMessageBox.Yes)

            if platform.system() == "Windows":
                msg_box.setWindowFlags(msg_box.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)  # 항상 위에 표시

            answer = msg_box.exec_()
            if answer == QtWidgets.QMessageBox.Yes:
                return

        self.start_evaluation_time = time.time()

        if self.parent.mainFrame_ui.popctrl_radioButton.isChecked():
            self.op_analyze_progress = ModalLess_ProgressDialog(message="Analyzing OP Model", show=True)
        else:
            self.op_analyze_progress = Modal_ProgressDialog(message="Analyzing OP Model", show=True)

        self.user_error_fmt = [fmt.strip() for fmt in self.grand_parent.error_lineedit.text().split(",")]

        self.op_analyze_thread = OP_Analyze_Thread(self, self.grand_parent, ssh_client)
        self.op_analyze_thread.output_signal.connect(self.update_test_result)
        self.op_analyze_thread.error_signal.connect(self.error_update_test_result)
        self.op_analyze_thread.send_max_progress_cnt.connect(self.set_max_progress_cnt)

        self.op_analyze_progress.send_user_close_event.connect(self.stop_analyze)
        self.op_analyze_thread.finish_output_signal.connect(self.finish_update_test_result)

        self.op_analyze_thread.start()

        self.op_analyze_progress.showModal_less()

    def select_all_scenario(self, check):
        if self.added_scenario_widgets is None or len(self.added_scenario_widgets) == 0:
            return

        for scenario_widget, scenario_widget_instance in self.added_scenario_widgets:
            scenario_widget.scenario_checkBox.setChecked(check)

    def save_analyze_result(self, BASE_DIR_):

        def save_analyze_result_thread(BASE_DIR_):
            count = 0
            for cnt, target_widget in enumerate(self.added_scenario_widgets):
                if target_widget[0].scenario_checkBox.isChecked():
                    date = GetCurrentDate()
                    pass_fail = target_widget[0].lineEdit.text()
                    test_dir = os.path.basename(target_widget[0].pathlineEdit.text())

                    # html로 저장 (color)
                    filename = f"{date}_{pass_fail}_{test_dir}"

                    test_result = target_widget[0].contexts_textEdit.toHtml()

                    # 파일 경로 설정
                    file_path = os.path.join(BASE_DIR_, filename)

                    save2html(file_path=file_path, data=test_result)

                    test_result = target_widget[0].contexts_textEdit.toPlainText()
                    file_path = os.path.join(BASE_DIR_, filename)
                    save2txt(file_path=file_path, data=test_result)

                    count += 1
                    self.op_result_save_progress.onCountChanged(value=count)

        if self.added_scenario_widgets is None or len(self.added_scenario_widgets) == 0:
            return

        count = 0
        for cnt, target_widget in enumerate(self.added_scenario_widgets):
            if target_widget[0].scenario_checkBox.isChecked():
                count += 1
        if count == 0:
            return

        if self.parent.mainFrame_ui.popctrl_radioButton.isChecked():
            self.op_result_save_progress = ModalLess_ProgressDialog(message="Saving Result")
        else:
            self.op_result_save_progress = Modal_ProgressDialog(message="Saving Result")

        self.op_result_save_progress.setProgressBarMaximum(max_value=count)

        self.result_thread = threading.Thread(target=save_analyze_result_thread, args=(BASE_DIR_,), daemon=True)
        self.result_thread.start()

        self.op_result_save_progress.showModal_less()
        self.op_result_save_progress.close()

        msg_box = QtWidgets.QMessageBox()  # QMessageBox 객체 생성
        msg_box.setWindowTitle("Save Result")  # 대화 상자 제목
        msg_box.setText(
            "All test result are saved.               \n")
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Yes)  # Yes/No 버튼 추가

        if platform.system() == "Windows":
            msg_box.setWindowFlags(msg_box.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)  # 항상 위에 표시

        answer = msg_box.exec_()  # 대화 상자를 실행하고 사용자의 응답을 반환
