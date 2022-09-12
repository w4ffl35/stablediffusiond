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

