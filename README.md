# zh_recogn中文语音识别

> 这是一个中文语音识别为字幕的项目，基于魔塔社区Paraformer模型。
> 支持中文音频、中文视频转为srt字幕。
>
> 该项目仅支持中文语音识别。对于非中文语音，您可以利用基于 OpenAI Whisper 和 Faster-Whisper 的项目，如 [pyvideotrans](https://github.com/jianchang512/pyvideotrans) 或 [stt](https://github.com/jianchang512/stt) 来进行识别，目的是为了弥补国外模型在中文支持方面的不足。


## 源码部署

1. 首先安装 python3.10/安装 [git](https://git-scm.com/downloads) ,安装ffmpeg，windows上 下载ffmpeg.exe后放到本项目的ffmpeg文件夹内，mac使用 `brew install ffmpeg`安装
2. 创建个空英文目录，该目录下打开cmd，执行 `git clone  https://github.com/jianchang512/zh_recogn ./`
3. cmd执行 `python -m venv venv`，然后windows中执行 `.\venv\scripts\activate`，macos和Linux中执行 `source ./venv/bin/activate`
4. 继续执行 `pip install -r requirements.txt --no-deps`
5. 如需cuda执行，在配置好cuda环境后， `pip uninstall torch torchaudio`, windows和linux下执行`pip install torch  torchaudio --index-url https://download.pytorch.org/whl/cu118`
6. 启动项目 `python start.py`


## 预打包版/仅win10 win11

下载后解压到英文目录，双击 start.exe


## 注意事项

1. 第一次使用将自动下载模型，用时会较长
2. 仅支持中文语音识别
3. set.ini文件中可修改绑定地址和端口

## 在 pyvideotrans项目中使用

首先升级 pyvideotrans 到v1.62+，然后左上角设置菜单-zh_recogn中文语音识别菜单点开，填写地址和端口，默认 "http://127.0.0.1:9933", 默认不要加`/api`


## API 

api地址 http://ip:prot/api,默认 `http://127.0.0.1:9933/api`

python代码示例

```
audio_file="D:/audio/1.wav"
file={"audio":open(audio_file,'rb')}
res=requests.post("http://127.0.0.1:9933/api",files=file,timeout=1800)

print(res.data)

```

在 pyvideotrans 中填写时不要末尾添加 `/api`