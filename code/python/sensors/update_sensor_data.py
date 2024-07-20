import subprocess
import threading
import time
import sys
import re
import curses

from sensor_structure import sensor_structure

global_sensor_data = {}
global_stdout_line_idx = 0

def global_sensor_data_init(sensors: list[str]):
    global global_sensor_data
    for sensor in sensors:
        global_sensor_data[sensor] = sensor_structure[sensor]

def execute(cmd: list[str]):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line 
    popen.stdout.close()

def poll(sensors: list[str], delay: int):
    cmd = ['termux-sensor', '-s', f'{",".join(sensors)}', '-d', f'{delay}']
    for stdout_line in execute(cmd):
        yield stdout_line

def update_global_sensor_data(sensors: list[str], delay: int):
    global global_sensor_data
    global global_stdout_line_idx
    global_sensor_data_init(sensors)

    sensor = None
    sensor_line = False
    sensor_line_idx = -1
    for line in poll(sensors, delay):
        if not sensor_line and '"' in line:
            sensor = line.split('"')[1]
            sensor_line = True
            sensor_line_idx = 0

        if sensor_line and sensor_line_idx > 1:
            if sensor_line_idx < sensor_structure[sensor].size + 2:
                global_sensor_data[sensor][sensor_line_idx - 2] = float(re.findall(r'[+-]?\d+(?:\.\d+)?', line)[0])
            else:
                sensor_line = False
        
        sensor_line_idx += 1
        global_stdout_line_idx += 1

def main():
    if len(sys.argv) < 3:
        print(f'Usage: python {sys.argv[0]} <delay (ms)> sensor_1 sensor_2 ... sensor_n')
        return

    delay = int(sys.argv[1])
    sensors = [s.upper() for s in sys.argv[2:]]
    stdscr = curses.initscr()

    cmd_thread = threading.Thread(target=update_global_sensor_data, args=(sensors, delay))
    cmd_thread.start()

    try:
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, '{')
            for idx, key in enumerate(global_sensor_data.keys(), start=1):
                stdscr.addstr(idx, 0, f'\t{key}: {list(global_sensor_data[key])}')
            stdscr.addstr(idx+1, 0, '}')
            stdscr.addstr(idx+2, 0, '')
            stdscr.refresh()
            time.sleep(0.3)

    except KeyboardInterrupt:
        cmd_thread.join()
        curses.endwin()
        return

if __name__ == '__main__':
    main()
