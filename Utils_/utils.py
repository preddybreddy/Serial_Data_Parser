import time
import serial
import os

# Reads serial data from the board and converts it into ASCII
# Waits for the data to be valid i.e, only grabs data when the first line has "Total Run Time" and stops when a '*' is encountered
# Returns data in the form of a list of lines for one 10-sec interval - sample data can be found in Filtered list/ulc_filtered_list
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

# Removes trailing whitespaces from the ASCII text
def strip_line(input_list):
    return list(map(lambda x: x.strip(), input_list))

# Filters empty strings from the ASCII text
def remove_empty_string(input_list):
    return list(filter( lambda x: x != '', (filter(lambda x: x.isspace() == False, input_list))))

def configure_com_port(com_port):
    serial_obj = serial.Serial(f'com{com_port}')
    serial_obj.baudrate = 9600
    serial_obj.bytesize = 8
    serial_obj.parity = 'N'
    serial_obj.stopbits = 1
    return serial_obj

# Outputs the grid shown in the readme with updated data every 10 seconds
# Every 10 seconds a new table is generated with new values this function is called
def output_table(com_port, generate_table_func):
    serial_obj = configure_com_port(com_port)
    prev_time = 0
    while(True):
        output_set = get_valid_input(serial_obj)
        os.system('cls')
        output_set_stripped = strip_line(output_set)
        output_set_empty_strings_removed = remove_empty_string(output_set_stripped)
        curr_time = extract_time(output_set_stripped[0])
        # This check ensures the table data is being refreshed every 10 seconds 
        # If not informs the user that data is out of sync
        if not(prev_time == 0 or abs(curr_time - prev_time) == 10):
            print('Data is not synchronized with 10-sec intervals\n')
            print('Restart process')
        # output table
        generate_table_func(output_set_empty_strings_removed)
        prev_time = curr_time
        time.sleep(9.5)
        
# str_input = "Total Run Time hrs:mins:secs 0:28:30    ULC_1XXX_LS_3_01  boost duty cycle 10 percent & delay SH start each comp off, int burn 50-5, int reset when suct press > 25"
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

# str_input_0 = "Total Run Time hrs:mins:secs 0:28:30    ULC_1XXX_LS_3_01  boost duty cycle 10 percent & delay SH start each comp off, int burn 50-5, int reset when suct press > 25"
def extract_ULC_version(str_input_0):
    start_index = str_input_0.index('ULC')
    sub_str = str_input_0[start_index:]
    end_index = sub_str.index(' ')
    return sub_str[:end_index]

# str_input_1 = 'DIPS = 4-6-15-20 default 4  Duty 40-41-43-44 default 42        state REFRIG C-OFF',
def extract_state(str_input_1):
    start_index = str_input_1.index('state') + len('state') + 1
    return str_input_1[start_index: ]

# str_input_3_4 = 'Super Heat 127.4, Evap Out 25.2, Suction Pressure 5.7, Suction Pressure Limit in REFRIG 25.0, SH Error 0.0, SH Target 4.0, Liquid PWM Solenoid Duty 10.0,'
def extract_superheat_evap_suction_solenoids(str_input_3_4, label):
    start_index = str_input_3_4.index(label) + len(label) + 1
    sub_str = str_input_3_4[start_index: ]
    end_index = sub_str.index(',')
    return sub_str[:end_index]


