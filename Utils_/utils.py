import time

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
