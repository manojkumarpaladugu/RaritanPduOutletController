Install below PIP packages:
  pip3 install raritan
  pip3 install customtkinter
  pip3 install pyinstaller

Convert python script into windows executable:
  1. Open PowerShell window here
  2. Copy pyinstaller path from the output of "pip3 show pyinstaller"
  3. pyinstaller --noconfirm --onefile --windowed --icon=app\PlugSocket.ico --add-data "c:\users\<username>\appdata\local\programs\python\python39\lib\site-packages\customtkinter;customtkinter\" 'RaritanPduOutletController.py'
  4. cp -r app dist/app
  5. cp PduConfig.json dist/PduConfig.json
  4. RaritanPduOutletController.exe will be in dist directory