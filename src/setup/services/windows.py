import sys
import logging
import peewee as pw

import win32serviceutil
import win32service
import win32event
import servicemanager
import time

import config

import upact.fences.web as web_fence
import upact.platforms
from upact.models import database_proxy


class UpactWebSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "UpactWebService"
    _svc_display_name_ = "Upact Web Service"

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        self._running = False

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self._running = False

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_,''))
        self._running = True
        self.main()

    def main(self):
        logging.basicConfig(
            format='%(asctime)s %(levelname)-8s %(message)s',
            level=logging.INFO,
            datefmt='%Y-%m-%d %H:%M:%S')

        logging.info("Starting upact web")

        db = pw.SqliteDatabase(config.DATABASE_FILE)
        logging.info(f"Connecting to database at {config.DATABASE_FILE}")
        db.connect()
        database_proxy.initialize(db)
        logging.info("Connection successful")

        windows = upact.platforms['Windows']

        logging.info("Updating permanently blocked ips")

        windows.update_firewall(
            ips_to_block=web_fence.permanently_blocked_ips(db),
            ips_to_unblock=[],
            config=config,
            rule_name="upact permanently_blocked_ips")

        logging.info("Update successful")

        
        while self._running:
            windows.update_firewall(
                ips_to_block=web_fence.blocked_ips_from_urls(db),
                ips_to_unblock=[],
                config=config,
                rule_name="upact ips from urls")

            time.sleep(5 * 60)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Called by Windows shell. Handling arguments such as: Install, Remove, etc.
        win32serviceutil.HandleCommandLine(UpactWebSvc)
    else:
        # Called by Windows Service. Initialize the service to communicate with the system operator
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(UpactWebSvc)
        servicemanager.StartServiceCtrlDispatcher()
