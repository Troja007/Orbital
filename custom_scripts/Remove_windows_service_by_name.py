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
            print(f"Failed to remove service '{service_name}'. Error: {result.stdout} {result.stderr}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    service_name = "background"
    remove_service(service_name)
