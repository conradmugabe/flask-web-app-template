#! /usr/bin/env python
"""automation scripts"""
import os
import json
import signal
import subprocess

import click

CONFIG_PATH = "config"
APPLICATION_CONFIG = "APPLICATION_CONFIG"


def setenv(variable: str, value: str) -> None:
    """set environment variable"""
    os.environ[variable] = os.getenv(variable, value)


def config_file(config: str) -> str:
    """get config file path"""
    return os.path.join(CONFIG_PATH, f"{config}.json")


def read_config_file(config: str) -> dict:
    """read contents of config file"""
    with open(config_file(config), encoding="utf-8") as file:
        config_data = json.load(file)
    config_data = dict((i["name"], i["value"]) for i in config_data)
    return config_data


def configure_app(config: str) -> None:
    """configure app environment variables"""
    configuration = read_config_file(config)
    for key, value in configuration.items():
        setenv(key, value)


@click.group()
def cli():
    """group all cli commands in 'cli'"""


@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("subcommand", nargs=-1, type=click.Path())
def flask(subcommand):
    """flask cli"""
    os.environ[APPLICATION_CONFIG] = "development"
    configure_app(os.getenv(APPLICATION_CONFIG))

    cmdline = ["flask"] + list(subcommand)

    try:
        process = subprocess.Popen(cmdline)
        process.wait()
    except KeyboardInterrupt:
        process.send_signal(signal.SIGINT)
        process.wait()


cli.add_command(flask)

if __name__ == "__main__":
    cli()
