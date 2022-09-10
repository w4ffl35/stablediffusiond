#!/usr/bin/env bash

# Install rabbitmq and pika
read -p "Install rabbitmq and pika? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    sudo apt-get install rabbitmq-server
    sudo systemctl start rabbitmq-server
    sudo systemctl enable rabbitmq-server
    python -m pip install pika --upgrade
fi

# Install stable diffusion
read -p "Do you want to clone stable-diffusion? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    git clone git@github.com:CompVis/stable-diffusion.git

    # Install stable diffusion dependencies
    read -p "Do you want to install stable diffusion dependencies? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        cd stable-diffusion
        conda env create -f environment.yaml
    fi
fi
