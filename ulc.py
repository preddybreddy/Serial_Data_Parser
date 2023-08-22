import Utils_.utils as utils
from tabulate import tabulate

# Each module only differs in the generate_table method because of the way the specific circuit board outputs data
# All the base logic is in Utils_/utils
def generate_table(current_data_from_ULC_formatted):
    head = ['Parameter', '\"Raw Data\"/DISPLAY']
    properties = ['Software Version', 'STATE', 'SUPERHEAT', 'EVAP OUT', 'SUCTION PRESSURE', 'LIQUID SOLENOID DUTY', 'HOT GAS DUTY']
    values = [utils.extract_ULC_version(current_data_from_ULC_formatted[0]), utils.extract_state(current_data_from_ULC_formatted[1]), 
     utils.extract_superheat_evap_suction_solenoids(current_data_from_ULC_formatted[3], 'Super Heat'), 
     utils.extract_superheat_evap_suction_solenoids(current_data_from_ULC_formatted[3], 'Evap Out'),
     utils.extract_superheat_evap_suction_solenoids(current_data_from_ULC_formatted[3], 'Suction Pressure'),
     utils.extract_superheat_evap_suction_solenoids(current_data_from_ULC_formatted[3], 'Liquid PWM Solenoid Duty'),
     utils.extract_superheat_evap_suction_solenoids(current_data_from_ULC_formatted[4], 'Hot Gas PWM Solenoid Duty')     
    ]
    table_data = []
    for i,j in zip(properties, values):
        table_data.append([i, j])
    print(tabulate(table_data, headers=head, tablefmt='grid'))

if __name__ == '__main__':   
    com_port_num = input('Enter COM port number: ')
    print('\n')
    print('Please wait...')
    utils.output_table(com_port_num, generate_table)


   