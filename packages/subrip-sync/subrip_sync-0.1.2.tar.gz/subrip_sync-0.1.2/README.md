# Sync SubRip subtitle with audio
```
> subrip-sync -h
usage: subrip-sync [-h] [--backup | --no-backup] filename lag

Sync SubRip subtitle with audio

positional arguments:
  filename              SubRip subtitle file (.srt). UFT-8 encoding
  lag                   lag in milliseconds. eg: 220, -150, +350

options:
  -h, --help            show this help message and exit
  --backup, --no-backup
                        create a backup file (.bak), default
```

## run test using uv
```
uv run python -m unittest discover -s src
```

## run program using uv
```
uv run subrip-sync -h
```

## build program using uv
```
> uv build
Building source distribution...
Building wheel from source distribution...
Successfully built dist\subrip_sync-0.1.0.tar.gz
Successfully built dist\subrip_sync-0.1.0-py3-none-any.whl
```

see https://docs.astral.sh/uv/