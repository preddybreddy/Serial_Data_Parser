import Utils_.utils as utils
import Utils_.utils_selay_ls as utils_selay_ls
import Utils_.utils_selay_hs as utils_selay_hs
from tabulate import tabulate


def generate_table(current_data_from_ULC_formatted):
    head = ['Parameter', '\"Raw Data\"/DISPLAY']
    properties = ['Software Version', 'STATE', 'SUPERHEAT',  'SUCTION PRESSURE', 'LIQUID SOLENOID DUTY', 'SH ERROR']
    values = [utils_selay_ls.extract_SCAB_version(current_data_from_ULC_formatted[0]), utils.extract_state(current_data_from_ULC_formatted[0]), 
     utils.extract_superheat_evap_suction_solenoids(current_data_from_ULC_formatted[3], 'Super Heat'), 
     utils.extract_superheat_evap_suction_solenoids(current_data_from_ULC_formatted[3], 'Suction Pressure'),
     utils_selay_hs.extract_liquid_solenoid_duty(current_data_from_ULC_formatted[3]),
     utils.extract_superheat_evap_suction_solenoids(current_data_from_ULC_formatted[3], 'SH Target')
    ]
    table_data = []
    for i,j in zip(properties, values):
        table_data.append([i, j])
    print(tabulate(table_data, headers=head, tablefmt='grid'))

#def get_valid_input(lines):
#    # Also temporary logic --delete after
#    lines_from_ULC = []
#    i = 0
#    first_line = lines[i]
#    while 'Total Run Time' not in first_line:
#        i += 1
#        first_line = lines[i]
#
#    lines_from_ULC.append(first_line) 
#    i = i + 1   
#    first_line = lines[i]
#    while ('*' not in first_line):
#        lines_from_ULC.append(first_line)
#        i = i + 1
#        first_line = lines[i]
#    return lines_from_ULC


if __name__ == '__main__':   
    com_port_num = input('Enter COM port number: ')
    print('\n')
    print('Please wait...')
    utils.output_table(com_port_num, generate_table)