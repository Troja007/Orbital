import sys
import os

def write_malware_test_file(filepath, filename):
    try:
        test_string = "X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"
        file_path = os.path.join(filepath, filename)

        # Ensure directory exists
        os.makedirs(filepath, exist_ok=True)

        with open(file_path, "w") as f:
            f.write(test_string)

        print(f"Malware test file written to: {file_path}")

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    filepath = '{{ .filepath }}'  # Path parameter from the UI
    filename = '{{ .filename }}'  # Filename parameter from the UI

    if len(filepath) > 0 and len(filename) > 0:
        write_malware_test_file(filepath, filename)
    else:
        print("Error: Missing parameters. Please provide both filename and filepath.", file=sys.stderr)
        sys.exit(1)
