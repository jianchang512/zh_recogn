import os
import re
import subprocess
import sys
import webbrowser
from datetime import timedelta

import requests
import lib
from lib import cfg

'''
print(ms_to_time_string(ms=12030))
-> 00:00:12,030
'''


def ms_to_time_string(*, ms=0, seconds=None):
    # 计算小时、分钟、秒和毫秒
    if seconds is None:
        td = timedelta(milliseconds=ms)
    else:
        td = timedelta(seconds=seconds)
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = td.microseconds // 1000

    time_string = f"{hours}:{minutes}:{seconds},{milliseconds}"
    return format_time(time_string, ',')


# 从字幕文件获取格式化后的字幕信息
'''
[
{'line': 13, 'time': '00:01:56,423 --> 00:02:06,423', 'text': '因此，如果您准备好停止沉迷于不太理想的解决方案并开始构建下一个
出色的语音产品，我们已准备好帮助您实现这一目标。深度图。没有妥协。唯一的机会..', 'startraw': '00:01:56,423', 'endraw': '00:02:06,423', 'start_time'
: 116423, 'end_time': 126423}, 
{'line': 14, 'time': '00:02:06,423 --> 00:02:07,429', 'text': '机会..', 'startraw': '00:02:06,423', 'endraw': '00:02
:07,429', 'start_time': 126423, 'end_time': 127429}
]
'''


# 将字符串或者字幕文件内容，格式化为有效字幕数组对象
# 格式化为有效的srt格式
# content是每行内容，按\n分割的，
def format_srt(content):
    # 去掉空行
    content = [it for it in content if it.strip()]
    if len(content) < 1:
        return []
    result = []
    maxindex = len(content) - 1
    # 时间格式
    timepat = r'^\s*?\d+:\d+:\d+([\,\.]\d*?)?\s*?-->\s*?\d+:\d+:\d+([\,\.]\d*?)?\s*?$'
    textpat = r'^[,./?`!@#$%^&*()_+=\\|\[\]{}~\s \n-]*$'
    for i, it in enumerate(content):
        # 当前空行跳过
        if not it.strip():
            continue
        it = it.strip()
        is_time = re.match(timepat, it)
        if is_time:
            # 当前行是时间格式，则添加
            result.append({"time": it, "text": []})
        elif i == 0:
            # 当前是第一行，并且不是时间格式，跳过
            continue
        elif re.match(r'^\s*?\d+\s*?$', it) and i < maxindex and re.match(timepat, content[i + 1]):
            # 当前不是时间格式，不是第一行，并且都是数字，并且下一行是时间格式，则当前是行号，跳过
            continue
        elif len(result) > 0 and not re.match(textpat, it):
            # 当前不是时间格式，不是第一行，（不是行号），并且result中存在数据，则是内容，可加入最后一个数据

            result[-1]['text'].append(it.capitalize())

    # 再次遍历，去掉text为空的
    result = [it for it in result if len(it['text']) > 0]

    if len(result) > 0:
        for i, it in enumerate(result):
            result[i]['line'] = i + 1
            result[i]['text'] = "\n".join([tx.capitalize() for tx in it['text']])
            s, e = (it['time'].replace('.', ',')).split('-->')
            s = format_time(s, ',')
            e = format_time(e, ',')
            result[i]['time'] = f'{s} --> {e}'
    return result


