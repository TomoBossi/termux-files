import subprocess
import threading
import signal
import sys
import re
import curses

from time import sleep
from sensor import sensor_structure, sensor_list

global_sensor_data = {} # sensor_structure
lock = threading.Lock()

terminate_flag = False
def signal_handler(sig, frame):
    global terminate_flag
    terminate_flag = True

signal.signal(signal.SIGINT, signal_handler)

def matching_sensor(requested_sensor):
    for sensor in sensor_list:
        if requested_sensor.upper() in sensor:
            return sensor

def global_sensor_data_init(sensors: list[str]):
    global global_sensor_data
    with lock:
        for sensor in sensors:
            global_sensor_data[sensor] = sensor_structure[sensor]

def poll(sensors: list[str], delay: int):
    cmd = ['termux-sensor', '-s', f'{",".join(sensors)}', '-d', f'{delay}']
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
        if terminate_flag:
            break
        # print(f"Thread {threading.current_thread().name} is reading sensor data")
    popen.stdout.close()

def update_global_sensor_data(sensors: list[str], delay: int):
    global global_sensor_data
    global_sensor_data_init(sensors)

    sensor = None
    sensor_line = False
    sensor_line_idx = -1
    for line in poll(sensors, delay):
        if not sensor_line and '"' in line:
            sensor = line.split('"')[1]
            if not len(sensor_structure[sensor]):
                continue
            sensor_line = True
            sensor_line_idx = 0

        if sensor_line and sensor_line_idx > 1:
            if sensor_line_idx < sensor_structure[sensor].size + 2:
                with lock:
                    # print(f"Thread {threading.current_thread().name} is modifying global_var")
                    global_sensor_data[sensor][sensor_line_idx - 2] = float(re.findall(r'[+-]?\d+(?:\.\d+)?', line)[0])
            else:
                sensor_line = False
    
        sensor_line_idx += 1

def update_global_sensor_data_thread(sensors: list[str], delay: int):
    global global_sensor_data
    sensors = [matching_sensor(s) for s in sensors]
    cmd_thread = threading.Thread(target=update_global_sensor_data, args=(sensors, delay))
    cmd_thread.start()
    return cmd_thread

def main():
    if len(sys.argv) < 3:
        print(f'Usage: spy <delay (ms)> sensor_1 sensor_2 ... sensor_n')
        return

    delay = int(sys.argv[1])
    sensors = sys.argv[2:]
    stdscr = curses.initscr()
    curses.curs_set(0)
    cmd_thread = update_global_sensor_data_thread(sensors, delay)

    while not terminate_flag:
        main_loop(stdscr)
        sleep(delay/1000)

    cmd_thread.join()
    curses.endwin()    

def main_loop(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, '{')
    for idx, key in enumerate(global_sensor_data.keys(), start=1):
        stdscr.addstr(idx, 0, f'\t{key}: {list(global_sensor_data[key])}')
    stdscr.addstr(idx+1, 0, '}')
    stdscr.addstr(idx+2, 0, '')
    stdscr.refresh()

if __name__ == '__main__':
    main()
