import Utils_.utils as utils
import Utils_.utils_selay_ls as utils_selay_ls
from tabulate import tabulate
import tkinter as tk



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
        utils.output_table(com_port, generate_table)
    button.bind('<Button-1>', get_com_port)
    
    window.mainloop()
