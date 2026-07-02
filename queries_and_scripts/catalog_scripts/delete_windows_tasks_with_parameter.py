import sys
import subprocess


def delete_task(scheduled_task_name):
    try:  
        cmd =  "schtasks", "/delete", "/F", "/TN", scheduled_task_name
        subprocess.check_call(cmd )
    except:
        sys.exit(1)

if __name__ == '__main__':
    scheduled_task_name = '{{ .scheduled_task_name }}'
    if len(scheduled_task_name) > 0:
        delete_task(scheduled_task_name)
    else:
        print("Error: The task name parameter is missing.",  file=sys.stderr)
        sys.exit(1)

