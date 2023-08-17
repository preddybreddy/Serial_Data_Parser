import time
import serial
import os 

# str_input format - Total Run Time hrs:mins:secs 0:28:30    ULC_1XXX_LS_3_01  boost duty cycle 10 percent & delay SH start each comp off, int burn 50-5, int reset when suct press > 25
def extract_time(str_input):
    time_label_index = str_input.index('hrs:mins:secs')
    offset = len('hrs:mins:secs')
    time_start_index = time_label_index + offset + 1
    sub_str = str_input[time_start_index:]
    end_index = sub_str.index(' ')
    time_str = sub_str[:end_index]
    time_str_list = time_str.split(':')
    return time.mktime(generate_time_tuple(time_str_list[0], time_str_list[1], time_str_list[2]))


def generate_time_tuple(hh,mm,ss):
    # The values other than hh, mm, ss do not seem to matter
    return (2022, 12, 28, int(hh), int(mm), int(ss), 4, 1, 0)

def extract_ULC_version(str_input_0):
    start_index = str_input_0.index('ULC')
    sub_str = str_input_0[start_index:]
    end_index = sub_str.index(' ')
    return sub_str[:end_index]

def extract_state(str_input_1):
    start_index = str_input_1.index('state') + len('state') + 1
    return str_input_1[start_index: ]

def extract_superheat_evap_suction_solenoids(str_input_3_4, label):
    start_index = str_input_3_4.index(label) + len(label) + 1
    sub_str = str_input_3_4[start_index: ]
    end_index = sub_str.index(',')
    return sub_str[:end_index]


def get_valid_input(serial_obj):
    lines_from_ULC = []
    first_line = serial_obj.readline().decode('ASCII')
    while 'Total Run Time' not in first_line:
        first_line = serial_obj.readline().decode('ASCII')

    lines_from_ULC.append(first_line)    
    first_line = serial_obj.readline().decode('ASCII')
    while ('*' not in first_line):
        lines_from_ULC.append(first_line)
        first_line = serial_obj.readline().decode('ASCII')
    return lines_from_ULC

def strip_line(input_list):
    return list(map(lambda x: x.strip(), input_list))

def remove_empty_string(input_list):
    return list(filter( lambda x: x != '', (filter(lambda x: x.isspace() == False, input_list))))


def configure_com_port(com_port):
    serial_obj = serial.Serial(f'com{com_port}')
    serial_obj.baudrate = 9600
    serial_obj.bytesize = 8
    serial_obj.parity = 'N'
    serial_obj.stopbits = 1
    return serial_obj


def output_table(com_port, generate_table_func):
    serial_obj = configure_com_port(com_port)
    prev_time = 0
    while(True):
        output_set = get_valid_input(serial_obj)
        output_set_stripped = strip_line(output_set)
        output_set_empty_strings_removed = remove_empty_string(output_set_stripped)
        curr_time = extract_time(output_set_stripped[0])
        #print(curr_time)
        if not(prev_time == 0 or abs(curr_time - prev_time) == 10):
            print('Data is not synchronized with 10-sec intervals\n')
            print('Restart process')
        # output table
        os.system('cls')
        generate_table_func(output_set_empty_strings_removed)
        prev_time = curr_time
        time.sleep(9.5)