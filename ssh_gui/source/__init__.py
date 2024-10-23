import os
import subprocess
import json
import chardet
from collections import OrderedDict
from datetime import datetime
import platform
import socket
import paramiko
import tkinter as tk
from tkinter import messagebox, ttk

from PyQt5.QtCore import pyqtSignal, QTimer, Qt

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar, QPushButton, QHBoxLayout, QSpacerItem, \
    QSizePolicy, QRadioButton, QWidget, QMessageBox

from langchain_community.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_text_splitters import CharacterTextSplitter

Version = "Single OP Verifier ver.0.1.0 (made by tom.shin)"

keyword_ctrl = {
    "target_format": [".yaml", ".md"],
    "error_keyword": ["error", "Error", "fail", "Fail", "Fault", "fault", "segmentation", "Fault", "ERROR"],
    "op_exe_cmd": ["enntools init", "enntools conversion"],
    "exclusive_dir": ["DATA"]
}

ssh_server_information = {
    "serverip": "1.220.53.154",
    "port": "63522",
    "username": "sam",
    "password": "Thunder$@88"
}


class ModalLess_ProgressDialog(QWidget):  # popup 메뉴가 있어도 뒤 main gui의 제어가 가능 함
    send_user_close_event = pyqtSignal(bool)

    def __init__(self, message, show=False, parent=None):
        super().__init__(parent)
        self.setWindowTitle(message)

        self.resize(400, 100)  # 원하는 크기로 조절

        self.progress_bar = QProgressBar(self)
        self.label = QLabel("", self)
        self.close_button = QPushButton("Close", self)
        self.radio_button = QRadioButton("", self)

        # Create a horizontal layout for the close button and spacer
        h_layout = QHBoxLayout()
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        h_layout.addSpacerItem(spacer)
        h_layout.addWidget(self.close_button)

        # Create the main layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.label)
        layout.addWidget(self.radio_button)
        layout.addLayout(h_layout)
        self.setLayout(layout)

        # Close 버튼 클릭 시 다이얼로그를 닫음
        self.close_button.clicked.connect(self.close)

        if show:
            self.close_button.show()
        else:
            self.close_button.hide()

        # Timer 설정
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.toggle_radio_button)
        self.timer.start(500)  # 500ms 간격으로 토글

        self.radio_state = False  # 깜빡임 상태 초기화

    def setProgressBarMaximum(self, max_value):
        self.progress_bar.setMaximum(int(max_value))

    def onCountChanged(self, value):
        self.progress_bar.setValue(int(value))

    def onProgressTextChanged(self, text):
        self.label.setText(text)

    def showModal_less(self):
        self.showModal()

    def showModal(self):
        self.show()

    def closeEvent(self, event):
        subprocess.run("taskkill /f /im cmd.exe /t", shell=True)

        self.send_user_close_event.emit(True)
        event.accept()

    def toggle_radio_button(self):
        if self.radio_state:
            self.radio_button.setStyleSheet("""
                        QRadioButton::indicator {
                            width: 12px;
                            height: 12px;
                            background-color: red;
                            border-radius: 5px;
                        }
                    """)
        else:
            self.radio_button.setStyleSheet("""
                        QRadioButton::indicator {
                            width: 12px;
                            height: 12px;
                            background-color: blue;
                            border-radius: 5px;
                        }
                    """)
        self.radio_state = not self.radio_state


class Modal_ProgressDialog(QDialog):  # popup 메뉴가 있으면 뒤 main gui의 제어 불 가능 -> modal
    send_user_close_event = pyqtSignal(bool)

    def __init__(self, message, show=False, parent=None):
        super().__init__(parent)
        self.setWindowTitle(message)
        self.setModal(True)

        self.resize(400, 100)  # 원하는 크기로 조절

        self.progress_bar = QProgressBar(self)
        self.label = QLabel("", self)
        self.close_button = QPushButton("Close", self)
        self.radio_button = QRadioButton("", self)

        # Create a horizontal layout for the close button and spacer
        h_layout = QHBoxLayout()
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        h_layout.addSpacerItem(spacer)
        h_layout.addWidget(self.close_button)

        # Create the main layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.label)
        layout.addWidget(self.radio_button)
        layout.addLayout(h_layout)
        self.setLayout(layout)

        # Close 버튼 클릭 시 다이얼로그를 닫음
        self.close_button.clicked.connect(self.close)

        if show:
            self.close_button.show()
        else:
            self.close_button.hide()

        # Timer 설정
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.toggle_radio_button)
        self.timer.start(500)  # 500ms 간격으로 토글

        self.radio_state = False  # 깜빡임 상태 초기화

    def setProgressBarMaximum(self, max_value):
        self.progress_bar.setMaximum(int(max_value))

    def onCountChanged(self, value):
        self.progress_bar.setValue(int(value))

    def onProgressTextChanged(self, text):
        self.label.setText(text)

    def showModal(self):
        super().exec_()

    def showModal_less(self):
        super().show()

    def closeEvent(self, event):
        self.send_user_close_event.emit(True)
        event.accept()

    def toggle_radio_button(self):
        if self.radio_state:
            self.radio_button.setStyleSheet("""
                        QRadioButton::indicator {
                            width: 12px;
                            height: 12px;
                            background-color: red;
                            border-radius: 5px;
                        }
                    """)
        else:
            self.radio_button.setStyleSheet("""
                        QRadioButton::indicator {
                            width: 12px;
                            height: 12px;
                            background-color: blue;
                            border-radius: 5px;
                        }
                    """)
        self.radio_state = not self.radio_state


