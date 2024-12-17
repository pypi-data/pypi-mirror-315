import argparse
from pathlib import Path
from . import subrip

def parse_args():
    parser = argparse.ArgumentParser(description='Sync SubRip subtitle with audio')
    parser.add_argument('filename', help='SubRip subtitle file (.srt). UFT-8 encoding')
    parser.add_argument('lag', type=int, help='lag in milliseconds. eg: 220, -150, +350')
    parser.add_argument('--backup', help='create a backup file (.bak), default', action=argparse.BooleanOptionalAction, default=True)
    return parser.parse_args()

def main():
    args = parse_args()
    with open(args.filename) as f:
        document = subrip.process_document(f, args.lag)
    if args.backup:
        p = Path(args.filename)
        p.rename(f'{args.filename}.bak')
    with open(args.filename, 'w') as f:
        f.write(document)

if __name__ == "__main__":
    main()
