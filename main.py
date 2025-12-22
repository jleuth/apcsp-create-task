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
@click.option('--edit', '-e', is_flag=True, help="Edit the command before executing it. Enters a Vim UI to edit your command.")
def run(nickname, edit):
    with open(STORAGE_FILE, "r") as fr:
        for line in fr:
            entry = json.loads(line)
            if entry.get("nickname") == nickname:
                found = True
                cmd = entry.get("command")
                if edit:
                    edited = click.edit(cmd)
                    if edited is None:
                        click.echo("Edit cancelled.")
                        return
                    cmd = edited.strip()

                click.echo(f"Running command '{nickname}'")
                ret = subprocess.run(cmd, shell=True, capture_output=True)
                click.echo(ret.stdout)
                break
    if not found:
        click.echo(f"Nickname '{nickname}' not found.")
        return
    

if __name__ == '__main__':
    cli()

#todo: add deleting and probably permanently modifying
#todo: maybe make compatible with repls?
#todo: idk other qol features i can think of
#todo: put the commands gotten from the file into a list of dicts so we dont need to keep rereading the file.