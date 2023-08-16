import serial
import time
import Utils_.utils as utils
import Utils_.utils_selay_ls as utils_selay_ls
import os
from tabulate import tabulate
import tkinter as tk


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

def generate_table(current_data_from_ULC_formatted):
    head = ['Parameter', '\"Raw Data\"/DISPLAY']
    properties = ['Software Version', 'STATE', 'SUPERHEAT', 'EVAP OUT', 'SUCTION PRESSURE', 'LIQUID SOLENOID DUTY', 'SH Error', 'HOT GAS DUTY']
    values = [utils_selay_ls.extract_SCAB_version(current_data_from_ULC_formatted[0]), utils.extract_state(current_data_from_ULC_formatted[1]), 
     utils.extract_superheat_evap_suction_solenoids(current_data_from_ULC_formatted[2], 'Super Heat'), 
     utils.extract_superheat_evap_suction_solenoids(current_data_from_ULC_formatted[2], 'Evap Out'),
     utils.extract_superheat_evap_suction_solenoids(current_data_from_ULC_formatted[2], 'Suction Pressure'),
     utils.extract_superheat_evap_suction_solenoids(current_data_from_ULC_formatted[2], 'Liquid PWM Solenoid Duty'),
     utils.extract_superheat_evap_suction_solenoids(current_data_from_ULC_formatted[2], 'SH Target'),
     utils.extract_superheat_evap_suction_solenoids(current_data_from_ULC_formatted[3], 'Hot Gas PWM Solenoid Duty')
    
    ]
    table_data = []
    for i,j in zip(properties, values):
        table_data.append([i, j])
    print(tabulate(table_data, headers=head, tablefmt='grid'))

def configure_com_port(com_port):
    serial_obj = serial.Serial(f'com{com_port}')
    serial_obj.baudrate = 9600
    serial_obj.bytesize = 8
    serial_obj.parity = 'N'
    serial_obj.stopbits = 1
    return serial_obj

def output_table(com_port):
    serial_obj = configure_com_port(com_port)
    prev_time = 0
    while(True):
        output_set = get_valid_input(serial_obj)
        output_set_stripped = strip_line(output_set)
        output_set_empty_strings_removed = remove_empty_string(output_set_stripped)
        curr_time = utils.extract_time(output_set_stripped[0])
        #print(curr_time)
        if not(prev_time == 0 or abs(curr_time - prev_time) == 10):
            print('Data is not synchronized with 10-sec intervals\n')
            print('Restart process')
        # output table
        os.system('cls')
        generate_table(output_set_empty_strings_removed)
        prev_time = curr_time
        time.sleep(9.5)


if __name__ == '__main__':
    window = tk.Tk()
    label = tk.Label(text='Enter COM port', fg='white', bg='black', width=50, height=10)
    label.pack(fill=tk.X)


    com_entry = tk.Entry(relief=tk.SUNKEN, borderwidth=5, width=15)
    com_entry.pack(fill=tk.X)
    
    button = tk.Button(
        text='Submit',
        width=10,
        height=2,
        bg='blue',
        fg='white'
    )
    button.pack()
    def get_com_port(event):
        com_port = com_entry.get()
        output_table(com_port)
    button.bind('<Button-1>', get_com_port)
    
    window.mainloop()
