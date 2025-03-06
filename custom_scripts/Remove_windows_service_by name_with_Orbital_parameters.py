import sys
import subprocess


def remove_service(service_name):
    try:
        # Stop the service if it's running
        subprocess.run(["sc", "stop", service_name], capture_output=True, text=True)

        # Delete the service
        result = subprocess.run(["sc", "delete", service_name], capture_output=True, text=True)

        if "SUCCESS" in result.stdout:
            print(f"Service '{service_name}' removed successfully.")
        else:
            print(f"Failed to remove service '{service_name}'. Error: {result.stdout} {result.stderr}", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    service_name = '{{ .service_name }}'  # Parameterized input for DFIR tool
    if len(service_name) > 0:
        remove_service(service_name)
    else:
        print("Error: The service name parameter is missing.", file=sys.stderr)
        sys.exit(1)