def json_dump_f(file_path, data, use_encoding=False):
    if file_path is None:
        return False

    if not file_path.endswith(".json"):
        file_path += ".json"

    if use_encoding:
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
            encoding = result['encoding']
    else:
        encoding = "utf-8"

    with open(file_path, "w", encoding=encoding) as f:
        json.dump(data, f, indent=4, ensure_ascii=False, sort_keys=False)

    return True


def json_load_f(file_path, use_encoding=False):
    if file_path is None:
        return False, False

    if use_encoding:
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
            encoding = result['encoding']
    else:
        encoding = "utf-8"

    with open(file_path, "r", encoding=encoding) as f:
        json_data = json.load(f, object_pairs_hook=OrderedDict)

    return True, json_data


def load_markdown(data_path):
    with open(data_path, 'rb') as f:
        result = chardet.detect(f.read())
        encoding = result['encoding']

    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
        ("####", "Header 4"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on
    )

    with open(data_path, 'r', encoding=encoding) as file:
        print(data_path)
        data_string = file.read()
        documents = markdown_splitter.split_text(data_string)

        # 파일명을 metadata에 추가
        domain = data_path  # os.path.basename(data_path)
        for doc in documents:
            if not doc.metadata:
                doc.metadata = {}
            doc.metadata["domain"] = domain  # Document 객체의 metadata 속성에 파일명 추가

        return documents

    # with open(data_path, 'r') as file:
    #     data_string = file.read()
    #     return markdown_splitter.split_text(data_string)


def load_txt(data_path):
    with open(data_path, 'rb') as f:
        result = chardet.detect(f.read())
        encoding = result['encoding']

    text_splitter = CharacterTextSplitter(
        separator="\n",
        length_function=len,
        is_separator_regex=False,
    )

    with open(data_path, 'r', encoding=encoding) as file:
        data_string = file.read().split("\n")
        domain = data_path  # os.path.basename(data_path)
        documents = text_splitter.create_documents(data_string)

        for doc in documents:
            if not doc.metadata:
                doc.metadata = {}
            doc.metadata["domain"] = domain  # Document 객체의 metadata 속성에 파일명 추가

        return documents
    # with open(data_path, 'r') as file:
    #     data_string = file.read().split("\n")
    #     domain = os.path.splitext(os.path.basename(data_path))[0]
    #     metadata = [{"domain": domain} for _ in data_string]
    #     return text_splitter.create_documents(
    #         data_string,
    #         metadata
    #     )


def load_general(base_dir):
    data = []
    cnt = 0
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                if os.path.getsize(file_path) > 0:
                    cnt += 1
                    data += load_txt(file_path)

    print(f"the number of txt files is : {cnt}")
    return data


def load_document(base_dir):
    data = []
    cnt = 0
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                if os.path.getsize(file_path) > 0:
                    cnt += 1
                    data += load_markdown(file_path)

    print(f"the number of md files is : {cnt}")
    return data


def X_get_markdown_files(source_dir):
    dir_ = source_dir
    loader = DirectoryLoader(dir_, glob="**/*.md", loader_cls=UnstructuredMarkdownLoader)
    documents = loader.load()
    print("number of doc: ", len(documents))
    return documents


