import os
import subprocess
from datetime import datetime
import sys

if getattr(sys, 'frozen', False):    
    BASE_EXE = os.path.dirname(sys.executable)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# keyword_ctrl = {
#     "target_format": [".yaml"],
#     "error_keyword": ["error", "Error", "fail", "Fail", "Fault", "fault", "segmentation"],
#     "op_exe_cmd": ["enntools init", "enntools conversion"]
# }

keyword_ctrl = {
    "target_format": [".md"],
    "error_keyword": ["error", "Error", "fail", "Fail", "Fault", "fault", "segmentation", "converter", "dataset_and_model"],
    "op_exe_cmd": ["dir"]
}


class op_ctrl_class:
    def __init__(self, root_dir):
        self.base = root_dir
        self.target_dirs = None
        self.result_output = None

    def open_target_dir(self):
        data = set()
        for root, dirs, files in os.walk(self.base):
            for file in files:
                if any(file.endswith(ext) for ext in keyword_ctrl["target_format"]):
                    data.add(root)

        self.target_dirs = list(data)

    def op_analyze(self):
        for cwd in self.target_dirs:
            output_list = []
            for cmd in keyword_ctrl["op_exe_cmd"]:
                try:                    
                    # Run the command using subprocess.run
                    process = subprocess.run(
                        cmd,
                        cwd=cwd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        shell=True,
                        check=True,
                    )

                    # Print and store output if it exists
                    if process.stdout:
                        print(process.stdout.strip())
                        output_list.append(process.stdout.strip())

                    # Print errors if they exist
                    if process.stderr:
                        print(f"[Error] cmd {cmd} error: {process.stderr.strip()}")

                except subprocess.CalledProcessError as e:
                    print(f"[Error] {cmd} Command failed: {str(e)}")
                except Exception as e:
                    print(f"[Error] Exception: {str(e)}")

            self.result_format_change_and_save(work_dir=cwd, result_output=output_list)

    @staticmethod
    def result_format_change_and_save(work_dir, result_output):
        current_date = datetime.now().strftime("%Y%m%d")
        filename = f"{current_date}_{os.path.basename(work_dir)}"

        if getattr(sys, 'frozen', False):    
            dir_path = os.path.join(BASE_EXE, "Result")
        else:
            dir_path = os.path.join(BASE_DIR, "Result")

        text_filename = filename + ".txt"
        with open(os.path.join(dir_path, text_filename), "w", encoding="utf-8") as f:
            f.write("\n".join(result_output))

        html_filename = filename + ".html"
        html_output = "<html><body>\n"
        for sentence in result_output:
            modified_sentence = sentence

            for keyword in keyword_ctrl["error_keyword"]:
                if keyword in sentence:
                    modified_sentence = modified_sentence.replace(keyword,
                                                                  f'<span style="color: red;">{keyword}</span>')

            html_output += f"<pre>{modified_sentence}</pre>\n"

        html_output += "</body></html>"

        with open(os.path.join(dir_path, html_filename), "w", encoding="utf-8") as f:
            f.write(html_output)


def main():
    if getattr(sys, 'frozen', False):    
        result_dir = os.path.join(BASE_EXE, "Result")
    else:
        result_dir = os.path.join(BASE_DIR, "Result")

    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    ctrl = op_ctrl_class(BASE_DIR)
    ctrl.open_target_dir()
    ctrl.op_analyze()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
