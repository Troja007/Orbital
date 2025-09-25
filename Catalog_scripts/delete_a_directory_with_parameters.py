import sys, os
import shutil
import platform


def handler(func, path, exc_info):
    print("Error:" + str(exc_info),  file=sys.stderr)
    sys.exit(1)
    
def delete(directory_path):
    if os.path.isdir(directory_path):
        shutil.rmtree(directory_path, onerror = handler)
        print(f"The directory {directory_path} deleted successfully.")
        sys.exit(0)
    else:
        print(f"Error: The directory {directory_path} doesn't exist.",  file=sys.stderr)
        sys.exit(1)

def delete_directory(directory_path, force):

    # Flag to detect important system/apps path
    sensitive_path_detected = False

    # If force is true, no path exclusions
    if force:
        delete(directory_path)

    # Check system or apps path to avoid accidental removal of protected directory
    if (platform.system() == "Windows"):
        winpath = os.environ['WINDIR'].upper() 
        if (directory_path.upper().startswith(winpath) or "PROGRAM FILES" in directory_path.upper()  or "CISCO" in directory_path.upper()):
            sensitive_path_detected = True
    else:   
        if "/System/" in directory_path or "/Applications/" in directory_path or "/usr/bin" in directory_path or "/usr/lib" in directory_path or "Cisco" in directory_path:
            sensitive_path_detected = True

    # Can't delete if force is false and protected path detected
    if sensitive_path_detected:
        print(f"Error: Cannot delete because protected path is detected in the directory path. If you really want to delete this directory, please set force parameter to \"True\"",  file=sys.stderr)
        sys.exit(1) 

    else:
        delete(directory_path)

if __name__ == '__main__':
    directory_path = '{{ .directory_path }}'
    force = '{{ .force }}'
    if len(directory_path) > 0 and (force.upper() == "TRUE" or force.upper() == "FALSE"):
        if force.upper() == "TRUE":
            force = True
        else:
            force = False
        delete_directory(directory_path, force)
    else:
        print("Error: parameters missing or incorrect. Force parameter should be \"True\" or \"False\".",  file=sys.stderr)
        sys.exit(1)
