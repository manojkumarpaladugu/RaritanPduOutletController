from raritan     import rpc
from raritan.rpc import pdumodel

class RaritanPduException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class RaritanPduOutletController:
    def __init__(self, pduModel, pduIpAddress, pduUsername, pduPassword):
        self.pduModel     = pduModel
        self.pduIpAddress = pduIpAddress
        self.pduUsername  = pduUsername
        self.pduPassword  = pduPassword

    def GetConnectionInfo(self):
        return self.pduIpAddress, self.pduUsername, self.pduPassword

    def ConnectToPdu(self):
        try:
            agent    = rpc.Agent('https', self.pduIpAddress, self.pduUsername, self.pduPassword)
            pduModel = pdumodel.Pdu(self.pduModel, agent)
            outlets  = pduModel.getOutlets()
            return outlets
        except rpc.HttpException as httpExec:
            if 'Authentication failed' in httpExec.args[0]:
                raise RaritanPduException('Authentication error')
            else:
                raise RaritanPduException('Unable to establish connection')

    def IsOutletPowerOn(self, outlet):
        return outlet.getState().powerState == pdumodel.Outlet.PowerState.PS_ON

    def IsOutletPowerOff(self, outlet):
        return outlet.getState().powerState == pdumodel.Outlet.PowerState.PS_OFF

    def IsSwitchOnInProgress(self, outlet):
        return outlet.getState().switchOnInProgress

    def IsCycleInProgress(self, outlet):
        return outlet.getState().cycleInProgress

    def PowerOnOutlet(self, outlet):
        if (self.IsSwitchOnInProgress(outlet) or self.IsOutletPowerOn(outlet)):
            return
        outlet.setPowerState(pdumodel.Outlet.PowerState.PS_ON)
        while(self.IsSwitchOnInProgress(outlet)):
            pass

    def PowerOffOutlet(self, outlet):
        if (self.IsOutletPowerOff(outlet)):
            return
        outlet.setPowerState(pdumodel.Outlet.PowerState.PS_OFF)
        while(self.IsOutletPowerOn(outlet)):
            pass

    def PowerCycleOutlet(self, outlet):
        if(self.IsCycleInProgress(outlet)):
            return
        outlet.cyclePowerState()
        while(self.IsCycleInProgress(outlet)):
            pass
