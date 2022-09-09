git clone https://github.com/beastmodeswag/FYP-IDS.git
cd FYP-IDS

# Create a virtual environment(To ensure the dependencies do not affect other python programs)
python3.9 -m venv venv

# Activate that virtual environment
source venv/bin/activate #If there are errors check the directory(e.g 'source /bin/activate' instead)

# Install the project requirements.
pip install -r requirements.txt

# To run the program
sudo python main.py

# An ip address should show up on the terminal(e.g http://127.0.0.1:5050)


# Remember to change the host address in the config.txt file to your ip address


*Note: May not work on windows systems as the packet sniffer is set to sniff packets for unix-based systems
