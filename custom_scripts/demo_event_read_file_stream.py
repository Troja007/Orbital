import sys
import subprocess

def read_eicar_ads(filepath, ads_name):
    try:
        # PowerShell command to read the ADS content
        read_ads_cmd = f'PowerShell -Command "Get-Content \'{filepath}:{ads_name}\'"'

        # Execute command and capture output
        result = subprocess.run(read_ads_cmd, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"Contents of ADS '{ads_name}' in file '{filepath}':\n")
            print(result.stdout)
        else:
            print(f"Error reading ADS: {result.stderr}", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    filepath = '{{ .filepath }}'  # File path parameter
    ads_name = '{{ .ads_name }}'  # ADS stream name parameter

    if len(filepath) > 0 and len(ads_name) > 0:
        read_eicar_ads(filepath, ads_name)
    else:
        print("Error: Missing parameters. Please provide both filepath and ADS stream name.", file=sys.stderr)
        sys.exit(1)
