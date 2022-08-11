import sys

import win32serviceutil
import win32service
import win32event
import servicemanager
import time

import config

import upact.platforms


class UpactWebSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "UpactWebService"
    _svc_display_name_ = "Upact Web Service"

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        self.platform = upact.platforms.Windows(config)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.platform.stop_service()

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_,''))
        self.main()

    def main(self):
        self.platform.start_service()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Called by Windows shell. Handling arguments such as: Install, Remove, etc.
        win32serviceutil.HandleCommandLine(UpactWebSvc)
    else:
        # Called by Windows Service. Initialize the service to communicate with the system operator
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(UpactWebSvc)
        servicemanager.StartServiceCtrlDispatcher()
