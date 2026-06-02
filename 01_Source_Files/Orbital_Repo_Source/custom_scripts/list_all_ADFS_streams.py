import sys
import os
import subprocess

def list_ads_streams(filepath, filename):
    try:
        # Construct the full file path
        full_file_path = os.path.join(filepath, filename)

        # PowerShell command to list ADS streams
        list_ads_cmd = f'PowerShell -Command "Get-Item -Path \'{full_file_path}\' -Stream * | Select-Object Stream"'

        # Execute command and capture output
        result = subprocess.run(list_ads_cmd, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            output = result.stdout.strip()
            if output:
                print(f"Available ADS streams for '{full_file_path}':\n")
                print(output)
            else:
                print(f"No ADS streams found for '{full_file_path}'")
        else:
            print(f"Error listing ADS streams: {result.stderr}", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    filepath = '{{ .filepath }}'   # Directory path parameter
    filename = '{{ .filename }}'   # File name parameter

    if len(filepath) > 0 and len(filename) > 0:
        list_ads_streams(filepath, filename)
    else:
        print("Error: Missing parameters. Please provide both filepath and filename.", file=sys.stderr)
        sys.exit(1)


