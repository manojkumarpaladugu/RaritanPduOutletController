Set-ExecutionPolicy RemoteSigned
New-Variable outputDirectory 'RaritanPduOutletController_Win' -Option ReadOnly
New-Variable cliAppName      'RaritanPduOutletController_Cli' -Option ReadOnly
New-Variable guiAppName      'RaritanPduOutletController_Gui' -Option ReadOnly
New-Variable customTkinterPath "c:\users\manoj\appdata\local\programs\python\python39\lib\site-packages\customtkinter;customtkinter\" -Option ReadOnly

"----------------------------------------------"
"-> Building $cliAppName.exe"
"----------------------------------------------"
pyinstaller  --distpath $outputDirectory --name $cliAppName --icon=assets\PlugSocket.ico --clean --noconfirm --onefile --console 'CommandLineInterface.py'

"----------------------------------------------"
"-> Building $guiAppName.exe"
"----------------------------------------------"
pyinstaller  --distpath $outputDirectory --name $guiAppName --icon=assets\PlugSocket.ico --add-data $customTkinterPath --clean --noconfirm --onefile --windowed 'GraphicalUserInterface.py'

"-----------------------"
"-> Copying dependencies"
"-----------------------"
New-Item  -Path ".\$outputDirectory\assets" -ItemType Directory

Copy-Item -Path '.\assets\AppConfig.Json' -Destination ".\$outputDirectory\assets\" -PassThru
Copy-Item -Path '.\assets\PlugSocket.ico' -Destination ".\$outputDirectory\assets\" -PassThru
Copy-Item -Path '.\PduOutletConfig.json'  -Destination ".\$outputDirectory\"        -PassThru

"--------------"
"-> Cleaning up"
"--------------"
Remove-Item '.\build'          -Recurse
Remove-Item "$cliAppName.spec"
Remove-Item "$guiAppName.spec"