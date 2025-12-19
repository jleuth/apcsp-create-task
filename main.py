import click
import json
import os
import subprocess
from pathlib import Path

STORAGE_FILE = Path.home() / '.cmdmgr_commands.json'

@click.group()
def cli():
    pass

@cli.command()
@click.argument('nickname', required=True)
@click.argument('command', required=True)
def store(nickname, command):
    click.echo(f"Stored command '{nickname}': {command}") 

@cli.command()
@click.argument('nickname', required=True)
def run(nickname):
    click.echo(f"Running command '{nickname}'")

if __name__ == '__main__':
    cli()
