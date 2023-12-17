import platform
import sys
import pathlib
import psutil as ps
import os
import subprocess as sp
import matplotlib.pyplot as plt
import argparse
import re


# TODO: use callback functions
def my_help():
    print("Available commands:")
    print("help, -h - displays this list of commands")
    print("view, -v - displays the current processes")
    print("view_by_name <NAME> - displays the processes with the specified NAME")
    print("kill <PID> - kills the process with the PID ID")
    print("run <PATH> <PARAMS>- runs the process at the specified PATH with the specified PARAMS")
    print("suspend <PID> - suspends the process with the PID ID")
    print("resume <PID> - resumes the process with the PID ID")
    print("info, -i - displays the CPU and memory usage")
    print("exit - exits the program")


def view_processes():
    print("Current processes...")
    my_list = []
    for proc in ps.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['ppid', 'pid', 'name', 'exe'])
        except ps.NoSuchProcess:
            raise ValueError(f"The process with the PID {proc.pid} no longer exists.")
        else:
            my_list.append(pinfo)

    # lista cu cate 10 elemente din my_list
    page = [my_list[i:i + 10] for i in range(0, len(my_list), 10)]
    return page


def listare(page_start):
    page = view_processes()
    nr_pages = len(page)
    if page_start >= nr_pages:
        print("No more pages.")
        return
    print(f"Page {page_start + 1} of {nr_pages}")
    print("PID\t\tPPID\t\tName\t\tPath")
    elements = len(page[page_start])
    for i in range(0, elements):
        print(page[page_start][i]['pid'], "\t\t", page[page_start][i]['ppid'], "\t\t", page[page_start][i]['name'],
              "\t\t", page[page_start][i]['exe'])


def view_processes_by_name(name):
    print("Current processes with the name provided...")
    #my_list = []
    switch = False
    for proc in ps.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['ppid', 'pid', 'name', 'exe'])
        except ps.NoSuchProcess:
            raise ValueError(f"The process with the PID {proc.pid} no longer exists.")
        else:

            # regex : ^[A-Z][a-z]*$\.exe - incepe cu litera mare, urmat de 0 sau mai multe litere mici si se termina cu .exe
            # if re.findall(r'^[A-Z][a-z]*\.exe$', pinfo['name']):
            #     print(pinfo)

            if name in pinfo['name'].lower():
                print(pinfo)
                switch = True
                # my_list.append(pinfo)
    if not switch:
        print("Nothing found.")



    # return [my_list[i:i + 10] for i in range(0, len(my_list), 10)]


# def listare_view_by_name(page_start, name):
#     my_list = view_processes_by_name(name)
#     nr_pages = len(my_list)
#     if page_start >= nr_pages:
#         print("No more pages.")
#         return
#     print(f"Page {page_start + 1} of {nr_pages}")
#     print("PID\t\tPPID\t\tName\t\tPath")
#     elements = len(my_list[page_start])
#     for i in range(0, elements):
#         print(my_list[page_start][i]['pid'], "\t\t", my_list[page_start][i]['ppid'], "\t\t",
#               my_list[page_start][i]['name'],
#               "\t\t", my_list[page_start][i]['exe'])


# function with callback
# def listare_callback(page_start, callback):
#     # what if i want to call a function that has parameters?
#     # callback(page_start, name)
#     my_list = callback()
#     nr_pages = len(my_list)
#     if page_start >= nr_pages:
#         print("No more pages.")
#         return
#     print(f"Page {page_start + 1} of {nr_pages}")
#     print("PID\t\tPPID\t\tName\t\tPath")
#     elements = len(my_list[page_start])
#     for i in range(0, elements):
#         print(my_list[page_start][i]['pid'], "\t\t", my_list[page_start][i]['ppid'], "\t\t", my_list[page_start][i]['name'],
#               "\t\t", my_list[page_start][i]['exe'])


def suspend_process(pid):
    try:
        proc = ps.Process(pid)
    except ps.NoSuchProcess:
        raise ValueError(f"The process with the PID {pid} no longer exists.")
    except ProcessLookupError:
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
    # try:
    #     command = [path]
    #     if params is not None:
    #         command.extend(params.split())
    #
    #     if platform.system() == 'Windows':
    #         # On Windows, use CREATE_NEW_PROCESS_GROUP to detach the process
    #          proc = sp.Popen(command, creationflags=sp.CREATE_NEW_PROCESS_GROUP)
    #         # proc = sp.Popen(command, shell=True, stdout=sp.PIPE, stderr=sp.PIPE, stdin=sp.PIPE)
    #     else:
    #         proc = sp.Popen(command, preexec_fn=os.setpgrp)  # On Unix-like systems
    #         # proc = sp.Popen(command, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)

    try:
        if platform.system() == 'Windows':
            cmd = "start cmd /k"
            command = [cmd, path]
            if params is not None:
                command.extend(params.split())
            command = " ".join(command)
            # print(command)

            proc = sp.Popen(command, shell=True, stdout=sp.PIPE, stderr=sp.PIPE, stdin=sp.PIPE)
        elif platform.system() == 'Linux':
            cmd = "gnome-terminal -e"
            command = [cmd, path]
            if params is not None:
                command.extend(params.split())
            command = " ".join(command)
            # print(command)

            proc = sp.Popen(command, shell=True, stdout=sp.PIPE, stderr=sp.PIPE, stdin=sp.PIPE)

    except FileNotFoundError:
        raise ValueError(f"Executable {path} not found.")
    else:
        print(f"Process with PID {proc.pid} has been started.")
        return proc.pid


def info():
    # get the cpu usage
    cpu_usage = ps.cpu_percent(10)
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
    # command = sys.argv[1]
    # if command == "start":
    start_page = 0
    while True:
        command = input("Enter command: ")
        if command == "help" or command == "-h":
            my_help()
        elif command == "view" or command == "-v":
            print("Type 'next' to see the next page and 'exit' to exit.")
            while True:
                listare(start_page)
                # listare_callback(start_page, view_processes)
                command = input("Enter command for viewing processes: ")
                if command == "next":
                    start_page += 1
                elif command == "exit":
                    break
        elif command == "view_by_name":
            name = input("Enter name: ")
            view_processes_by_name(name)
            # print("Type 'next' to see the next page and 'exit' to exit.")
            # while True:
            #     listare_view_by_name(start_page, name)
            #     # listare_callback(start_page, view_processes_by_name(name))
            #     command = input("Enter command for viewing processes: ")
            #     if command == "next":
            #         start_page += 1
            #     elif command == "exit":
            #         break
        elif command == "suspend":
            pid = int(input("Enter PID: "))
            suspend_process(pid)
        elif command == "resume":
            pid = int(input("Enter PID: "))
            resume_process(pid)
        elif command == "kill":
            pid = int(input("Enter PID: "))
            kill_proces(pid)
        elif command == "run":
            path = input("Enter path: ")
            params = input("Enter params: ")
            start_proces(path, params)
        elif command == "info" or command == "-i":
            info()
        elif command == "exit":
            break
        else:
            print("Invalid command. Type 'help' or '-h' for a list of commands.")
