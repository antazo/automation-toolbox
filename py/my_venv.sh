# Virtual environment: "my_venv"

# Libraries needed
sudo apt-get install -y python3-pip python3-venv

# We invoke the venv module and create my_venv
python3 -m venv my_venv

# Activate
source venv/bin/activate

# Under the virtual environment, we install Nornir.
# Nornir let's us install other Python libraries
# such as Netmiko, Npalm, Scrapy
pip install nornir_utils nornir_netmiko

# Check all libraries installed in our environment
# and store it to later use in our Dockerfile
pip freeze >> requirement.txt

