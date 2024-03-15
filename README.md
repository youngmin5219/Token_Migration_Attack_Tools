# Token_Migration_Attack_Tools
- **attack.exe**
  - victim 기기에 최초 접근 시 실행되는 실행파일
  - victim의 Onedrive 폴더 내에 Startup 폴더를 junction으로 연결, token_extractor_startup 프로그램을 Startup 폴더 내에 저장
  - token_extractor_portable.exe, token_extractor_startup 실행
- **token_extractor_startup.exe**
  - 백그라운드에서 실행, 일정 시간 간격으로 실행되는 공격 프로그램
  - Onedrive wlid token을 DPAPI decrypt해서 Onedrive 'data'폴더에 업로드
  - victim의 Onedrive 폴더 내에 Startup, data folder가 있는지 확인하고 사리진 경우 새롭게 생성
  - victim의 기기 내에 저장되어있는 ms 계정 리스트업해서 username.txt 형태로 victim's onedrive에 저장
- **token_extractor_portable.exe**
  - victim의 local에 저장되어 있는 wlid token을 dpapi decrypt해서 usb에 저장
  - victim의 기기 내에 저장되어있는 ms 계정 리스트업해서 username.txt 형태로 usb에 저장
- **token_spoofer_portable.exe**
  - usb에 있는 wlid token data를 공격자 기기에 이식
- **token_spoofer_local.exe**
  - 공격자 기기 로컬에 저장되어 있는 token_spoofer.exe
  - Onedrive에 저장되어있는 갱신된 wlid token을 공격자 로컬에 이식
  

