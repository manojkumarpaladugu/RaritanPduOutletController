import sys
import argparse
from   version                    import __version__
from   RaritanPduOutletController import RaritanPduOutletController

if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    argParser.add_argument('-v' , action='version', version="%(prog)s ("+__version__+")")
    argParser.add_argument('-i' , help='PDU IP address'                           , required=True)
    argParser.add_argument('-u' , help='PDU username'                             , required=True)
    argParser.add_argument('-p' , help='PDU password'                             , required=True)
    argParser.add_argument('-o' , help='PDU outlet number'                        , required=True)
    argParser.add_argument('-s' , help='Set PDU outlet power state (on|off|cycle)', required=True)
    args = argParser.parse_args()

    pduIpAddress     = args.i
    pduUsername      = args.u
    pduPassword      = args.p
    pduOutletNumber  = int(args.o)
    pduState         = args.s
    outletController = RaritanPduOutletController('/model/pdu/0', pduIpAddress, pduUsername, pduPassword)

    try:
        outlets = outletController.ConnectToPdu()
        if pduOutletNumber > len(outlets):
            raise ValueError('ERROR: Outlet number {0} is exceeding the maximum limit {1}'.format(pduOutletNumber, len(outlets)))

        outlet = outlets[pduOutletNumber- 1]
        if pduState == 'on':
            outletController.PowerOnOutlet(outlet)
            print('Outlet {} is ON now'.format(pduOutletNumber))
        elif pduState == 'off':
            outletController.PowerOffOutlet(outlet)
            print('Outlet {} is OFF now'.format(pduOutletNumber))
        elif pduState == 'cycle':
            outletController.PowerCycleOutlet(outlet)
            print('Outlet {} is CYCLED now'.format(pduOutletNumber))
        else:
            raise ValueError('ERROR: Unrecognised option \'-s {}\''.format(pduState))
    except ValueError as message:
        print(message)
    except:
        print('ERROR: Unable to establish connection at https://{}'.format(pduIpAddress))

    sys.exit()
