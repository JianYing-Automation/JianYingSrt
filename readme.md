# JianYingActionsSrt
![English Readme](https://img.shields.io/badge/Docs-English-green.svg) ![For_Asdb](https://img.shields.io/badge/For-ASDB-blue.svg)  ![Python](https://img.shields.io/badge/Language-Python-green.svg) [![CI](https://github.com/P-PPPP/ActionsGui/actions/workflows/main.yml/badge.svg)](https://github.com/P-PPPP/ActionsGui/actions/workflows/main.yml)  

### 使用Github Actions 使用剪映转换字幕文件

#### 使用方法
- Fork 本仓库
- 启用Actions
- 修改Config.json
```json
{
    "types":"",    *"requests","you-get","bili"*
    "ASDB":true,
    "url":["BVXXXXXX","https://a.b.c"]
}
```
- 转换完成后会发布到Release下

#### TODO
- 加入Github Secret 支持
- 增加Webhook

#### 许可证及引用

License GPL V3.0

[JianYing Srt Server](https://github.com/A-Soul-Database/JianYingSrtServer)  
[Python-UIAutomation-for-Windows](https://github.com/yinkaisheng/Python-UIAutomation-for-Windows)  
[Pyautogui](https://github.com/asweigart/pyautogui)
[requests](https://github.com/psf/requests)  
[You-Get](https://github.com/soimort/you-get)  
