# stablediffusiond

A daemon which watches for messages on RabbitMQ and runs [Stable Diffusion](https://github.com/CompVis/stable-diffusion)

- **No hot loading** - Model stored in RAM (4GB~) for faster processing
- **Daemon** - existing solutions use a webserver, here we use a daemon which is more lightweight
- **Less bloat** - code and dependencies have been kept to a minimum
- **Flexability** - request daemon, response daemon and queue system can be run independently, allowing for more efficient use of resources
- **Easy to use** - just run the daemon and send messages to the queue using `send.py`

## Flow chart

1. `stablediffusiond` listens to _request queue_
2. client makes a request which is added to _request queue_
3. `stablediffusiond` gets top item from _request queue_ and runs Stable Diffusion based on request
4. `stablediffusiond` places response from Stable Diffusion into _response queue_
5. `stablediffusion_responsed` service listens to _response queue_ and opens a socket on `localhost:50007`
6. `stablediffusion_responsed` gets top item from _response queue_ and returns it to client connected on `localhost:50007`

![img.png](src/stablediffusiond_flowchart.png)

---

## Installation

### Install RabbitMQ

Follow the instructions at [RabbitMQ](https://www.rabbitmq.com/download.html) to install RabbitMQ for your platform

![img.png](img.png)

### Install Stable Diffusion and stablediffusiond

The following instructions assume that you are on Linux and may need to be adapted for your platform

1. `git clone --branch feature/add-classes https://github.com/w4ffl35/stable-diffusion.git`
2. `cd stable-diffusion`
3. Edit the `.git/info/exclude` file and add the following line to the end of the file: `stablediffusiond`
4. `git clone https://github.com/w4ffl35/stablediffusiond.git`
5. Follow Stable Diffusion installation instructions [found in README](https://github.com/w4ffl35/stable-diffusion).
6. ensure you have enabled the conda environment created in step 4, then install pika `pip install pika --upgrade`
7. `cd stablediffusiond`
8. `cp settings.default.py settings.py`, make any changes to the settings file that you wish

### Setup bin files

1. `cd /usr/local/bin`
2. `sudo ln -s /path/to/stablediffusiond/bin/server.sh stablediffusion_server`
3. `sudo ln -s /path/to/stablediffusiond/bin/client.sh stablediffusion_client`
4. `sudo ln -s /path/to/stablediffusiond/bin/response.sh stablediffusion_response_query`

### Install stablediffusiond as a service

1. `sudo cp stablediffusiond.service /etc/systemd/system/`
2. `sudo cp stablediffusion_responsed.service /etc/systemd/system/`
3. Edit stablediffusiond.service
4. `sudo vim /etc/systemd/system/stablediffusiond.service`
5. change the `User=[USER_HERE]` line to point to the correct user (`User=bob`, for example)
6. save the file
7. `sudo vim /etc/systemd/system/stablediffusion_responsed.service`
8. change the `User=[USER_HERE]` line to point to the correct user as you did in line 14
9. save the file
10. `sudo systemctl daemon-reload`
11. `sudo systemctl start stablediffusiond.service`
12. `sudo systemctl start stablediffusion_responsed.service`

Your directory structure should look like this:

```
> stable-diffusion
  > [various folders such as `assets`, `classes` and `scripts`]
  > stablediffusiond
    > [various files such as `recieve.py` and `send.py`]
```

---

## Forked Stable Diffusion

Currently `stablediffusiond` depends on a forked branch which contains classes that mirror the code found in the 
`txt2img` and `img2img` Stable Diffusion scripts. The classes allow us to skip model initialization for each request.

[The three classes can be viewed here](https://github.com/w4ffl35/stable-diffusion/tree/feature/add-classes/classes) (compare to `scripts/txt2img` and `scripts/img2img`):

---

## Commands

### stablediffusiond service

Starts a Stable Diffusion request queue runner
 
- start `sudo systemctl start stablediffusiond.service`
- restart `sudo systemctl restart stablediffusiond.service`
- stop `sudo systemctl stop stablediffusiond.service`


### stablediffusion_responsed service

Starts a Stable Diffusion response queue runner
 
- start `sudo systemctl start stablediffusion_responsed.service`
- restart `sudo systemctl restart stablediffusion_responsed.service`
- stop `sudo systemctl stop stablediffusion_responsed.service`

### bin commands

- start stable diffusion queue runner (daemon uses this) `stablediffusion_client`
- start the sable diffusion response runner (response damen uses this) `stablediffusion_response_query`
- send a message to running stable diffusion queue `stablediffusion_client '{"prompt": "cat", "seed": 42}'`

---

## Limitations

- Installation is too manual
- Very basic RabbitMQ configuration
- Not production ready
