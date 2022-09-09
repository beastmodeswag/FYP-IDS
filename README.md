# FYP-IDS Instructions to run
1) git clone https://github.com/beastmodeswag/FYP-IDS.git
2) cd FYP-IDS

# Create a virtual environment
3) python3.10 -m venv venv # or whichever version of python you are running(i.e 'python3.9 -m venv venv' etc.)

# Activate that virtual environment
4) source venv/bin/activate # if you are getting errors try 'source /bin/activate' or check your present working directory

# Install the project requirements.
5) pip install -r requirements.txt 

# To run the program(require sudo)
6) sudo python main.py

# A URL should appear on the terminal (e.g http://127.0.1.1:5050) to view the dashboard


*Remember to change the host ip address in the config.txt file to your ip address*

*Note : This program may not work on windows as the packet sniffer is set to sniff packets for linux only*
