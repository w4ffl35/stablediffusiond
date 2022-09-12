"""
stablediffusiond setup script
"""
from setuptools import setup

setup(
    name="stablediffusiond",
    version="0.4.1",
    description="A daemon that watches a queue, runs stable diffusion and enqueues the results.",
    url="https://github.com/w4ffl35/stablediffusiond.git",
    author="w4ffl35 (Joe Curlee)",
    author_email="25737761+w4ffl35@users.noreply.github.com",
    license="BSD-3-Clause",
    packages=["stablediffusiond"],
    install_requires=[
        "pika"
    ]
)
