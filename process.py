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
            pinfo = proc.as_dict(attrs=['pid', 'name', 'exe'])
        except ps.NoSuchProcess:
            raise ValueError(f"The process with the PID {proc.pid} no longer exists.")
        else:
            print(pinfo)


if __name__ == "__main__":
    print("Welcome to the process manager!")
    print("Type 'help' to see the available commands.")
    command = sys.argv[1]
    if command == "help":
        my_help()
    elif command == "view":
        view_processes()
