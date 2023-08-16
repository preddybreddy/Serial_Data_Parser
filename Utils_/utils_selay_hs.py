def extract_liquid_solenoid_duty(str_3):
    return str_3[str_3.index('Liquid PWM Solenoid Duty') + len('Liquid PWM Solenoid Duty') + 1:]

#s = 'Super Heat  4.3, Suction Temp 19.0, Suction Pressure 107.6, Suction Pressure Limit in REFRIG 50.0, SH Error -5.5, SH Target 12.0, Liquid PWM Solenoid Duty 10.0'
#print(extract_liquid_solenoid_duty(s))
