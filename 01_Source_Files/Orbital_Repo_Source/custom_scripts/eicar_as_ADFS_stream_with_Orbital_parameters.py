import sys
import subprocess

def write_eicar_ads(filepath, ads_name):
    try:
        eicar_string = "X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"

        # PowerShell command to create the base file
        create_file_cmd = f'PowerShell -Command "Set-Content \'{filepath}\' \'Nothing to see here.\'"'

        # PowerShell command to write EICAR to an ADS
        write_ads_cmd = f'PowerShell -Command "Set-Content \'{filepath}:{ads_name}\' \'{eicar_string}\'"'

        # Execute commands
        subprocess.run(create_file_cmd, shell=True, capture_output=True, text=True)
        subprocess.run(write_ads_cmd, shell=True, capture_output=True, text=True)

        print(f"EICAR test string written to Alternate Data Stream '{ads_name}' in file '{filepath}'")

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    filepath = '{{ .filepath }}'  # File path parameter
    ads_name = '{{ .ads_name }}'  # ADS stream name parameter

    if len(filepath) > 0 and len(ads_name) > 0:
        write_eicar_ads(filepath, ads_name)
    else:
        print("Error: Missing parameters. Please provide both filepath and ADS stream name.", file=sys.stderr)
        sys.exit(1)
