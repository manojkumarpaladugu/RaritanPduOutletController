from raritan     import rpc
from raritan.rpc import pdumodel

class RaritanPduOutletController:
    def __init__(self, pduModel, pduIpAddress, pduUsername, pduPassword):
        self.pduModel     = pduModel
        self.pduIpAddress = pduIpAddress
        self.pduUsername  = pduUsername
        self.pduPassword  = pduPassword

    def ConnectToPdu(self):
        agent    = rpc.Agent('https', self.pduIpAddress, self.pduUsername, self.pduPassword)
        pduModel = pdumodel.Pdu(self.pduModel, agent)
        outlets  = pduModel.getOutlets()
        return outlets

    def IsOutletPowerOn(self, outlet):
        return outlet.getState().powerState == pdumodel.Outlet.PowerState.PS_ON

    def IsOutletPowerOff(self, outlet):
        return outlet.getState().powerState == pdumodel.Outlet.PowerState.PS_OFF

    def PowerOnOutlet(self, outlet):
        if (outlet.getState().switchOnInProgress) or \
           (outlet.getState().powerState == pdumodel.Outlet.PowerState.PS_ON):
            return
        outlet.setPowerState(pdumodel.Outlet.PowerState.PS_ON)
        while(outlet.getState().switchOnInProgress):
            pass

    def PowerOffOutlet(self, outlet):
        if (outlet.getState().powerState == pdumodel.Outlet.PowerState.PS_OFF):
            return
        outlet.setPowerState(pdumodel.Outlet.PowerState.PS_OFF)
        while(outlet.getState().powerState == pdumodel.Outlet.PowerState.PS_ON):
            pass

    def PowerCycleOutlet(self, outlet):
        if(outlet.getState().cycleInProgress):
            return
        outlet.cyclePowerState()
        while(outlet.getState().powerState == pdumodel.Outlet.PowerState.PS_OFF):
            pass
