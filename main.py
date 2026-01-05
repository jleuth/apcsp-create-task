import argparse
import json
import os
import subprocess
from pathlib import Path

STORAGE_FILE = Path.home() / '.cmdmgr_commands.jsonl' # ~/.cmdmgr_commands.jsonl


def load():
    if not STORAGE_FILE.exists():
        return []
    with open(STORAGE_FILE, "r") as file: #load the file into memory to prevent constantly reaccessing it
        return [json.loads(line) for line in file]

loaded = load()

def write(nickname, command):
    entry = {'nickname': nickname, 'command': command} #defines dict structure
    with open(STORAGE_FILE, 'a') as f: 
        json.dump(entry, f)
        f.write('\n')
    loaded.append(entry)

def run(nickname, edit):
    for entry in loaded:
        if entry.get("nickname") == nickname: #iterate through each entry till we hit whatever the nicknamed cmd is
            cmd = entry.get("command")

            if edit:
                print(f"Command: {cmd}")
                cmd = input("Edit (or press Enter to use as-is): ") or cmd

            ret = subprocess.run(cmd, shell=True, capture_output=True) #shell tells it that this is an interactive shell (for sudo) and capture_output says to feed the output back into the program
            print(ret.stdout.decode()) #We have to decode because stdout and stderr are returned as bytes
            print(ret.stderr.decode())
            return

    print(f"Nickname '{nickname}' not found.")

def main():
    # Set up the top-level argument parser and initialize subcommands parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    store_p = subparsers.add_parser("store") #Parser = command basically
    store_p.add_argument("nickname")
    store_p.add_argument("cmd")

    run_p = subparsers.add_parser("run")
    run_p.add_argument("nickname") #This is counted as a positional arg
    run_p.add_argument("--edit", "-e", action="store_true")#This is a flag

    args = parser.parse_args() #this tells the program what action to take
    if args.command == "store":
        write(args.nickname, args.cmd) 
    elif args.command == "run":
        run(args.nickname, args.edit) 

if __name__ == '__main__':
    main()

#Some parts of programming, such as debugging and explanation, were assisted by Claude