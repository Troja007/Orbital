import sys
import subprocess


def start_service(service_name):
    try:
        result = subprocess.run(["sc", "start", service_name], capture_output=True, text=True)
        if "START_PENDING" in result.stdout or "RUNNING" in result.stdout:
            print(f"Service '{service_name}' started successfully.")
        else:
            print(f"Failed to start service '{service_name}'. Error: {result.stdout} {result.stderr}", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"An error occurred while starting the service: {e}", file=sys.stderr)
        sys.exit(1)


def stop_service(service_name):
    try:
        result = subprocess.run(["sc", "stop", service_name], capture_output=True, text=True)
        if "STOP_PENDING" in result.stdout or "STOPPED" in result.stdout:
            print(f"Service '{service_name}' stopped successfully.")
        else:
            print(f"Failed to stop service '{service_name}'. Error: {result.stdout} {result.stderr}", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"An error occurred while stopping the service: {e}", file=sys.stderr)
        sys.exit(1)


def remove_service(service_name):
    try:
        stop_service(service_name)  # Attempt to stop before deletion
        result = subprocess.run(["sc", "delete", service_name], capture_output=True, text=True)
        if "SUCCESS" in result.stdout:
            print(f"Service '{service_name}' removed successfully.")
        else:
            print(f"Failed to remove service '{service_name}'. Error: {result.stdout} {result.stderr}", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"An error occurred while removing the service: {e}", file=sys.stderr)
        sys.exit(1)


def restart_service(service_name):
    stop_service(service_name)
    start_service(service_name)


def enable_service(service_name):
    try:
        result = subprocess.run(["sc", "config", service_name, "start=", "auto"], capture_output=True, text=True)
        if "SUCCESS" in result.stdout:
            print(f"Service '{service_name}' enabled (start type set to auto).")
        else:
            print(f"Failed to enable service '{service_name}'. Error: {result.stdout} {result.stderr}", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"An error occurred while enabling the service: {e}", file=sys.stderr)
        sys.exit(1)


def disable_service(service_name):
    try:
        result = subprocess.run(["sc", "config", service_name, "start=", "disabled"], capture_output=True, text=True)
        if "SUCCESS" in result.stdout:
            print(f"Service '{service_name}' disabled (start type set to disabled).")
        else:
            print(f"Failed to disable service '{service_name}'. Error: {result.stdout} {result.stderr}", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"An error occurred while disabling the service: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    service_name = '{{ .service_name }}'
    action = '{{ .action }}'.lower()

    if not service_name or not action:
        print("Error: Missing required parameters: service_name or action.", file=sys.stderr)
        sys.exit(1)

    if action == 'start':
        start_service(service_name)
    elif action == 'stop':
        stop_service(service_name)
    elif action == 'restart':
        restart_service(service_name)
    elif action == 'remove':
        remove_service(service_name)
    elif action == 'enable':
        enable_service(service_name)
    elif action == 'disable':
        disable_service(service_name)
    else:
        print(f"Error: Unsupported action '{action}'. Valid actions are: start, stop, restart, remove, enable, disable.", file=sys.stderr)
        sys.exit(1)
