#!/usr/bin/env python3

import re
import sys
import os
import subprocess
from datetime import datetime
import platform
import time
# from tqdm import tqdm

KEYWORD_CTRL = {
    "target_format": [".yaml"],
    # 만약 [Error 처럼 표현된다고 하면 아래 키워드 등록을 [Error 로 해야 한다. 즉 아래 등록된 키워드와 완전 동일할 때 에러 표시가 된다.
    "error_keyword": ["[Error]", "Fail", "segmentation", "ERROR"],
    "op_exe_cmd": ["enntools init", "enntools conversion"],
    "exclusive_dir": ["DATA"]
}

# ANSI 코드 정규식 패턴 (터미널 컬러 코드)
ANSI_ESCAPE = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')

# RTF 헤더 및 색상 테이블
RTF_HEADER = r"{\rtf1\ansi\deff0{\fonttbl{\f0 Courier;}}\n{\colortbl ;\red255\green0\blue0;\red0\green0\blue255;\red0\green255\blue0;\red255\green255\blue0;\red255\green0\blue255;\red0\green255\blue255;\red255\green255\blue255;\red128\green128\blue128;\red255\green0\blue0;\red0\green255\blue0;\red255\green255\blue0;\red0\green0\blue255;\red255\green0\blue255;\red0\green255\blue255;\red255\green255\blue255;}\n"
RTF_FOOTER = r"}"


def is_exe():
    return hasattr(sys, 'frozen')


def is_dot_slash():
    return os.path.dirname(os.path.abspath(sys.executable)) == os.getcwd()


# BASE_DIR 설정
if platform.system() == 'Windows' and is_exe():
    BASE_DIR = os.path.dirname(os.path.abspath(sys.executable))
elif platform.system() == 'Linux' and is_dot_slash():
    BASE_DIR = os.getcwd()
elif is_exe():
    BASE_DIR = os.path.dirname(os.path.abspath(sys.executable))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class op_ctrl_class:
    def __init__(self, root_dir):
        self.base = root_dir
        self.target_dirs = None
        self.result_output = None
        self.fail_cnt = 0
        self.pass_cnt = None
        self.total_cnt = None

    def open_target_dir(self):
        data = set()
        for root, dirs, files in os.walk(self.base):
            for exclusive in KEYWORD_CTRL["exclusive_dir"]:
                if exclusive in dirs:
                    dirs.remove(exclusive)
            for file in files:
                if any(file.endswith(ext) for ext in KEYWORD_CTRL["target_format"]):
                    data.add(root)                    
        self.target_dirs = list(data)        

    def op_analyze(self):
        self.fail_cnt = []
        self.pass_cnt = []
        self.total_cnt = len(self.target_dirs)

        # for cnt_s, cwd in tqdm(enumerate(self.target_dirs), total=self.total_cnt, desc="Processing directories"):
        for cnt_s, cwd in enumerate(self.target_dirs):
            output_list = []
            for cmd in KEYWORD_CTRL["op_exe_cmd"]:
                try:
                    process = subprocess.run(
                        cmd,
                        cwd=cwd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        shell=True,
                        check=True,
                    )
                    if process.stdout:
                        # print(process.stdout.strip())
                        output_list.append(process.stdout.strip())

                except subprocess.CalledProcessError as e:
                    print(f"[Error] {cmd} Command failed: {str(e)}")
                except Exception as e:
                    print(f"[Error] Exception: {str(e)}")

            self.result_format_change_and_save(work_dir=cwd, result_output=output_list)
            print(f"Processing directories: {cnt_s+1}/{self.total_cnt}")


    def op_summary(self, elapsed_T=None):
        current_date = datetime.now().strftime("%Y%m%d")
        summary_path = os.path.join(BASE_DIR, "Result")       

        summary = [
            f"\n================= Result Summary [Elapsed time: {elapsed_T}] =================",
            f"total test: {self.total_cnt}",
            f"total pass: {len(self.pass_cnt)}",
            f"total fail: {len(self.fail_cnt)}",
            f"\n================= Result Pass Item =================",
            f"\n================= Result Fail Item =================\n"
        ]

        with open(os.path.join(summary_path, f"Summary_{current_date}.txt"), "w", encoding="utf-8") as f:
            for line in summary:
                print(line + "\n")  # Write each line to the file
                f.write(line + "\n")  # Write each line to the file
                f.flush()  # Ensure it's written to disk immediately

                if "Pass Item" in line:
                    for item in self.pass_cnt:
                        print(item + "\n")  # Write each line to the file
                        f.write(item + "\n")  # Write each line to the file
                        f.flush()  # Ensure it's written to disk immediately

                elif "Fail Item" in line:
                    for item in self.fail_cnt:
                        print(item + "\n")  # Write each line to the file
                        f.write(item + "\n")  # Write each line to the file
                        f.flush()  # Ensure it's written to disk immediately
                
                else:
                    continue
            

    def result_format_change_and_save(self, work_dir, result_output):
        current_date = datetime.now().strftime("%Y%m%d")
        filename = f"{current_date}_{os.path.basename(work_dir)}"
        dir_path = os.path.join(BASE_DIR, "Result")

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # Save as text file (ANSI 컬러 코드 제거)
        r_data, key_found = self.conver2txt(result_output)
        if key_found:
            text_filename = filename + "_fail.txt"
        else:
            text_filename = filename + "_pass.txt"

        with open(os.path.join(dir_path, text_filename), "w", encoding="utf-8") as f:
            f.write(r_data)

        # Save as HTML file (HTML 스타일로 변환)
        r_data, key_found = self.convert_ansi_to_html(result_output)
        if key_found:
            self.fail_cnt.append(filename)
            html_filename = filename + "_fail.html"
        else:
            self.pass_cnt.append(filename)
            html_filename = filename + "_pass.html"

        with open(os.path.join(dir_path, html_filename), "w", encoding="utf-8") as f:
            f.write(r_data)

        # # Save as RTF file (RTF 스타일로 변환)
        # rtf_filename = filename + ".rtf"
        # with open(os.path.join(dir_path, rtf_filename), "w", encoding="utf-8") as f:
        #     f.write(self.convert_ansi_to_rtf(result_output))

    @staticmethod
    def conver2txt(result_output):
        # ANSI 코드 제거하여 텍스트 파일로 저장
        stripped_output = []
        keyword_found = False  # 키워드 발견 여부를 추적하는 플래그

        for sentence in result_output:
            # ANSI 코드 제거
            cleaned_sentence = ANSI_ESCAPE.sub('', sentence)
            stripped_output.append(cleaned_sentence)

            # 키워드가 존재하는지 확인
            for keyword in KEYWORD_CTRL["error_keyword"]:
                pattern = r'\b' + re.escape(keyword) + r'\b'  # \b는 단어 경계를 의미
                if re.search(pattern, cleaned_sentence):  # 키워드가 존재하는지 검사
                    keyword_found = True  # 키워드가 발견되었음을 표시
                    break  # 한 번 발견하면 더 이상 검사할 필요 없음

        return "\n".join(stripped_output), keyword_found


    @staticmethod
    def convert_ansi_to_html(result_output):
        # ANSI 코드를 HTML 스타일로 변환
        html_output = "<html><body>\n"
        for sentence in result_output:
            # ANSI 코드 제거 및 변환
            modified_sentence = ANSI_ESCAPE.sub(lambda match: ansi_to_html(match.group()), sentence)

            # 키워드 강조 처리 (정확한 매치 사용)
            keyword_found = False
            for keyword in KEYWORD_CTRL["error_keyword"]:
                # 정규 표현식을 사용하여 키워드가 완전한 단어로만 존재하는지 검사
                pattern = r'\b' + re.escape(keyword) + r'\b'  # \b는 단어 경계를 의미

                if re.search(pattern, modified_sentence):
                    keyword_found = True
                    modified_sentence = re.sub(pattern, f'<span style="color: red; font-weight: bold;">{keyword}</span>', modified_sentence)

            html_output += f"<pre>{modified_sentence}</pre>\n"
        html_output += "</body></html>"
        return html_output, keyword_found

    @staticmethod
    def convert_ansi_to_rtf(result_output):
        # ANSI 코드를 RTF 스타일로 변환
        rtf_output = RTF_HEADER
        for sentence in result_output:
            modified_sentence = ANSI_ESCAPE.sub(lambda match: ansi_to_rtf(match.group()), sentence)
            rtf_output += f"{modified_sentence}\\par\n"
        rtf_output += RTF_FOOTER
        return rtf_output