def get_directory_for_verification(ssh_client=None, base_dir=None, grand_parent=None, user_defined_fmt=None,
                                   BASE_DIR=None):
    base_dir = base_dir.directory

    if ssh_client is not None:

        module_path = os.path.join(BASE_DIR, "source", "os_walk.py").replace("\\", "/")

        target = [item.strip() for item in grand_parent.targetformat_lineedit.text().split(",") if item.strip()]
        error = [item.strip() for item in grand_parent.error_lineedit.text().split(",") if item.strip()]
        op_cmd = [item.strip() for item in grand_parent.command_lineedit.text().split(",") if item.strip()]
        exclusive_dir = [item.strip() for item in grand_parent.exclusivelineEdit.text().split(",") if item.strip()]

        keyword_ctrl = {
            "target_format": target,
            "error_keyword": error,
            "op_exe_cmd": op_cmd,
            "exclusive_dir": exclusive_dir
        }

        modified_lines = []
        with open(module_path, 'r', encoding='utf-8') as file:
            for line in file:
                # 특정 문자열을 찾아서 변경
                if "user_defined_root_path" in line:
                    modified_line = line.replace("user_defined_root_path", str(base_dir))
                    modified_lines.append(modified_line)
                elif "user_defined_keyword_ctrl" in line:
                    # replace_string = f'{{"target_format": [".yaml"], "error_keyword": ["error", "Error", "fail", "Fail", "Fault", "fault", "segmentation", "Fault", "ERROR"], "op_exe_cmd": ["enntools init", "enntools conversion"], "exclusive_dir": ["DATA"]}}'
                    #
                    # modified_line = line.replace("user_defined_keyword_ctrl", str(replace_string.strip("'")))
                    #
                    # modified_lines.append(modified_line)
                    modified_lines.append(f"keyword_ctrl = {keyword_ctrl}\n")
                else:
                    modified_lines.append(line)

        target_dir = os.path.join(base_dir, "os_walk.py").replace("\\", "/")
        with ssh_client.get_ssh_instance().open_sftp().open(target_dir, 'w') as remote_file:
            for line in modified_lines:
                remote_file.write(line)

        # print(f"os_walk.py is pushed to {target_dir}")
        # .py 파일 실행
        command = f"python3 {target_dir}"
        stdin, stdout, stderr = ssh_client.get_ssh_instance().exec_command(command)

        # 출력 결과 받기
        output = stdout.read().decode()  # 출력 값을 가져옴
        error = stderr.read().decode()

        if output:
            # 출력된 값에서 줄바꿈 기준으로 분리하여 리스트로 변환
            verification_paths = output.strip().split('\n')
            # print("Matched directories:", verification_paths)
            return verification_paths

        if error:
            print("Errors:\n", error)

    else:
        data = set()
        for root, dirs, files in os.walk(base_dir):

            if "DATA" in dirs:
                dirs.remove("DATA")

            for file in files:
                if user_defined_fmt is None:
                    if any(file.endswith(ext) for ext in keyword_ctrl["target_format"]):
                        data.add(root)
                else:
                    if any(file.endswith(ext) for ext in user_defined_fmt):
                        data.add(root)

        unique_paths = list(data)
        return unique_paths


def GetCurrentDate():
    current_date = datetime.now()

    # 날짜 형식 지정 (예: YYYYMMDD)
    formatted_date = current_date.strftime("%Y%m%d")

    return formatted_date


def save2html(file_path, data, use_encoding=False):
    if file_path is None:
        return False

    if not file_path.endswith(".html"):
        file_path += ".html"

    if use_encoding:
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
            encoding = result['encoding']
    else:
        encoding = "utf-8"

    with open(file_path, "w", encoding=encoding) as f:
        f.write(data)

    # print("Saved as HTML text.")


def save2txt(file_path, data, use_encoding=False):
    if file_path is None:
        return False

    if not file_path.endswith(".txt"):
        file_path += ".txt"

    if use_encoding:
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
            encoding = result['encoding']
    else:
        encoding = "utf-8"

    with open(file_path, "w", encoding=encoding) as f:
        f.write(data)

    # print("Saved as TEXT.")


def Checking_Directory(path_=None):
    dir_ = os.path.join(path_, "Result")
    if not os.path.exists(dir_):
        os.makedirs(dir_)


