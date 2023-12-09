# Browser ProcessViewer (ID: 25)

![Badge](https://img.shields.io/badge/Difficulty-B-<YELLOW>)

## Overview

Welcome to the Browser ProcessViewer repository! This Python script allows you to perform various operations on processes, offering a set of powerful features to interact with and manage processes on your machine. Whether you're a developer, system administrator, or just someone who loves exploring the depths of their system, Browser ProcessViewer has you covered.

## Features

1. **View Current Processes**
   - Display a list of currently running processes with details such as PID, Name, and Path.

2. **Suspend/Resume Processes**
   - Suspend or resume a specific process by providing its PID.

3. **Start/Stop Processes**
   - Start or stop a process, including the ability to use a command line for advanced control.

4. **Process Information**
   - Retrieve information about running processes, including CPU usage and memory consumption.

## Usage

   1. **Help command to see all the functionalities**
      - py process.py help

   2. **List all processes with additional information**
      - py process.py view

   3. **Suspend a process by providing its PID**
      - py process.py suspend <PID>

   4. **Stop a process by providing its PID**
      - py process.py kill <PID>

   5. **Start a process with a specified path and parameters**
      - py process.py run <path> <parameters>
