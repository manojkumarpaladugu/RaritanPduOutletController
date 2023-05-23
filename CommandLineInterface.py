import sys
import argparse
from   version                    import __version__
from   RaritanPduOutletController import RaritanPduOutletController

if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    argParser.add_argument('-v' , '--version'  , action='version', version="%(prog)s ("+__version__+")")
    argParser.add_argument('-i' , '--ipaddress', help='PDU IP Address'                           , required=True)
    argParser.add_argument('-u' , '--username' , help='PDU Username'                             , required=True)
    argParser.add_argument('-p' , '--password' , help='PDU Password'                             , required=True)
    argParser.add_argument('-o' , '--outlet'   , help='PDU Outlet number'                        , required=True)
    argParser.add_argument('-s' , '--state'    , help='Set PDU outlet power state (on|off|cycle)', required=True)
    args = argParser.parse_args()

    outletController = RaritanPduOutletController('/model/pdu/0', args.ipaddress, args.username, args.password)

    try:
        outlets = outletController.ConnectToPdu()
        outlet = outlets[args.outlet - 1]
        if args.state == 'on':
            outletController.PowerOnOutlet(outlet)
            print('Outlet {} ON now'.format(args.outlet))
        elif args.state == 'off':
            outletController.PowerOffOutlet(outlet)
            print('Outlet {} OFF now'.format(args.outlet))
        elif args.state == 'cycle':
            outletController.PowerCycleOutlet(outlet)
            print('Outlet {} CYCLED now'.format(args.outlet))
        else:
            print('ERROR: Unrecognised option \'-s {}\''.format(args.state))
    except:
        print('ERROR: Unable to establish connection at https://{}'.format(args.ipaddress))
        sys.exit()
