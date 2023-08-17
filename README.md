# Introduction 
All the python source code is converted into executables to run on the host machine. The executable reads serial data incoming from a COM port and outputs a table with refreshed data every 10 seconds.

# Getting Started
1.	Installation process
    - Environments are based on conda
    - To recreate the environment use ```conda create --name <name_of_environment> --file spec-list.txt``` 
2.	Software dependencies
    * Python packages
        - pyserial 3.5
        - tabulate
        - tkinter

# How to use the app
1. The executables for three different boards are in the ```dist``` folder
2. Plug in the ULC board and identify the COM port from which it is receving data
3. Run the appropriate executable and enter the identified COM port 

# Contribute
1. Make the program non-blocking so that the COM port input window is responsive when data from the board is being parsed
2. Close or minimize the COM port input window once an input from the user is submitted