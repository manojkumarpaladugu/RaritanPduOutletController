# Raritan PDU Outlet Controller
## Introduction:
* An application that helps you control Raritan Power Distribution Unit (PDU) remotely
* With this, you will be able to remotely ON|OFF|CYCLE power outlets remotely over internet
* GUI and CLI support

## Graphical User Interface (GUI)
**How to use?**  
1. Add PDU outlet configuration in assets\PduOutletConfig.Json
2. [Optional] Adjust application settings in assets\AppConfig.json
3. Open RaritanPduOutletController_Gui.exe
<img src="https://github.com/manojkumarpaladugu/RaritanPduOutletController/blob/main/assets/RaritanPduOutletController_Gui.jpg" width="600"/>

## Command Line Interface (CLI)
<img src="https://github.com/manojkumarpaladugu/RaritanPduOutletController/blob/main/assets/RaritanPduOutletController_Cli.jpg" width="600"/>

## Install Below Dependencies
**On Windows and Ubuntu:**
~~~
pip3 install raritan
pip3 install customtkinter
pip3 install pyinstaller
~~~
**On Windows:**
~~~
pip3 install tk
~~~

**On Ubuntu:**
~~~
sudo apt-get install python3-tk
~~~

## Generate Executable
**On Windows:**
~~~
.\BuildWindows.ps1
~~~
**Output**
~~~
_out\RaritanPduOutletController_Win\RaritanPduOutletController_Gui.exe
_out\RaritanPduOutletController_Win\RaritanPduOutletController_Cli.exe
~~~
**On Ubuntu:**
~~~
./UbuntuBuild.sh
~~~
**Output**
~~~
_out\RaritanPduOutletController_Ubuntu\RaritanPduOutletController_Gui
_out\RaritanPduOutletController_Ubuntu\RaritanPduOutletController_Cli
~~~
