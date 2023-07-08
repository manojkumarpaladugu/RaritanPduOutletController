# Raritan PDU Outlet Controller
## Introduction:
* An application that helps you control Raritan Power Distribution Unit (PDU) remotely
* With this, you will be able to remotely ON|OFF|CYCLE power outlets remotely over internet
* GUI and CLI support

## Downloads
Released binaries and source code available in [Releases](https://github.com/manojkumarpaladugu/RaritanPduOutletController/releases) page

## Install Below Dependencies
**On Windows:**
~~~
pip3 install raritan
pip3 install customtkinter
pip3 install pyinstaller
pip3 install Pillow
pip3 install tk
~~~

**On Ubuntu:**
~~~
sudo pip3 install raritan
sudo pip3 install customtkinter
sudo pip3 install pyinstaller
sudo apt-get install python3-tk
sudo apt-get install python3-pil python3-pil.imagetk
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

## Graphical User Interface (GUI)
**How to use?**  
1. Add PDU outlet configuration in assets\PduOutletConfig.Json
2. [Optional] Adjust application settings in assets\AppConfig.json
3. Open RaritanPduOutletController_Gui.exe
<img src="https://github.com/manojkumarpaladugu/RaritanPduOutletController/blob/main/assets/RaritanPduOutletController_Gui.jpg" width="600"/>

## Command Line Interface (CLI)
<img src="https://github.com/manojkumarpaladugu/RaritanPduOutletController/blob/main/assets/RaritanPduOutletController_Cli.jpg" width="600"/>

## Release Notes
> ## v1.0.4 (July/08/2023)
> 
> - Replaced seperate On/Off buttons with a single slider switch
> - Replaced cycle button with an image
> - Added clean build option

> ## v1.0.3 (June/04/2023)
> 
> - Added error handling in CLI and GUI
> - Environment variable support in CLI
> - Enhancements and bug fixes

> ## v1.0.2 (June/03/2023)
> 
> - Added CLI support
> - Enhancements and bug fixes

> ## v1.0.1 (April/29/2023)
> 
> - Enhancements and bug fixes

> ## v1.0.0 (April/29/2023)
> - Added Raritan PDU device
> - Added GUI tool
