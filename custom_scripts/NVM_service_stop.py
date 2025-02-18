import platform
import os
import sys
import subprocess

def stop_service(service_name):
    if (platform.system() == "Windows"):
        # windows command
        cmd = f"net stop {service_name}"
    elif (platform.system() == "Darwin"):
        # macos command
        cmd = f"launchctl unload {service_name}"
    elif (platform.system() == "Linux"):
        # linux command
        cmd = f"systemctl stop {service_name} "
    try:
        proc = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        print("Success")
    except subprocess.CalledProcessError as err:
        print(err.output.decode("utf-8"), file=sys.stderr)
        sys.exit(1)
if __name__ == "__main__":
    service_name = '{{ .service_name }}'
    if " " in service_name and not service_name.startswith('"'):
        service_name = f"\"{service_name}\""
    if service_name != "":
        try:
            stop_service(service_name)
        except Exception as e:
            print(str(e), file=sys.stderr)
            sys.exit(1)
    else:
        print(f"Error: service name is missing. Please provide service name in the service_name parameter to continue. For Darwin system provide the full path to plist.", file=sys.stderr)
        sys.exit(1)