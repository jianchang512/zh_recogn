import os
import sys

ROOT_DIR = os.getcwd().replace('\\', '/')


def parse_ini():
    sets = {
        "web_address": "127.0.0.1:9922"
    }
    with open(ROOT_DIR + "/set.ini", 'r', encoding='utf-8') as f:
        for line in f.readlines():
            t = line.strip()
            if t  and not t.startswith(';') and t.find('=') > 0:
                t = t.split('=', maxsplit=1)
                sets[t[0]] = t[1]

    return sets


sets = parse_ini()
web_address = sets.get('web_address')

STATIC_DIR = os.path.join(ROOT_DIR, 'static').replace('\\', '/')
TMP_DIR = os.path.join(STATIC_DIR, 'tmp').replace('\\', '/')

if not os.path.exists(TMP_DIR):
    os.makedirs(TMP_DIR, 0o777, exist_ok=True)
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR, 0o777, exist_ok=True)

if sys.platform == 'win32':
    os.environ['PATH'] = f'{ROOT_DIR};{ROOT_DIR}\\ffmpeg;' + os.environ['PATH']
else:
    os.environ['PATH'] = f'{ROOT_DIR}:{ROOT_DIR}/ffmpeg:' + os.environ['PATH']

updatetips = ""
