import sys, subprocess

feature = "{{ .feature }}"  # Set to the Windows feature name to disable
restart = "{{ .restart }}"  # Set to 'true' to restart after disabling, 'false' to not restart

def run_subprocess(command_arguments):
  return subprocess.check_output(command_arguments, universal_newlines=True, stderr=subprocess.STDOUT)

def run_powershell_command(command_arguments):
  try:
    output = run_subprocess(command_arguments)
    return output, 0
  except subprocess.CalledProcessError as error:
    print(error.output, file=sys.stderr)
    return error.output, 1

def disable_windows_feature(feature_name, restart):
  command = ['powershell.exe', 'Disable-WindowsOptionalFeature', '-Online', '-FeatureName', feature_name]
  if restart.lower() != 'true':
    command.append('-NoRestart')
  _, returncode = run_powershell_command(command)
  return returncode

def is_feature_disabled_from_output(output):
  for line in output.splitlines():
    if 'State ' in line and 'disabled' in line.lower():
      return True
  return False

def check_if_feature_is_disabled(feature_name):
  output, _ = run_powershell_command(['powershell.exe', 'Get-WindowsOptionalFeature', '-Online', '-FeatureName', feature_name])
  return is_feature_disabled_from_output(output)

def ensure_feature_disabled(feature, restart):
  if not check_if_feature_is_disabled(feature):
    disable_windows_feature(feature, restart)

def print_feature_status_and_exit(feature):
  if check_if_feature_is_disabled(feature):
    print(f"{feature} is now disabled.")
    sys.exit(0)
  else:
    sys.exit(1)

def main():
  ensure_feature_disabled(feature, restart)
  print_feature_status_and_exit(feature)

if __name__ == '__main__':
  main()