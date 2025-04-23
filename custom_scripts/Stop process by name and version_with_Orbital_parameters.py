import sys
import subprocess
import os
import ctypes
import ctypes.wintypes


def get_process_list(process_name):
    try:
        result = subprocess.run(['tasklist', '/FI', f'IMAGENAME eq {process_name}'], capture_output=True, text=True)
        lines = result.stdout.splitlines()
        pids = []

        for line in lines:
            if process_name.lower() in line.lower():
                parts = line.split()
                if len(parts) > 1 and parts[0].lower() == process_name.lower():
                    pids.append(parts[1])
        return pids
    except Exception as e:
        print(f"Error getting process list: {e}", file=sys.stderr)
        return []


def get_process_path(pid):
    try:
        cmd = f'wmic process where ProcessId={pid} get ExecutablePath /value'
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        for line in result.stdout.splitlines():
            if line.strip().lower().startswith('executablepath'):
                _, path = line.strip().split('=', 1)
                return path.strip()
    except Exception as e:
        print(f"Error getting process path: {e}", file=sys.stderr)
    return None


def get_file_version(file_path):
    size = ctypes.windll.version.GetFileVersionInfoSizeW(file_path, None)
    if size == 0:
        return None

    res = ctypes.create_string_buffer(size)
    ctypes.windll.version.GetFileVersionInfoW(file_path, 0, size, res)

    r = ctypes.wintypes.LPVOID()
    l = ctypes.wintypes.UINT()
    if ctypes.windll.version.VerQueryValueW(res, '\\', ctypes.byref(r), ctypes.byref(l)) == 0:
        return None

    class VS_FIXEDFILEINFO(ctypes.Structure):
        _fields_ = [
            ('dwSignature', ctypes.wintypes.DWORD),
            ('dwStrucVersion', ctypes.wintypes.DWORD),
            ('dwFileVersionMS', ctypes.wintypes.DWORD),
            ('dwFileVersionLS', ctypes.wintypes.DWORD),
            ('dwProductVersionMS', ctypes.wintypes.DWORD),
            ('dwProductVersionLS', ctypes.wintypes.DWORD),
            ('dwFileFlagsMask', ctypes.wintypes.DWORD),
            ('dwFileFlags', ctypes.wintypes.DWORD),
            ('dwFileOS', ctypes.wintypes.DWORD),
            ('dwFileType', ctypes.wintypes.DWORD),
            ('dwFileSubtype', ctypes.wintypes.DWORD),
            ('dwFileDateMS', ctypes.wintypes.DWORD),
            ('dwFileDateLS', ctypes.wintypes.DWORD),
        ]

    info = ctypes.cast(r.value, ctypes.POINTER(VS_FIXEDFILEINFO)).contents
    major = info.dwFileVersionMS >> 16
    minor = info.dwFileVersionMS & 0xFFFF
    build = info.dwFileVersionLS >> 16
    revision = info.dwFileVersionLS & 0xFFFF

    return f"{major}.{minor}.{build}.{revision}"


def kill_process(pid):
    try:
        subprocess.run(['taskkill', '/PID', pid, '/F'], capture_output=True, text=True)
        print(f"Process with PID {pid} terminated.")
    except Exception as e:
        print(f"Failed to kill process {pid}: {e}", file=sys.stderr)


def kill_matching_version(process_name, target_version):
    pids = get_process_list(process_name)
    if not pids:
        print(f"No running process found with name: {process_name}")
        return

    for pid in pids:
        exe_path = get_process_path(pid)
        if not exe_path or not os.path.exists(exe_path):
            continue

        version = get_file_version(exe_path)
        if version == target_version:
            print(f"Found matching version {version} for PID {pid}. Killing process.")
            kill_process(pid)
        else:
            print(f"Process PID {pid} has version {version}. Not killing.")


if __name__ == '__main__':
    process_name = '{{ .process_name }}'
    target_version = '{{ .target_version }}'

    if not process_name or not target_version:
        print("Error: One or more required parameters are missing.", file=sys.stderr)
        sys.exit(1)

    kill_matching_version(process_name, target_version)