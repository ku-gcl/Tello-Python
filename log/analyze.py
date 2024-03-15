from tello import Tello
import sys
from datetime import datetime
import threading
import time
import os
import socket
import pandas as pd

OUTPUT = True
INTERVAL = 0.5
DATA_NAME = ['pitch', 'roll', 'yaw', 'vgx', 'vgy', 'vgz', 'templ', 'temph', 'tof', 'h', 'bat', 'baro', 'time', 'agx', 'agy', 'agz']
result = []    # global variable for save drone's state data

"""
Add emergency stop fucntion
Pushing ctrl+c for EMERGENCY STOP
"""

start_time = str(datetime.now())
file_path = '/Users/tatsuya_1/Documents/Tello-Python/Single_Tello_Test'
file_name = os.path.join(file_path, 'command_debug.txt')
# file_name = os.path.join(file_path, 'command_rectangle.txt')
f = open(file_name, "r")
commands = f.readlines()

tello = Tello()

data_ip = ''
data_port = 8890
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # sock
socket.bind((data_ip, data_port))

def data_arrange(state_str: str) -> list:
    global DATA_NAME
    state_data = []
    data_list = state_str.split(';')
    for ii in range(len(DATA_NAME)):
        data = data_list[ii]
        name = data.split(':')[0]       # data name
        value = float(data.split(':')[1])      # data value
        # Removing "b'  " for the bytes like character at the beggining of the string
        if ii == 0:
            name = name.replace("b'", "")
        # append the data to list
        if name == DATA_NAME[ii]:
            state_data.append(value)
    return state_data


def get_data(socket):
    global result
    try:
        while True:
            response, ip = socket.recvfrom(1024)
            # print("-------------get_data-----------")
            print(response)
            time.sleep(INTERVAL)
            state = data_arrange(str(response))
            result.append(state)        # append the state data to "result" list
    except KeyboardInterrupt:
        print("get_data_thread end")


try:
    ii = 0
    while ii < len(commands):
        command = commands[ii]
        if command != '' and command != '\n':
            command = command.rstrip()
            if command.find('delay') != -1:
                sec = float(command.partition('delay')[2])
                print('\n delay %s' % sec)
                time.sleep(sec)
                pass
            else:
                print('\n', command)
                tello.send_command(command)
            if ii == 0:
                # threading for get state data of the drone
                get_data_thread = threading.Thread(target=get_data, args=[socket])
                get_data_thread.daemon = True
                get_data_thread.start()
                pass
            ii += 1
except(KeyboardInterrupt, SystemExit):
    print ("ctrl+c ----- emergency stop -----")
    tello.send_command('emergency')

if OUTPUT:
    log = tello.get_log()
    LOG_PATH = 'Single_Tello_Test/log/'
    out = open(LOG_PATH + start_time + '.txt', 'w')
    for stat in log:
        # stat.print_stats()
        str_log = stat.return_stats()
        out.write(str_log)
    out.close()
    df = pd.DataFrame(result, columns=DATA_NAME)
    LOG_FILE = '{}{}_state_interval{}.csv'.format(LOG_PATH, start_time, str(INTERVAL))
    df.to_csv(LOG_FILE)
    
