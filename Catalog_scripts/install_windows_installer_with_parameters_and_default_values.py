import os, sys, subprocess

def error_handler(message, exitFlag=True):
  print(message, file=sys.stderr)
  if not exitFlag:
    return
  sys.exit(1)

def install_installer(directory, filename):
  installer_path = os.path.join(directory, filename)

  ext = os.path.splitext(filename)[1].lower()

  if ext == ".msi":
    args = ["msiexec.exe", "/i", installer_path, "/quiet", "/norestart"]
  elif ext == ".exe":
    args = [installer_path, "/S"]
  else:
    error_handler(f"Unsupported installer extension: {ext}")

  if not os.path.isfile(installer_path):
    error_handler(f"Installer not found: {installer_path}")

  print(f"[+] Running installer silently: {' '.join(args)}")

  result = subprocess.run(args, capture_output=True)

  if result.returncode == 0:
    print("[✓] Installation completed successfully.")
    sys.exit(0)
  else:
    error_handler(f" Installation failed with exit code: {result.returncode}")
    print(f"stdout: {result.stdout.decode(errors='ignore')}")
    print(f"stderr: {result.stderr.decode(errors='ignore')}", file=sys.stderr)
    sys.exit(result.returncode)

def main():
  directory = "{{ .path }}"
  filename = "{{ .filename }}"

  if not directory or not filename:
    error_handler("Variables 'path' and 'filename' are required.")

  install_installer(directory, filename)
  sys.exit(0)

if __name__ == "__main__":
  main()