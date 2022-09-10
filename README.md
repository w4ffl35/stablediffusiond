# stablediffusiond

A daemen which watches a queue and runs [Stable Diffusion](https://github.com/CompVis/stable-diffusion).

`stablediffusiond` is a process that watches a RabbitMQ queue for messages in the format of JSON strings.

The current use-case is to allow local applications easier access to stable diffusion. 

`stablediffusiond` keeps the process in memory so that your application doesn't have to wait for the model 
to initialize each time, resulting in faster responses.

Currently `stablediffusiond` depends on a branch which contains classes that mirror the code found in the 
`txt2img` and `img2img` Stable Diffusion scripts. The classes allow us to skip model initialization for each request.

[The three classes can be viewed here](https://github.com/w4ffl35/stable-diffusion/tree/feature/add-classes/classes) (compare to `scripts/txt2img` and `scripts/img2img`):

## Installation

`stablediffusiond` is in the early stages of development, so installation is more manual than it should be.

### Install RabbitMQ

Follow the instructions at [RabbitMQ](https://www.rabbitmq.com/download.html) to install RabbitMQ for your platform

![img.png](img.png)

The following instructions assume that you are on Linux and may need to be adapted for your platform

1. `git clone --branch feature/add-classes https://github.com/w4ffl35/stable-diffusion.git`
2. `cd stable-diffusion`
3. `git clone https://github.com/w4ffl35/stablediffusiond.git`
4. Follow Stable Diffusion installation instructions [found in README](https://github.com/w4ffl35/stable-diffusion).
5. ensure you have enabled the conda environment created in step 4, then install pika `pip install pika --upgrade`
6. `cd stablediffusiond`
7. `cp settings.default.py settings.py`, make any changes to the settings file that you wish

## Usage

Run the listener

1. `cd stablediffusiond`
2. `python recieve.py`

Make a request

1. `cd stablediffusiond`
2. `python send.py '{"prompt":"cat"}'`


## Limitations

- Installation is too manual
- Very basic RabbitMQ configuration
- Not production ready
