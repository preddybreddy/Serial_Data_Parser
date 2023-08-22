# str_input_0 = 'Total Run Time hrs:mins:secs 1:43:00    Scab_LS_0_08'
def extract_SCAB_version(str_input_0):
    start_index = str_input_0.index('Scab')
    return str_input_0[start_index:]