# zh_recogn中文语音识别

>
> 这是一个中文语音识别为字幕的项目，基于魔塔社区Paraformer模型。
> 支持中文音频、中文视频转为srt字幕。提供 api 接口和简单界面
>
> 该项目仅支持中文语音识别。对于非中文语音，您可以利用基于 OpenAI Whisper 和 Faster-Whisper 的项目，如 [pyvideotrans](https://github.com/jianchang512/pyvideotrans) 或 [stt](https://github.com/jianchang512/stt) 来进行识别，目的是为了弥补国外模型在中文支持方面的不足。
> 


## 源码部署

1. 首先安装 python3.10/安装 [git](https://git-scm.com/downloads) ,安装ffmpeg，windows上 下载ffmpeg.exe后放到本项目的ffmpeg文件夹内，mac使用 `brew install ffmpeg`安装

2. 创建个空英文目录，window上在该目录下打开cmd(Macos和Linux使用终端)，执行命令 `git clone  https://github.com/jianchang512/zh_recogn ./`

3. 继续执行 `python -m venv venv`，然后Windows中执行 `.\venv\scripts\activate`，Macos和Linux中执行 `source ./venv/bin/activate`

4. 继续执行 `pip install -r requirements.txt --no-deps`

5. Windows和Linux如需cuda加速，继续执行， `pip uninstall torch torchaudio`, 再执行`pip install torch  torchaudio --index-url https://download.pytorch.org/whl/cu118`

6. 启动项目 `python start.py`


## 预打包版/仅win10 win11

下载地址 https://github.com/jianchang512/zh_recogn/releases

1. 下载后解压到英文目录，双击 start.exe

2. 为减小打包体积，预打包版不支持CUDA，若需cuda加速，请源码部署



## 在 pyvideotrans项目中使用

首先升级 [pyvideotrans](https://github.com/jianchang512/pyvideotrans)   到v1.62+，然后左上角设置菜单-zh_recogn中文语音识别菜单点开，填写地址和端口，默认 "http://127.0.0.1:9933", 末尾不要加`/api`


## API 

api地址 http://ip:prot/api  默认 `http://127.0.0.1:9933/api`

python代码请求api示例

```
import requests

audio_file="D:/audio/1.wav"
file={"audio":open(audio_file,'rb')}
res=requests.post("http://127.0.0.1:9933/api",files=file,timeout=1800)

print(res.data)

[
	{
	 line:1,
	 time:"00:00:01,100 --> 00:00:03,300",
	 text:"字幕内容1"
	},
	{
	 line:2,
	 time:"00:00:04,100 --> 00:00:06,300",
	 text:"字幕内容2"
	},
]


```

在 pyvideotrans 中填写时不要末尾添加 `/api`


## web界面
![image](https://github.com/jianchang512/zh_recogn/assets/3378335/86305245-c206-4507-afb8-90193dd27bd1)


## 注意事项

1. 第一次使用将自动下载模型，用时会较长
2. 仅支持中文语音识别
3. set.ini文件中可修改绑定地址和端口
