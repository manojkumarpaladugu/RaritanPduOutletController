import os
import hashlib
import threading
import subprocess

class TimeoutException(Exception): pass

class ThreadWithReturnValue(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=[], kwargs={}, Verbose=None):
        threading.Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
        self.exception = None

    def run(self):
        if self._target is not None:
            try:
                self._return = self._target(*self._args,
                                            **self._kwargs)
            except Exception as ex:
                self.exception = ex

    def join(self, *args):
        threading.Thread.join(self, *args)
        if self.exception:
            raise self.exception
        return self._return

def RunThreadWithReturnValueBlocking(function, arguments=[], timeout=0):
    twrv = ThreadWithReturnValue(target=function, args=arguments)
    twrv.daemon = True
    twrv.start()
    if timeout:
        result = twrv.join(timeout)
    else:
        result = twrv.join()
    if twrv.is_alive():
        raise TimeoutException('Connection timed out')
    return result

def GetMd5OfFile(file):
    with open(file, "rb") as f:
        file_hash = hashlib.md5()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    return file_hash.hexdigest()

def StartFile(file):
    if os.name == 'nt': # Windows OS
        command = 'notepad.exe {}'.format(file)
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL)