def ansi_to_html(ansi_code):
    # ANSI 코드를 HTML 스타일로 변환하는 함수
    color_map = {
        '30': 'black',
        '31': 'red',
        '32': 'green',
        '33': 'yellow',
        '34': 'blue',
        '35': 'magenta',
        '36': 'cyan',
        '37': 'white',
        '90': 'bright black',
        '91': 'bright red',
        '92': 'bright green',
        '93': 'bright yellow',
        '94': 'bright blue',
        '95': 'bright magenta',
        '96': 'bright cyan',
        '97': 'bright white'
    }
    for code, color in color_map.items():
        if code in ansi_code:
            return f'<span style="color: {color};">'
    if ansi_code == '\x1b[0m':  # 리셋
        return '</span>'
    return ''


def ansi_to_rtf(ansi_code):
    # ANSI 코드를 RTF 스타일로 변환하는 함수
    color_map = {
        '30': '\\cf0 ',  # 검정
        '31': '\\cf1 ',  # 빨강
        '32': '\\cf3 ',  # 초록
        '33': '\\cf4 ',  # 노랑
        '34': '\\cf2 ',  # 파랑
        '35': '\\cf5 ',  # 자주
        '36': '\\cf6 ',  # 청록
        '37': '\\cf7 ',  # 흰색
        '90': '\\cf8 ',  # 밝은 검정
        '91': '\\cf9 ',  # 밝은 빨강
        '92': '\\cf10 ',  # 밝은 초록
        '93': '\\cf11 ',  # 밝은 노랑
        '94': '\\cf12 ',  # 밝은 파랑
        '95': '\\cf13 ',  # 밝은 자주
        '96': '\\cf14 ',  # 밝은 청록
        '97': '\\cf15 '  # 밝은 흰색
    }
    for code, rtf_color in color_map.items():
        if code in ansi_code:
            return rtf_color
    if ansi_code == '\x1b[0m':  # 리셋
        return ''
    return ''


def main():
    start_evaluation_time = time.time()

    result_dir = os.path.join(BASE_DIR, "Result")
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    ctrl = op_ctrl_class(BASE_DIR)
    ctrl.open_target_dir()
    ctrl.op_analyze()

    end_evaluation_time = time.time()
    elapsed_time = end_evaluation_time - start_evaluation_time
    days = elapsed_time // (24 * 3600)
    remaining_secs = elapsed_time % (24 * 3600)
    hours = remaining_secs // 3600
    remaining_secs %= 3600
    minutes = remaining_secs // 60
    seconds = remaining_secs % 60
    total_time = f"{int(days)}day {int(hours)}h {int(minutes)}m {int(seconds)}s"

    ctrl.op_summary(elapsed_T=total_time)


if __name__ == '__main__':
    main()
