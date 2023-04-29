# Raritan PDU Outlet Controller

### How to use?
    1. Add PDU - Outlet configuration in PduConfig.Json
    2. [Optional] Adjust application settings in assets/AppConfig.json
    3. Open RaritanPduOutletController.exe

### Screenshot
<img src="https://github.com/manojkumarpaladugu/RaritanPduOutletController/blob/main/assets/RaritanPduOutletController.jpg" width="600"/>

### Install Below PIP Packages:
    pip3 install raritan
    pip3 install customtkinter
    pip3 install pyinstaller

### Generate Windows Executable:
    1. Open PowerShell
    2. Copy customtkinter path from the output of "pip3 show customtkinter"
    3. pyinstaller --noconfirm --onefile --windowed --icon=assets\PlugSocket.ico --add-data "c:\users\<username>\appdata\local\programs\python\python39\lib\site-packages\customtkinter;customtkinter\" 'RaritanPduOutletController.py'
    4. cp -r assets dist/assets
    5. cp PduConfig.json dist/PduConfig.json
    6. RaritanPduOutletController.exe will be in 'dist' directory