class SSH_Ctrl_Class:
    def __init__(self, ip, port, username, pwd):
        self.ip = ip
        self.port = port
        self.username = username
        self.pwd = pwd

        self.ssh = None
        self.initial_path = '/home/sam'

    def get_ssh_instance(self):
        return self.ssh

    def _ssh_connect(self, ip, port, username, password, timeout):

        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(hostname=ip, port=port, username=username, password=password, timeout=timeout)
            print(f"Successfully connected to the server.")
            return True

        except paramiko.AuthenticationException:
            print("Authentication failed")
        except paramiko.SSHException as sshException:
            print(f"SSH error: {sshException}")
        except socket.timeout:
            print("Connection timed out")
        except Exception as e:
            print(f"Other error: {e}")

        if self.ssh:
            # print("Closing previous connection.")
            self.ssh.close()
            self.ssh = None

        return False

    def ssh_connect(self):
        check = False

        if self.ssh is not None:
            self.ssh.close()
            self.ssh = None

        ret = self._ssh_connect(ip=self.ip, port=self.port, username=self.username, password=self.pwd, timeout=30)

        msg_box = QMessageBox()
        msg_box.setWindowTitle("Notification...")

        if ret:
            msg_box.setText(f"Successfully connected to the server.")
            check = True
        else:
            msg_box.setText(f"Connection Failed.")

        msg_box.setStandardButtons(QMessageBox.Yes)

        if platform.system() == "Windows":
            msg_box.setWindowFlags(msg_box.windowFlags() | Qt.WindowStaysOnTopHint)

        answer = msg_box.exec_()

        return check

    def ssh_disconnect(self):
        if self.ssh is not None:
            self.ssh.close()
            self.ssh = None

            return True

    def ssh_cmd_execution(self, cmd):
        if self.ssh is None:
            print("SSH Not Connected.")
            return False, None, None

        try:
            stdin, stdout, stderr = self.ssh.exec_command(cmd)
            stdout.channel.recv_exit_status()  # Wait for the command to complete
            output = stdout.read().decode()
            error = stderr.read().decode()

            if error:
                print("Devices Error:", error)

            return True, output, error

        except Exception as e:
            print(f"An error occurred: {e}")
            return False, None, str(e)

    def ssh_remote_diropenbox(self):
        """Open a dialog box to select a remote directory, starting from the initial path."""
        current_path = self.initial_path  # SSH 연결 후 초기 경로 설정
        selected_directory = None
        root = tk.Tk()
        root.title("Select a Directory")

        def on_select(event):
            nonlocal current_path
            selected_item = tree.selection()
            if selected_item:
                selected_directory = tree.item(selected_item)['text']
                if selected_directory == '..':
                    # 상위 디렉토리로 이동
                    new_path = os.path.dirname(current_path.rstrip('/'))
                    if new_path != current_path:  # 상위 디렉토리가 존재하는지 확인
                        current_path = new_path + '/'
                        update_tree()
                else:
                    # 하위 디렉토리로 이동
                    current_path = f"{current_path}/{selected_directory}/"  # 수정된 부분
                    update_tree()

        def update_tree():
            tree.delete(*tree.get_children())
            sftp = self.ssh.open_sftp()
            try:
                # 디렉토리 목록 가져오기
                directory_list = sftp.listdir(current_path)

                # 디렉토리만 필터링
                directories_only = []
                for item in directory_list:
                    try:
                        # 항목의 상태를 확인하여 디렉토리인지 확인
                        item_stat = sftp.stat(f"{current_path}/{item}")
                        if item_stat.st_mode & 0o40000:  # 디렉토리인지 체크
                            directories_only.append(item)
                    except Exception as e:
                        print(f"Error checking {item}: {e}")  # 오류 처리 (필요시 로그로 남김)

                if current_path != '/':  # 루트가 아닐 때만 '..' 추가
                    tree.insert('', 'end', '..', text='..')

                for directory in directories_only:
                    tree.insert('', 'end', directory, text=directory)
            except Exception as e:
                messagebox.showerror("Error", f"Error accessing directory: {e}")
            finally:
                sftp.close()

        def on_select_confirm():
            # 현재 full 경로인 current_path를 사용하여 판단
            if current_path and current_path != '/':
                root.quit()  # 창 종료
                root.destroy()  # 창을 완전히 종료
            else:
                messagebox.showwarning("Warning", "Please select a valid directory.")

        def on_cancel():
            nonlocal selected_directory
            selected_directory = None
            root.quit()  # 창 종료
            root.destroy()  # 창을 완전히 종료

        frame = ttk.Frame(root)
        frame.pack(fill='both', expand=True)

        tree = ttk.Treeview(frame)
        tree.pack(fill='both', expand=True)
        tree.bind('<<TreeviewSelect>>', on_select)

        update_tree()

        button_frame = ttk.Frame(root)
        button_frame.pack(fill='x')

        select_button = ttk.Button(button_frame, text="Select", command=on_select_confirm)
        select_button.pack(side='left', padx=5, pady=5)

        cancel_button = ttk.Button(button_frame, text="Cancel", command=on_cancel)
        cancel_button.pack(side='right', padx=5, pady=5)

        root.mainloop()  # 메인 루프 시작

        if current_path and current_path != '/':
            return current_path.replace("//", "/")
        else:
            return None

    def get_os_walk_dir(self):
        # /home/sam/tom/
        command = "python3 /home/sam/tom/os_walk.py"
        stdin, stdout, stderr = self.ssh.exec_command(command)

        # 출력 결과 받기
        output = stdout.read().decode()
        error = stderr.read().decode()

        # 결과 출력
        print(">>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<")
        if output:
            print("Matched directories:\n", output)
        if error:
            print("Errors:\n", error)
