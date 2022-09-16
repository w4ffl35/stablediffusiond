#!/usr/bin/env bash


#####################################################
#### Installation script for Debian based systems ###
#####################################################

# check if conda is installed
if ! command -v conda &> /dev/null
then
  echo
  read -p "Install miniconda? (y/n) " -n 1 -r
  echo

  if [[ $REPLY =~ ^[Yy]$ ]]
  then
    # download latest miniconda for linux install script
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

    # verify hash
    sha256sum Miniconda3-latest-Linux-x86_64.sh

    # install miniconda
    bash Miniconda3-latest-Linux-x86_64.sh
  else
    echo "Please install miniconda and run this script again."
    exit 1
  fi
fi

source ~/.bashrc

# initialize shell for conda
conda init bash


##############################
### RabbitMQ installation ####
##############################

# check if rabbitmq is installed
if ! command -v rabbitmq-server &> /dev/null
then
  echo
  read -p "Install rabbitmq-server? (y/n) " -n 1 -r
  echo

  if [[ $REPLY =~ ^[Yy]$ ]]
  then
    echo
    read -p "Install RabbitMQ from apt? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        # install rabbitmq
        sudo apt-get install rabbitmq-server
        # start rabbitmq
        sudo systemctl start rabbitmq-server
        # enable rabbitmq service
        sudo systemctl enable rabbitmq-server
    fi
  else
    echo "Please install rabbitmq-server and run this script again."
    exit 1
  fi
fi


######################################
### stable diffusion installation ####
######################################

echo
read -p "Install stable diffusion? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "Where would you like to clone stable-diffusion?"
    # get input from user
    echo
    read -p "Path: " path_for_clone
    echo

    # add stable-diffusion to path_for_clone
    path_for_clone="$path_for_clone/stable-diffusion"

    if [ -d "$path_for_clone" ]; then
        echo
        echo "Directory already exists"
        echo
        read -p "Would you like to overwrite it? (y/n): " -n 1 -r
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "$path_for_clone"
        fi
    fi

    # clone stable-diffusion
    if ! [ -d "$path_for_clone" ]; then
      git clone --branch feature/add-classes https://github.com/w4ffl35/stable-diffusion.git "$path_for_clone"
    fi

    # change directory to stable-diffusion
    cd "$path_for_clone"

    cd stable_diffusion

    # create virtual environment
    # ask user if they want to user virtual environment
    echo
    read -p "Standard stable-diffusion installation? [y/n]: " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        conda env create -f environment.yaml
        conda activate ldm
    else
        echo "Skipping virtual environment creation..."
    fi
fi


######################################
### stablediffusiond installation ####
######################################

echo
read -p "Install stablediffusiond? (y/n) " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
  # append stablediffusiond to .git/info/exclude if it doesn't already exist
  if ! grep -q "stablediffusiond" .git/info/exclude; then
    echo "stablediffusiond" >> .git/info/exclude
  fi

  echo
    read -p "Path: " path_for_clone
  echo


  # clone stablediffusiond
  git clone https://github.com/w4ffl35/stablediffusiond.git

  # change directory to stablediffusiond
  cd stablediffusiond

  # install stablediffusiond requirements
  pip install -r requirements.txt

  # copy settings.default.py to settings.py
  cp settings.default.py settings.py
fi


############################
### bin directory setup ####
############################

echo
read -p "Setup bin directory? (y/n) " -n 1 -r
echo

# Add bin directory to .bashrc PATH
if [[ $REPLY =~ ^[Yy]$ ]]
then
  sudo ln -s "$PWD/bin/send.sh" "/usr/local/bin/send"
  sudo ln -s "$PWD/bin/client.sh" "/usr/local/bin/stablediffusiond_client"
  sudo ln -s "$PWD/bin/server.sh" "/usr/local/bin/stablediffuiond_server"
fi


######################################
### stablediffusiond daemon setup ####
######################################

echo
read -p "Setup stablediffusiond daemon? (y/n) " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]
then
  # copy etc/stablediffusiond.service to /etc/systemd/system
  sudo cp etc/stablediffusiond.service /etc/systemd/system

  # change [USER_HERE] to current user
  sudo sed -i "s/\[USER_HERE\]/$(whoami)/g" /etc/systemd/system/stablediffusiond.service

  # change PATH_TO_STABLEDIFFUSIOND to current path
  sudo sed -i "s|PATH_TO_STABLEDIFFUSIOND|$PWD|g" /etc/systemd/system/stablediffusiond.service

  # enable stablediffusiond.service
  sudo systemctl enable stablediffusiond.service

  # start stablediffusiond.service
  sudo systemctl start stablediffusiond.service

  # check status of stablediffusiond.service
  sudo systemctl status stablediffusiond.service
fi


###############################################
### stablediffusion_responsed daemon setup ####
###############################################

echo
read -p "Setup stablediffusion_responsed daemon? (y/n) " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]
then
  # copy etc/stablediffusion_responsed.service to /etc/systemd/system
  sudo cp etc/stablediffusion_responsed.service /etc/systemd/system

  # change [USER_HERE] to current user
  sudo sed -i "s/\[USER_HERE\]/$(whoami)/g" /etc/systemd/system/stablediffusion_responsed.service

  # change PATH_TO_STABLEDIFFUSIOND to current path
  sudo sed -i "s|PATH_TO_STABLEDIFFUSIOND|$PWD|g" /etc/systemd/system/stablediffusiond.service

  # enable stablediffusion_responsed.service
  sudo systemctl enable stablediffusion_responsed.service

  # start stablediffusion_responsed.service
  sudo systemctl start stablediffusion_responsed.service

  # check status of stablediffusion_responsed.service
  sudo systemctl status stablediffusion_responsed.service
fi

echo "Installation complete!"