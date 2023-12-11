import platform
import sys
import pathlib
import psutil as ps
import os
import subprocess as sp
import matplotlib.pyplot as plt


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
            pinfo = proc.as_dict(attrs=['ppid', 'pid', 'name', 'exe'])
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
            name2 = name.capitalize()
            if pinfo['name'] == name or pinfo['name'] == name2:
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


def kill_proces(pid):
    try:
        proc = ps.Process(pid)
    except ps.NoSuchProcess:
        raise ValueError(f"The process with the PID {pid} no longer exists.")
    else:
        proc.kill()
        # os.kill(pid, signal.SIGILL)
        print(f"The process with the PID {pid} is killed.")


def start_proces(path, params=None):
    # start a process with the given path and params
    try:
        command = [path]
        if params is not None:
            command.extend(params.split())

        if platform.system() == 'Windows':
            # On Windows, use CREATE_NEW_PROCESS_GROUP to detach the process
            proc = sp.Popen(command, creationflags=sp.CREATE_NEW_PROCESS_GROUP)
        else:
            proc = sp.Popen(command, preexec_fn=os.setpgrp)  # On Unix-like systems

    except FileNotFoundError:
        raise ValueError(f"Executable {path} not found.")
    else:
        print(f"Process with PID {proc.pid} has been started.")
        return proc.pid


def info():
    # get the cpu usage
    cpu_usage = ps.cpu_percent()
    # get the memory usage
    memory_usage = ps.virtual_memory().percent

    print("CPU usage: ", cpu_usage)
    print("Memory usage: ", memory_usage)

    # PLOT CPU
    # make a pie chart
    labels = 'Used', 'Free'
    sizes = [cpu_usage, 100 - cpu_usage]
    explode = (0, 0.1)
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=False, startangle=90)
    ax1.axis('equal')
    plt.title("CPU Usage")
    plt.show()

    # PLOT MEMORY
    sizes = [memory_usage, 100 - memory_usage]
    explode = (0, 0.1)
    fig2, ax2 = plt.subplots()
    ax2.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=False, startangle=90)
    ax2.axis('equal')
    plt.title("Memory Usage")
    plt.show()


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
    elif command == "kill":
        pid = int(sys.argv[2])
        kill_proces(pid)
    elif command == "run":
        path = sys.argv[2]
        # if params is empty, it will be None
        if len(sys.argv) == 3:
            params = None
        else:
            params = sys.argv[3]
        start_proces(path, params)
    elif command == "info":
        info()
    else:
        print("Invalid command. Type 'help' for a list of commands.")
