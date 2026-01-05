import argparse
import json
import os
import subprocess
from pathlib import Path

STORAGE_FILE = Path.home() / '.cmdmgr_commands.jsonl'


def load():
    if not STORAGE_FILE.exists():
        return []
    with open(STORAGE_FILE, "r") as file:
        return [json.loads(line) for line in file]

loaded = load()

def write(nickname, command):
    entry = {'nickname': nickname, 'command': command}
    with open(STORAGE_FILE, 'a') as f:
        json.dump(entry, f)
        f.write('\n')
    loaded.append(entry)

def run(nickname, edit):
    for entry in loaded:
        if entry.get("nickname") == nickname:
            cmd = entry.get("command")

            if edit:
                print(f"Command: {cmd}")
                cmd = input("Edit (or press Enter to use as-is): ") or cmd

            ret = subprocess.run(cmd, shell=True, capture_output=True)
            print(ret.stdout.decode())
            print(ret.stderr.decode())
            return

    print(f"Nickname '{nickname}' not found.")

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    store_p = subparsers.add_parser("store")
    store_p.add_argument("nickname")
    store_p.add_argument("cmd")

    run_p = subparsers.add_parser("run")
    run_p.add_argument("nickname")
    run_p.add_argument("--edit", "-e", action="store_true")

    args = parser.parse_args()
    if args.command == "store":
        write(args.nickname, args.cmd) 
    elif args.command == "run":
        run(args.nickname, args.edit) 

if __name__ == '__main__':
    main()
