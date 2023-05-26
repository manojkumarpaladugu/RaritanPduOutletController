New-Variable HOME_DIR       $PWD                                      -Option ReadOnly
New-Variable SRC_DIR        "$HOME_DIR\src"                           -Option ReadOnly
New-Variable ASSETS_DIR     "$HOME_DIR\assets"                        -Option ReadOnly
New-Variable OUT_DIR        "$HOME_DIR\_out"                          -Option ReadOnly
New-Variable BIN_DIR        "$OUT_DIR\RaritanPduOutletController_Win" -Option ReadOnly
New-Variable OUT_ASSETS_DIR "$BIN_DIR\assets"                         -Option ReadOnly
New-Variable CLI_APP_NAME   'RaritanPduOutletController_Cli'          -Option ReadOnly
New-Variable GUI_APP_NAME   'RaritanPduOutletController_Gui'          -Option ReadOnly
New-Variable ICON_FILE      "$ASSETS_DIR\PlugSocket.ico"              -Option ReadOnly

"----------------------------------------------"
"-> Building $CLI_APP_NAME.exe"
"----------------------------------------------"
pyinstaller                           `
    --workpath $OUT_DIR               `
    --specpath $OUT_DIR/$CLI_APP_NAME `
    --distpath $BIN_DIR               `
    --name $CLI_APP_NAME              `
    --icon=$ICON_FILE                 `
    --noconfirm                       `
    --onefile                         `
    --console                         `
    "$SRC_DIR\CommandLineInterface.py"

"----------------------------------------------"
"-> Building $GUI_APP_NAME.exe"
"----------------------------------------------"
pyinstaller                              `
    --workpath $OUT_DIR                  `
    --specpath $OUT_DIR/$CLI_APP_NAME    `
    --distpath $BIN_DIR                  `
    --name $GUI_APP_NAME                 `
    --icon=$ICON_FILE                    `
    --collect-all customtkinter          `
    --noconfirm                          `
    --onefile                            `
    --windowed                           `
    "$SRC_DIR\GraphicalUserInterface.py"

"-----------------------"
"-> Copying dependencies"
"-----------------------"
New-Item  -Path $OUT_ASSETS_DIR                    -ItemType    Directory
Copy-Item -Path "$ASSETS_DIR\AppConfig.json"       -Destination $OUT_ASSETS_DIR -PassThru
Copy-Item -Path "$ASSETS_DIR\PlugSocket.ico"       -Destination $OUT_ASSETS_DIR -PassThru
Copy-Item -Path "$ASSETS_DIR\PduOutletConfig.json" -Destination $BIN_DIR        -PassThru

# cleaning up
Remove-Item $OUT_DIR/$CLI_APP_NAME -Recurse
Remove-Item $OUT_DIR/$GUI_APP_NAME -Recurse