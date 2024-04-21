import subprocess
# import asyncio
# import json
# import time

def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line 
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
         raise subprocess.CalledProcessError(return_code, cmd)


# light = json.loads(subprocess.run(['termux-sensor', '-s', 'LIGHT', '-n', '3'], capture_output = True, text = True).stdout)['LIGHT']['values'][

light = 0
line_idx = 0
try:
    for line in execute(['termux-sensor', '-s', 'LIGHT', '-d', '50']): # , '-n', '3']):
        if line_idx%7 == 3:
            light = int(line[:-1]) 
            print(f'{light:06d}', end = '\r')
        line_idx += 1
except KeyboardInterrupt:
    for line in execute(['termux-sensor', '-c']):
        print(line)
