# Github Actions Gui Debug Template
![English Readme](https://img.shields.io/badge/Docs-English-green.svg) ![For_Asdb](https://img.shields.io/badge/For-ASDB-blue.svg)  ![Python](https://img.shields.io/badge/Language-Python-green.svg) [![CI](https://github.com/P-PPPP/ActionsGui/actions/workflows/main.yml/badge.svg)](https://github.com/P-PPPP/ActionsGui/actions/workflows/main.yml)  

### 使用 GithubActions 调试 Windows Gui 应用 *-- 以剪映Srt Parser 为例实现语音转字幕服务*

Github Actions 提供的Windows镜像支持窗口应用。这就为Gui调试提供了必备的基础条件。  
在测试时使用使用了这两个Python 自动化库: `Uiautomation` `pyautogui`。
编写测试脚本时建议使用 `UISpy.exe` 辅助定位元素。  
初始化时Github Actions **不会** 下载空文件夹,若需要临时文件等,请手动创建。

*目前只支持B站视频转换*
#### 使用方法
- Fork 本仓库
- 启用Actions
- 修改Config.json
```json
{
    "ASDB":true,
    "url":["BVXXXXXX","https://a.b.c"]
}
```
- 转换完成后会发布到Release下

#### TODO
- 加入`You-Get` 支持
- 加入Github Secret 支持
- 增加Webhook

#### 许可证及引用

License GPL V3.0

[JianYing Srt Server](https://github.com/A-Soul-Database/JianYingSrtServer)  
[Python-UIAutomation-for-Windows](https://github.com/yinkaisheng/Python-UIAutomation-for-Windows)  
[Pyautogui](https://github.com/asweigart/pyautogui)
[requests](https://github.com/psf/requests)  
[You-Get](https://github.com/soimort/you-get)  