def get_subtitle_from_srt(srtfile, *, is_file=True):
    if is_file:
        if os.path.getsize(srtfile) == 0:
            raise Exception('字幕格式出错')
        try:
            with open(srtfile, 'r', encoding='utf-8') as f:
                content = f.read().strip().splitlines()
        except:
            try:
                with open(srtfile, 'r', encoding='gbk') as f:
                    content = f.read().strip().splitlines()
            except Exception as e:
                raise Exception(f'get srtfile error:{str(e)}')
    else:
        content = srtfile.strip().splitlines()
    if len(content) < 1:
        raise Exception("srt content is 0")

    result = format_srt(content)
    if len(result) < 1:
        return []

    new_result = []
    line = 1
    for it in result:
        if "text" in it and len(it['text'].strip()) > 0:
            it['line'] = line
            startraw, endraw = it['time'].strip().split("-->")

            startraw = format_time(startraw.strip().replace(',', '.').replace('，', '.').replace('：', ':'), '.')
            start = startraw.split(":")

            endraw = format_time(endraw.strip().replace(',', '.').replace('，', '.').replace('：', ':'), '.')
            end = endraw.split(":")

            start_time = int(int(start[0]) * 3600000 + int(start[1]) * 60000 + float(start[2]) * 1000)
            end_time = int(int(end[0]) * 3600000 + int(end[1]) * 60000 + float(end[2]) * 1000)
            it['startraw'] = startraw
            it['endraw'] = endraw
            it['start_time'] = start_time
            it['end_time'] = end_time
            new_result.append(it)
            line += 1

    return new_result


# 将 时:分:秒,|.毫秒格式为  aa:bb:cc,|.ddd形式
def format_time(s_time="", separate=','):
    if not s_time.strip():
        return f'00:00:00{separate}000'
    s_time = s_time.strip()
    hou, min, sec = "00", "00", f"00{separate}000"
    tmp = s_time.split(':')
    if len(tmp) >= 3:
        hou = tmp[-3].strip()
        min = tmp[-2].strip()
        sec = tmp[-1].strip()
    elif len(tmp) == 2:
        min = tmp[0].strip()
        sec = tmp[1].strip()
    elif len(tmp) == 1:
        sec = tmp[0].strip()

    if re.search(r',|\.', str(sec)):
        sec, ms = re.split(r',|\.', str(sec))
        sec = sec.strip()
        ms = ms.strip()
    else:
        ms = '000'
    hou = hou if hou != "" else "00"
    if len(hou) < 2:
        hou = f'0{hou}'
    hou = hou[-2:]

    min = min if min != "" else "00"
    if len(min) < 2:
        min = f'0{min}'
    min = min[-2:]

    sec = sec if sec != "" else "00"
    if len(sec) < 2:
        sec = f'0{sec}'
    sec = sec[-2:]

    ms_len = len(ms)
    if ms_len < 3:
        for i in range(3 - ms_len):
            ms = f'0{ms}'
    ms = ms[-3:]
    return f"{hou}:{min}:{sec}{separate}{ms}"


def runffmpeg(arg):
    cmd = ["ffmpeg", "-hide_banner", "-y"]
    # if cfg.devtype =='cuda':
    #     cmd.extend(["-hwaccel", "cuda","-hwaccel_output_format","cuda"])
    cmd = cmd + arg
    p = subprocess.run(cmd,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE,
                       creationflags=0 if sys.platform != 'win32' else subprocess.CREATE_NO_WINDOW)
    try:
        # 成功
        if p.returncode == 0:
            return "ok"
        errs = str(p.stderr)
        if errs:
            errs = errs.replace('\\\\', '\\').replace('\r', ' ').replace('\n', ' ')
            errs = errs[errs.find("Error"):]
        return errs
    except subprocess.TimeoutExpired as e:
        # 如果前台要求停止
        pass
    except Exception as e:
        # 出错异常
        errs = f"[error]ffmpeg:error {cmd=},\n{str(e)}"
        return errs


def checkupdate():
    try:
        res = requests.get("https://raw.githubusercontent.com/jianchang512/sts/main/version.json")
        print(f"{res.status_code=}")
        if res.status_code == 200:
            d = res.json()
            print(f"{d=}")
            if d['version_num'] > lib.VERSION:
                cfg.updatetips = f'New version {d["version"]}'
    except Exception as e:
        pass


def openweb(web_address):
    webbrowser.open("http://" + web_address)
