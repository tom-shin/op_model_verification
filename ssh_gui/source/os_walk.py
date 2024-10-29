import os

# keyword_ctrl = {
#     "target_format": [".yaml", ".md"],
#     "error_keyword": ["error", "Error", "fail", "Fail", "Fault", "fault", "segmentation", "Fault", "ERROR"],
#     "op_exe_cmd": ["enntools init", "enntools conversion"],
#     "exclusive_dir": ["DATA"]
# }

"user_defined_keyword_ctrl"


def get_directory_for_verification(base_dir, user_defined_fmt=None):
    data = {}

    for root, dirs, files in os.walk(base_dir):

        # 'DATA' 폴더가 있으면 dirnames에서 제거하여 탐색하지 않음
        for exclusive in keyword_ctrl["exclusive_dir"]:
            if exclusive in dirs:
                dirs.remove(exclusive)

        # 파일 확장자에 해당하는 파일이 있으면 경로와 파일을 저장
        matched_files = []
        for file in files:
            if user_defined_fmt is None:
                if any(file.endswith(ext) for ext in keyword_ctrl["target_format"]):
                    matched_files.append(file)
            else:
                if any(file.endswith(ext) for ext in user_defined_fmt):
                    matched_files.append(file)

        # If there are matched files, add the root and files to data
        if matched_files:
            data[root] = matched_files

    # Convert data to sorted list of unique paths with matched files
    unique_paths = sorted(data.items())  # Each item is (root, [list of files])
    return unique_paths


def X_get_directory_for_verification(base_dir, user_defined_fmt=None):
    data = set()

    for root, dirs, files in os.walk(base_dir):

        # 'DATA' 폴더가 있으면 dirnames에서 제거하여 탐색하지 않음
        for exclusive in keyword_ctrl["exclusive_dir"]:
            if exclusive in dirs:
                dirs.remove(exclusive)

        # 파일 확장자에 해당하는 파일이 있으면 경로 저장
        for file in files:
            if user_defined_fmt is None:
                if any(file.endswith(ext) for ext in keyword_ctrl["target_format"]):
                    data.add(root)
            else:
                if any(file.endswith(ext) for ext in user_defined_fmt):
                    data.add(root)

        # 중복을 제거한 후 경로들을 정렬
    unique_paths = sorted(list(data))  # 경로를 정렬
    return unique_paths


# 디렉토리 경로 지정
base_directory = 'user_defined_root_path'  # 필요에 따라 변경

# 함수 실행
verification_paths = get_directory_for_verification(base_directory)
for path in verification_paths:
    print(path)
