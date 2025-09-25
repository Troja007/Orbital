import os
import platform
import sys


def delete(file_path):
    try:
        os.remove(filename)
        print(f"{filename} deleted successfully")
        sys.exit(0)
    except OSError as error:
        print(f"Error: {error}",  file=sys.stderr)
        sys.exit(1)


def delete_file(filename, force):

    # Flag to detect important system/apps path
    sensitive_path_detected = False

    # If force is true, no path exclusions
    if force:
        delete(filename)

    # Check system or apps path to avoid accidental removal of important files
    if (platform.system() == "Windows"):
        winpath = os.environ['WINDIR'].upper() 
        if (filename.upper().startswith(winpath) or "PROGRAM FILES" in filename.upper()  or "CISCO" in filename.upper()):
            sensitive_path_detected = True
    else:   
        if "/System/" in filename or "/Applications/" in filename or "/usr/bin" in filename or "/usr/lib" in filename or "Cisco" in filename:
            sensitive_path_detected = True

    # Can't delete if force is false and important path detected
    if sensitive_path_detected:
        print(f"Error: Cannot delete because system/apps path detected in the file path. If you really want to delete this file, please set force parameter to \"True\"",  file=sys.stderr)
        sys.exit(1) 

    else:
        delete(filename)

if __name__ == '__main__':
    filename = '{{ .file_path }}'
    force = '{{ .force }}'
    if len(filename) > 0 and (force.upper() == "TRUE" or force.upper() == "FALSE"):
        if force.upper() == "TRUE":
            force = True
        else:
            force = False
        delete_file(filename, force)
    else:
        print("Error: parameters missing or incorrect. Force parameter should be \"True\" or \"False\"",  file=sys.stderr)
        sys.exit(1)
