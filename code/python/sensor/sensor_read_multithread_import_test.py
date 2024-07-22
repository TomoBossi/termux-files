import sensor_read as s

# importing works
# global variable from imported module works
# background process on a different thread works and does not affect stdout

# multithreading does not work because termux-sensor does not support it

if __name__ == '__main__':
    cmd_thread_1 = s.update_global_sensor_data_thread(['light'], 600)
    # cmd_thread_2 = s.update_global_sensor_data_thread(['gravity'], 600)
    while not s.terminate_flag:
        print(f'{s.global_sensor_data["LIGHT"]} {s.global_sensor_data["GRAVITY"]}{" "*50}', end='\r')
        s.sleep(0.1)
    cmd_thread_1.join()
    # cmd_thread_2.join()
