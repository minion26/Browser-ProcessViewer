import platform
import sys
import pathlib
import psutil as ps
import os
import subprocess as sp


def my_help():
    print("Available commands:")
    print("help - displays this list of commands")
    print("view - displays the current processes")
    print("kill <PID> - kills the process with the PID ID")
    print("run <PATH> <PARAMS>- runs the process at the specified PATH with the specified PARAMS")
    print("suspend <PID> - suspends the process with the PID ID")
    print("resume <PID> - resumes the process with the PID ID")


def view_processes():
    print("Current processes:")
    for proc in ps.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['ppid','pid', 'name', 'exe'])
        except ps.NoSuchProcess:
            raise ValueError(f"The process with the PID {proc.pid} no longer exists.")
        else:
            print(pinfo)


def view_processes_by_name(name):
    for proc in ps.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['ppid', 'pid', 'name', 'exe'])
        except ps.NoSuchProcess:
            raise ValueError(f"The process with the PID {proc.pid} no longer exists.")
        else:
            if pinfo['name'] == name:
                print(pinfo)


def suspend_process(pid):
    try:
        proc = ps.Process(pid)
    except ps.NoSuchProcess:
        raise ValueError(f"The process with the PID {pid} no longer exists.")
    else:
        proc.suspend()
        print(f"The process with the PID {pid} is suspended.")


def check_if_suspended(pid):
    try:
        proc = ps.Process(pid)
    except ps.NoSuchProcess:
        raise ValueError(f"The process with the PID {pid} no longer exists.")
    else:
        if proc.status() == 'stopped':
            return True

        else:
            return False


def resume_process(pid):
    try:
        proc = ps.Process(pid)
    except ps.NoSuchProcess:
        raise ValueError(f"The process with the PID {pid} no longer exists.")
    else:
        if check_if_suspended(pid):
            proc.resume()
            print(f"The process with the PID {pid} is resumed.")


if __name__ == "__main__":
    command = sys.argv[1]
    if command == "help":
        my_help()
    elif command == "view":
        view_processes()
    elif command == "view_by_name":
        name = sys.argv[2]
        view_processes_by_name(name)
    elif command == "suspend":
        pid = int(sys.argv[2])
        suspend_process(pid)
        check_if_suspended(pid)
    elif command == "resume":
        pid = int(sys.argv[2])
        resume_process(pid)