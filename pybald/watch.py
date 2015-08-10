import sys
import os
import time
import signal

# ======
file_modification_times = {}


def is_modified(filename):
    '''
    Returns True if the file referenced by filename has been modified
    since the last time this funciton was called, otherwise False.
    '''
    new_modified_time = os.path.getmtime(filename)
    last_modified_time = file_modification_times.get(filename, None)
    if last_modified_time is None:
        file_modification_times[filename] = new_modified_time
        return False
    if last_modified_time < new_modified_time:
        file_modification_times[filename] = new_modified_time
        return True
    else:
        return False


def watch_module_files(pid=None):
    '''
    Continuously monitors all loaded modules and issues a POSIX SIGHUP if 
    any of the files associated with the loaded modules are changed during
    runtime.
    '''
    while True:
        changed = False
        for filename in filter(None, (getattr(module, '__file__', None) for
                                module in set(filter(None, sys.modules.values())))):
            changed = is_modified(filename)
            #print filename, changed
            if filename.endswith(".pyc") and os.path.exists(filename[:-1]):
                changed = changed or is_modified(filename[:-1])
                #print filename[:-1], changed
            if changed:
                print("File Changed!")
                os.kill(pid, signal.SIGHUP)
        time.sleep(1)
