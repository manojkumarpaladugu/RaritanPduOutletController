import os
import MiscLib
import textwrap
import argparse
from   version                    import __version__
from   RaritanPduOutletController import *

# Environment variables
PDU_HOST        = 'PDU_IP'
PDU_USERNAME    = 'PDU_USERNAME'
PDU_PASSWORD    = 'PDU_PASSWORD'
TIMEOUT_SECONDS = 5

if __name__ == '__main__':
    additionalInfo = textwrap.dedent('''\
        Additional Information:
            The following environment variables will override the connection:
                {0}
                {1}
                {2}'''.format(PDU_HOST, PDU_USERNAME, PDU_PASSWORD))
    argParser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, epilog=additionalInfo)
    argParser.add_argument('-v' , action='version'                                , version="%(prog)s ("+__version__+")")
    argParser.add_argument('-i' , help='PDU IP address'                           , default='None')
    argParser.add_argument('-u' , help='PDU username'                             , default='None')
    argParser.add_argument('-p' , help='PDU password'                             , default='None')
    argParser.add_argument('-o' , help='PDU outlet number'                        , required=True)
    argParser.add_argument('-s' , help='Set PDU outlet power state (on|off|cycle)', required=True)
    args = argParser.parse_args()

    pduIpAddress     = os.environ.get(PDU_HOST    , args.i)
    pduUsername      = os.environ.get(PDU_USERNAME, args.u)
    pduPassword      = os.environ.get(PDU_PASSWORD, args.p)
    outletController = RaritanPduOutletController('/model/pdu/0', pduIpAddress, pduUsername, pduPassword)
    pduOutletNumber  = int(args.o)
    pduState         = args.s

    try:
        outlets = MiscLib.RunThreadWithReturnValueBlocking(function=outletController.ConnectToPdu, timeout=TIMEOUT_SECONDS)
        if pduOutletNumber > len(outlets):
            raise ValueError('Outlet number {0} is exceeding the maximum limit {1}'.format(pduOutletNumber,
                                                                                           len(outlets)))

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
            raise ValueError('Unrecognised option \'-s {}\''.format(pduState))
    except ValueError as message:
        print('ERROR:', message)
    except MiscLib.TimeoutException as message:
        print('ERROR: {0} [IP={1}, Username={2}, Password={3}]'.format(message,
                                                                       pduIpAddress,
                                                                       pduUsername,
                                                                       pduPassword))
    except RaritanPduException as message:
        print('ERROR: {0} [IP={1}, Username={2}, Password={3}]'.format(message,
                                                                       pduIpAddress,
                                                                       pduUsername,
                                                                       pduPassword))
    except:
        print('ERROR: Unknown exception occurred')
