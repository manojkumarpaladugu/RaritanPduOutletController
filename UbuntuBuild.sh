#!/bin/bash
HOME_DIR=$PWD
SRC_DIR=$HOME_DIR/src
ASSETS_DIR=$HOME_DIR/assets
OUT_DIR=$HOME_DIR/_out
BIN_DIR=$OUT_DIR/RaritanPduOutletController_Ubuntu
OUT_ASSETS_DIR=$BIN_DIR/assets
CLI_APP_NAME='RaritanPduOutletController_Cli'
GUI_APP_NAME='RaritanPduOutletController_Gui'
CYCLE_IMG=$ASSETS_DIR/Cycle.png

# Clean the output directory
if [ $1 = "clean" ]; then
    rm -rf _out
fi

echo "------------------------------------------"
echo "-> Building $CLI_APP_NAME"
echo "------------------------------------------"
pyinstaller                           \
    --workpath $OUT_DIR               \
    --specpath $OUT_DIR/$CLI_APP_NAME \
    --distpath $BIN_DIR               \
    --name $CLI_APP_NAME              \
    --noconfirm                       \
    --onefile                         \
    --console                         \
    $SRC_DIR/CommandLineInterface.py

echo "------------------------------------------"
echo "-> Building $GUI_APP_NAME"
echo "------------------------------------------"
pyinstaller                            \
    --workpath $OUT_DIR                \
    --specpath $OUT_DIR/$GUI_APP_NAME  \
    --distpath $BIN_DIR                \
    --name $GUI_APP_NAME               \
    --add-data $CYCLE_IMG:assets       \
    --collect-all customtkinter        \
    --noconfirm                        \
    --onefile                          \
    --windowed                         \
    $SRC_DIR/GraphicalUserInterface.py

# Copying dependencies
mkdir $OUT_ASSETS_DIR
cp $ASSETS_DIR/AppConfig.json        $OUT_ASSETS_DIR/AppConfig.json
cp $ASSETS_DIR/PduOutletConfig.json  $OUT_ASSETS_DIR/PduOutletConfig.json

# Cleaning up intermediate files
rm -rf $OUT_DIR/$CLI_APP_NAME
rm -rf $OUT_DIR/$GUI_APP_NAME