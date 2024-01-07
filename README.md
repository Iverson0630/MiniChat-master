# MiniChat

A WeChat-style chat robot, built by pyqt5

This project uses Google Gemini as chat model and design a WeChat-style GUI.

## 1. Quick Start

### 1. 1  Requirements

- Python >3.9

- google-generativeai

- pyqt5 == 5.15.2

To install google-generativeai,run:

```shell
pip install -q -U google-generativeai
```

For more details and Gemini API, visit [here](https://ai.google.dev/tutorials/python_quickstart).

Besides, you also need to apply for a Gemini API_Key [here](https://ai.google.dev/)

### 1.2 Start Chatting!!!

To open the GUI, run python script:

```shell
python MiniChat.py
```

Or you can [download]() our released .exe file. Be careful to keep the **src** folder and **.exe** files in one folder

"用户名" or ''Admin" is customized and the "密码" or "password" is your API_KEY.

**Remember to enable VPN and switch the region to a supported country otherwise the login screen will be stuck!!!**

### 1.3 Modified and rebuilt

After you modified the python code and want to rebuild an .exe file, just run:

```shell
pyinstaller -w -i path_to_icon.ico MiniChat.py 
```

<<<<<<< HEAD
## 2. Future improvements

- Adaptive window size
- Chat with multiple objects at the same time, now only one
- Support image input 



=======

## 2. Future improvements

- Adaptive window size
- Chat with multiple objects at the same time, now only one
- Support image input 


>>>>>>> 418a3b8afd947d90e31916c94adaac0a055e967d
