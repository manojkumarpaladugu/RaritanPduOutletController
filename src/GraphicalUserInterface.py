import os
import sys
import json
import MiscLib
import threading
import functools
import webbrowser
import customtkinter
from   version                    import __version__
from   dataclasses                import dataclass
from   RaritanPduOutletController import *

BUTTON_ACTIVE_COLOR    = '#3a7ebf'
APP_CONFIGURATION_FILE = os.path.join('assets', 'AppConfig.json')
TIMEOUT_SECONDS        = 5

@dataclass
class Theme:
    staticFrame       : str
    scrollableFrame   : str
    pduFrame          : str
    pduFrameText      : str
    groupFrame        : str
    groupFrameText    : str
    buttonActiveColor : str

@dataclass
class Outlet:
    name             : str
    number           : int
    powerStatusLabel : customtkinter.CTkLabel
    powerOnButton    : customtkinter.CTkButton
    powerOffButton   : customtkinter.CTkButton
    powerCycleButton : customtkinter.CTkButton

@dataclass
class PowerDistributionUnit:
    name             : str
    outletController : RaritanPduOutletController
    outletGroups     : dict

class PduOutletController:
    def __init__(self):
        appConfig              = self.LoadConfiguration(APP_CONFIGURATION_FILE)
        self.applicationName   = 'Raritan PDU Outlet Controller'
        self.applicationWidth  = appConfig['Application']['Width']
        self.applicationHeight = appConfig['Application']['Height']
        if os.name == 'nt': # Windows OS
            relativePath         = appConfig['Application']['Icon'].split(';')[-1]
            fileName             = appConfig['Application']['Icon'].split(';')[-2]
            self.applicationIcon = self.GetResourcePath(os.path.join(relativePath, fileName))
        self.applicationTheme  = Theme(appConfig['Application']['Theme']['Static Frame'],
                                       appConfig['Application']['Theme']['Scrollable Frame'],
                                       appConfig['Application']['Theme']['PDU Frame'],
                                       appConfig['Application']['Theme']['PDU Frame Text'],
                                       appConfig['Application']['Theme']['Group Frame'],
                                       appConfig['Application']['Theme']['Group Frame Text'],
                                       BUTTON_ACTIVE_COLOR)
        relativePath           = appConfig['Application']['PDU Configuration'].split(';')[-1]
        fileName               = appConfig['Application']['PDU Configuration'].split(';')[-2]
        self.pduConfigFile     = os.path.join(relativePath, fileName)
        self.gui               = customtkinter.CTk()

    def LoadConfiguration(self, fileName):
        with open(fileName, "r") as jsonFile:
            configuration = json.load(jsonFile)
            jsonFile.close()
        return configuration

    def GetResourcePath(self, relativePath):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        basePath = getattr(sys, '_MEIPASS', '')
        return os.path.join(basePath, relativePath)

    def PopulatePduOutlets(self):
        pduConfig = self.LoadConfiguration(self.pduConfigFile)
        self.pduMap = dict()
        for pduName, pduMap in pduConfig['Power Distribution Units'].items():
            groupMap = dict()
            for outletGroupName, outletGroupMap in pduMap['Outlet-Groups'].items():
                outletMap = dict()
                for outletName, outletNumber in outletGroupMap.items():
                    outletMap[str(outletNumber)] = Outlet(outletName,
                                                          int(outletNumber),
                                                          None,
                                                          None,
                                                          None,
                                                          None)
                groupMap[outletGroupName] = outletMap
            outletController     = RaritanPduOutletController(pduMap['Model'],
                                                              pduMap['IP Address'],
                                                              pduMap['Username'],
                                                              pduMap['Password'])
            self.pduMap[pduName] = PowerDistributionUnit(pduName,
                                                         outletController,
                                                         groupMap)

    def RunMainLoop(self):
        self.PopulatePduOutlets()
        self.gui.bind('<Visibility>', self.GenerateWindow())
        self.gui.mainloop()

    def GenerateWindow(self):
        self.gui.unbind('<Visibility>')
        customtkinter.set_appearance_mode('light')     # system (default), dark, light
        customtkinter.set_default_color_theme('dark-blue')  # Themes: "blue" (standard), "green", "dark-blue"
        self.gui.title(self.applicationName)
        self.gui.resizable(False, False)
        if os.name == 'nt': # Windows OS
            self.gui.wm_iconbitmap(self.applicationIcon)

        staticFrame = customtkinter.CTkFrame(self.gui,
                                             width=self.applicationWidth,
                                             corner_radius=0,
                                             bg_color=self.applicationTheme.staticFrame,
                                             fg_color=self.applicationTheme.staticFrame)
        staticFrame.grid(row=0, column=0, sticky=customtkinter.W+customtkinter.E)

        self.refreshButton = customtkinter.CTkButton(staticFrame,
                                                     text='Refresh',
                                                     width=self.applicationWidth / 2,
                                                     height=20,
                                                     command=self.RefreshButtonCallback)
        self.refreshButton.grid(row=0, column=0, padx=5, sticky=customtkinter.W+customtkinter.E)

        self.aboutButton = customtkinter.CTkButton(staticFrame,
                                                   text='About',
                                                   width=self.applicationWidth / 2,
                                                   height=20,
                                                   command=self.AboutButtonCallback)
        self.aboutButton.grid(row=0, column=1, padx=5, sticky=customtkinter.W+customtkinter.E)

        verticalScrollableFrame = customtkinter.CTkScrollableFrame(self.gui,
                                                                   width=self.applicationWidth,
                                                                   height=self.applicationHeight,
                                                                   corner_radius=0,
                                                                   bg_color=self.applicationTheme.scrollableFrame,
                                                                   fg_color=self.applicationTheme.scrollableFrame,
                                                                   scrollbar_button_color='#b5bbbd',
                                                                   scrollbar_button_hover_color='#7d888c',
                                                                   orientation='vertical')
        verticalScrollableFrame.grid(row=1, column=0, sticky=customtkinter.W+customtkinter.E)

        scrollbarRow = 0
        for pduName, pduMap in self.pduMap.items():
            # Create PDU frame
            pduFrame = customtkinter.CTkFrame(verticalScrollableFrame,
                                              corner_radius=5,
                                              fg_color=self.applicationTheme.pduFrame)
            pduFrame.grid(row=scrollbarRow, column=0, padx=5, pady=5, sticky=customtkinter.W+customtkinter.E)
            scrollbarRow += 1

            pduRow = 0
            ipAddress, username, password = pduMap.outletController.GetConnectionInfo()
            pduLabel = customtkinter.CTkLabel(pduFrame,
                                              text=pduName + ' - ' + ipAddress,
                                              text_color=self.applicationTheme.pduFrameText,
                                              font=customtkinter.CTkFont(weight='bold'))
            pduLabel.grid(row=pduRow, column=0, padx=5, pady=5, sticky=customtkinter.W)
            pduRow += 1

            for outletGroupName, outletGroupMap in pduMap.outletGroups.items():
                # Create group frame
                groupFrame = customtkinter.CTkFrame(pduFrame,
                                                    corner_radius=5,
                                                    fg_color=self.applicationTheme.groupFrame)
                groupFrame.grid(row=pduRow, column=0, padx=5, pady=5, sticky=customtkinter.N+customtkinter.S)
                pduRow += 1

                groupRow = 0
                outletGrouplabel = customtkinter.CTkLabel(groupFrame,
                                                          text=outletGroupName,
                                                          width=150,
                                                          text_color=self.applicationTheme.groupFrameText,
                                                          font=customtkinter.CTkFont(weight='bold'))
                outletGrouplabel.grid(row=groupRow, column=0, padx=5, pady=5, sticky=customtkinter.W+customtkinter.E)
                for outlet in outletGroupMap.values():
                    outletColumn = 1
                    # Outlet number
                    outletNumberLabel = customtkinter.CTkLabel(groupFrame,
                                                               text=str(outlet.number),
                                                               text_color=self.applicationTheme.groupFrameText)
                    outletNumberLabel.grid(row=groupRow, column=outletColumn, padx=5, pady=5, sticky=customtkinter.W+customtkinter.E)
                    outletColumn += 1
                    # Outlet name
                    outletNameLabel = customtkinter.CTkLabel(groupFrame,
                                                             text=outlet.name,
                                                             text_color=self.applicationTheme.groupFrameText)
                    outletNameLabel.grid(row=groupRow, column=outletColumn, padx=20, pady=5, sticky=customtkinter.W)
                    outletColumn += 1
                    # Outlet status
                    outlet.powerStatusLabel = customtkinter.CTkLabel(groupFrame,
                                                                     text='?',
                                                                     text_color=self.applicationTheme.groupFrameText,
                                                                     width=25)
                    outlet.powerStatusLabel.grid(row=groupRow, column=outletColumn, padx=20, pady=5, sticky=customtkinter.W+customtkinter.E)
                    outletColumn += 1
                    # Power on button
                    callbackWithArgs = functools.partial(self.PowerOnButtonCallback, pduMap, outlet)
                    outlet.powerOnButton = customtkinter.CTkButton(groupFrame,
                                                                  text="On",
                                                                  width=50,
                                                                  command=callbackWithArgs)
                    outlet.powerOnButton.grid(row=groupRow, column=outletColumn, padx=5, pady=5, sticky=customtkinter.W+customtkinter.E)
                    outletColumn += 1
                    # Power off button
                    callbackWithArgs = functools.partial(self.PowerOffButtonCallback, pduMap, outlet)
                    outlet.powerOffButton = customtkinter.CTkButton(groupFrame,
                                                                   text="Off",
                                                                   width=50,
                                                                   command=callbackWithArgs)
                    outlet.powerOffButton.grid(row=groupRow, column=outletColumn, padx=5, pady=5, sticky=customtkinter.W+customtkinter.E)
                    outletColumn += 1
                    # Power cycle button
                    callbackWithArgs = functools.partial(self.PowerCycleButtonCallback, pduMap, outlet)
                    outlet.powerCycleButton = customtkinter.CTkButton(groupFrame,
                                                                     text="Cycle",
                                                                     width=50,
                                                                     command=callbackWithArgs)
                    outlet.powerCycleButton.grid(row=groupRow, column=outletColumn, padx=5, pady=5, sticky=customtkinter.W+customtkinter.E)
                    groupRow += 1

        thread = threading.Thread(target=self.RefreshButtonCallback)
        thread.start()

    def OpenPopUpWindow(self, title, windowWidthHeight, message):
        popUpWindow = customtkinter.CTkToplevel(self.gui)
        popUpWindow.geometry(windowWidthHeight)
        popUpWindow.title(title)
        # CtkTopLevel class set window icon after 200 ms. To overcome it, we should delay call to wm_iconbitmap(...).
        if os.name == 'nt': # Windows OS
            popUpWindow.after(205, lambda: popUpWindow.wm_iconbitmap(self.applicationIcon))
        popUpWindow.resizable(False, False)
        label = customtkinter.CTkLabel(popUpWindow,
                                       text=message)
        label.pack(padx=20, pady=20)
        x = self.gui.winfo_x() + self.gui.winfo_width() // 2 - popUpWindow.winfo_width() // 2
        y = self.gui.winfo_y() + self.gui.winfo_height() // 2 - popUpWindow.winfo_height() // 2
        popUpWindow.geometry("+%d+%d" %(x,y))
        popUpWindow.wm_transient(self.gui)   # Keep the toplevel window in front of the root window
        popUpWindow.grab_set()

    def RefreshButtonCallback(self):
        # Update outlet power status
        for pdu in self.pduMap.values():
            try:
                outlets = MiscLib.RunThreadWithReturnValueBlocking(function=pdu.outletController.ConnectToPdu, timeout=TIMEOUT_SECONDS)
                for outletGroup in pdu.outletGroups.values():
                    for outlet in outletGroup.values():
                        outletNumber = outlet.number - 1
                        if (pdu.outletController.IsOutletPowerOn(outlets[outletNumber])):
                            outlet.powerStatusLabel.configure(text='ON', text_color='green')
                        elif (pdu.outletController.IsOutletPowerOff(outlets[outletNumber])):
                            outlet.powerStatusLabel.configure(text='OFF', text_color='red')
                        else:
                            outlet.powerStatusLabel.configure(text='?', text_color='black')
            except (MiscLib.TimeoutException, RaritanPduException) as message:
                ipAddress, username, password = pdu.outletController.GetConnectionInfo()
                self.OpenPopUpWindow(title='Error',
                                    windowWidthHeight='{}x75'.format(self.applicationWidth),
                                    message='{0}\nIP={1}, Username={2}, Password={3}'.format(message, ipAddress, username, password))
            except:
                self.OpenPopUpWindow(title='Error',
                                    windowWidthHeight='{}x75'.format(self.applicationWidth),
                                    message='Unknown exception occurred')
                continue

    def OpenUrl(self, url):
        webbrowser.open_new_tab(url)

    def AboutButtonCallback(self):
        windowWidth  = 459
        windowHeight = 131
        aboutWindow = customtkinter.CTkToplevel(self.gui)
        aboutWindow.geometry('{0}x{1}'.format(windowWidth, windowHeight))
        aboutWindow.title('About')
        # CtkTopLevel class set window icon after 200 ms. To overcome it, we should delay call to wm_iconbitmap(...)
        if os.name == 'nt': # Windows OS
            aboutWindow.after(205, lambda: aboutWindow.wm_iconbitmap(self.applicationIcon))
        aboutWindow.resizable(False, False)

        frame = customtkinter.CTkFrame(aboutWindow,
                                       corner_radius=0)
        frame.grid(row=0, column=0, sticky=customtkinter.W+customtkinter.E)

        message = 'Version'
        label = customtkinter.CTkLabel(frame,
                                       text=message)
        label.grid(row=0, column=0, padx=10, pady=2, sticky=customtkinter.W)
        message = ': ' + __version__
        label = customtkinter.CTkLabel(frame,
                                       text=message)
        label.grid(row=0, column=1, padx=10, pady=2, sticky=customtkinter.W)

        message = 'Developer'
        label = customtkinter.CTkLabel(frame,
                                       text=message)
        label.grid(row=1, column=0, padx=10, pady=2, sticky=customtkinter.W)
        message = ': Manoj Kumar Paladugu'
        label = customtkinter.CTkLabel(frame,
                                       text=message)
        label.grid(row=1, column=1, padx=10, pady=2, sticky=customtkinter.W)

        message = 'E-Mail'
        label = customtkinter.CTkLabel(frame,
                                       text=message)
        label.grid(row=2, column=0, padx=10, pady=2, sticky=customtkinter.W)
        message = ': paladugumanojkumar@gmail.com'
        label = customtkinter.CTkLabel(frame,
                                       text=message)
        label.grid(row=2, column=1, padx=10, pady=2, sticky=customtkinter.W)

        message = 'Repository'
        label = customtkinter.CTkLabel(frame,
                                       text=message)
        label.grid(row=3, column=0, padx=10, pady=2, sticky=customtkinter.W)
        url     = 'github.com/manojkumarpaladugu/RaritanPduOutletController'
        message = ': ' + url
        label = customtkinter.CTkLabel(frame,
                                       text=message,
                                       text_color='#285885',
                                       cursor='hand2')
        label.grid(row=3, column=1, padx=10, pady=2, sticky=customtkinter.W)
        label.bind('<Button-1>', lambda e: self.OpenUrl(url))

        x = self.gui.winfo_x() + self.gui.winfo_width() // 2 - aboutWindow.winfo_width() // 2
        y = self.gui.winfo_y() + self.gui.winfo_height() // 2 - aboutWindow.winfo_height() // 2
        aboutWindow.geometry("+%d+%d" %(x,y))
        aboutWindow.wm_transient(self.gui)   # Keep the toplevel window in front of the root window
        aboutWindow.wait_visibility()
        aboutWindow.grab_set()

    def PowerOnOutlet(self, pdu, outlet):
        outlet.powerOnButton.configure(state=customtkinter.DISABLED, fg_color='gray')
        try:
            outlets = MiscLib.RunThreadWithReturnValueBlocking(function=pdu.outletController.ConnectToPdu, timeout=TIMEOUT_SECONDS)
            if outlet.number > len(outlets):
                self.OpenPopUpWindow(title='Error',
                                     windowWidthHeight='400x75',
                                     message='Outlet number {0} is exceeding the maximum limit {1}'.format(outlet.number, len(outlets)))
                return
            pdu.outletController.PowerOnOutlet(outlets[outlet.number - 1])
            outlet.powerStatusLabel.configure(text='ON', text_color='green')
        except (MiscLib.TimeoutException, RaritanPduException) as message:
            outlet.powerStatusLabel.configure(text='?', text_color='black')
            ipAddress, username, password = pdu.outletController.GetConnectionInfo()
            self.OpenPopUpWindow(title='Error',
                                 windowWidthHeight='{}x75'.format(self.applicationWidth),
                                 message='{0}\nIP={1}, Username={2}, Password={3}'.format(message, ipAddress, username, password))
        except:
            outlet.powerStatusLabel.configure(text='?', text_color='black')
            self.OpenPopUpWindow(title='Error',
                                 windowWidthHeight='{}x75'.format(self.applicationWidth),
                                 message='Unknown exception occurred')
        outlet.powerOnButton.configure(state=customtkinter.NORMAL, fg_color=self.applicationTheme.buttonActiveColor)

    def PowerOnButtonCallback(self, pdu, outlet):
        thread = threading.Thread(target=self.PowerOnOutlet, args=[pdu, outlet])
        thread.start()

    def PowerOffOutlet(self, pdu, outlet):
        outlet.powerOffButton.configure(state=customtkinter.DISABLED, fg_color='gray')
        try:
            outlets = MiscLib.RunThreadWithReturnValueBlocking(function=pdu.outletController.ConnectToPdu, timeout=TIMEOUT_SECONDS)
            if outlet.number > len(outlets):
                self.OpenPopUpWindow(title='Error',
                                     windowWidthHeight='350x75',
                                     message='Outlet number {0} is exceeding the maximum limit {1}'.format(outlet.number, len(outlets)))
                return
            pdu.outletController.PowerOffOutlet(outlets[outlet.number - 1])
            outlet.powerStatusLabel.configure(text='OFF', text_color='red')
        except (MiscLib.TimeoutException, RaritanPduException) as message:
            outlet.powerStatusLabel.configure(text='?', text_color='black')
            ipAddress, username, password = pdu.outletController.GetConnectionInfo()
            self.OpenPopUpWindow(title='Error',
                                 windowWidthHeight='{}x75'.format(self.applicationWidth),
                                 message='{0}\nIP={1}, Username={2}, Password={3}'.format(message, ipAddress, username, password))
        except:
            outlet.powerStatusLabel.configure(text='?', text_color='black')
            self.OpenPopUpWindow(title='Error',
                                 windowWidthHeight='{}x75'.format(self.applicationWidth),
                                 message='Unknown exception occurred')
        outlet.powerOffButton.configure(state=customtkinter.NORMAL, fg_color=self.applicationTheme.buttonActiveColor)

    def PowerOffButtonCallback(self, pdu, outlet):
        thread = threading.Thread(target=self.PowerOffOutlet, args=[pdu, outlet])
        thread.start()

    def PowerCycleOutlet(self, pdu, outlet):
        outlet.powerCycleButton.configure(state=customtkinter.DISABLED, fg_color='gray')
        try:
            outlets = MiscLib.RunThreadWithReturnValueBlocking(function=pdu.outletController.ConnectToPdu, timeout=TIMEOUT_SECONDS)
            if outlet.number > len(outlets):
                self.OpenPopUpWindow(title='Error',
                                     windowWidthHeight='350x75',
                                     message='Outlet number {0} is exceeding the maximum limit {1}'.format(outlet.number, len(outlets)))
                return
            outlet.powerStatusLabel.configure(text='OFF', text_color='red')
            pdu.outletController.PowerCycleOutlet(outlets[outlet.number - 1])
            outlet.powerStatusLabel.configure(text='ON', text_color='green')
        except (MiscLib.TimeoutException, RaritanPduException) as message:
            outlet.powerStatusLabel.configure(text='?', text_color='black')
            ipAddress, username, password = pdu.outletController.GetConnectionInfo()
            self.OpenPopUpWindow(title='Error',
                                 windowWidthHeight='{}x75'.format(self.applicationWidth),
                                 message='{0}\nIP={1}, Username={2}, Password={3}'.format(message, ipAddress, username, password))
        except:
            outlet.powerStatusLabel.configure(text='?', text_color='black')
            self.OpenPopUpWindow(title='Error',
                                 windowWidthHeight='{}x75'.format(self.applicationWidth),
                                 message='Unknown exception occurred')
        outlet.powerCycleButton.configure(state=customtkinter.NORMAL, fg_color=self.applicationTheme.buttonActiveColor)

    def PowerCycleButtonCallback(self, pdu, outlet):
        thread = threading.Thread(target=self.PowerCycleOutlet, args=[pdu, outlet])
        thread.start()

if __name__ == '__main__':
    pduOutletController = PduOutletController()
    pduOutletController.RunMainLoop()
