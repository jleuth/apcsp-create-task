import click
import json
import os
import subprocess
from pathlib import Path

STORAGE_FILE = Path.home() / '.cmdmgr_commands.jsonl'

@click.group()
def cli():
    pass

@cli.command()
@click.argument('nickname', required=True)
@click.argument('command', required=True)
def store(nickname, command):
    with open(STORAGE_FILE, 'a') as f:
        json.dump({'nickname': nickname, 'command': command}, f)
        f.write('\n')
    f.close()

    click.echo(f"Stored command '{nickname}': {command}") 

@cli.command()
@click.argument('nickname', required=True)
@click.option('--print', '-p', is_flag=True, help="Print the command instead of executing it, nice if you need to edit it without storing a new command.")
def run(nickname):
    with open(STORAGE_FILE, "r") as fr:
        for line in fr:
            entry = json.loads(line)
            if entry.get("nickname") == nickname:
                found = True
                cmd = entry.get("command")
                click.echo(f"Running command '{nickname}'")
                ret = subprocess.run(cmd, shell=True, capture_output=True)
                click.echo(ret.stdout)
                break
    if not found:
        click.echo(f"Nickname '{nickname}' not found.")
        return
    

if __name__ == '__main__':
    cli()
