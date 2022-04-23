# JianYingActionsSrt
![For_Asdb](https://img.shields.io/badge/For-ASDB-blue.svg)  ![Python](https://img.shields.io/badge/Language-Python-green.svg) [![CI](https://github.com/P-PPPP/ActionsGui/actions/workflows/main.yml/badge.svg)](https://github.com/P-PPPP/ActionsGui/actions/workflows/main.yml)  

### 使用Github Actions 使用剪映**自动**转换字幕文件
![202201300956_1_.gif](https://s2.loli.net/2022/03/24/G92tQ6RfJdYivPK.gif)  
#### 使用方法
- Fork 本仓库
- 启用Actions
- 修改Config.json
```json
{
    "Jy_Download_Url":"https://xxx/Jianying_pro.exe", //剪映的下载链接,不用动
    "ASDB":true,  //若为True,则对于分P中含有“弹幕”的文件将不会识别
    "url":["BV1D3411W7K6"], // 支持BV号和直链
    "Sources_Path":"./components/tmp/", // 本地运行时可以修改媒体目标文件夹
    "webhooks":[] // 支持注册 webhooks 用于工作流
}
```

##### 本地调用
文件提供了四种方式
```
    Args    Description
    local(Default)   本地调用(把自己的视频/媒体放到Config.json指定的目录下进行转换)
    nonactions  不安装剪映,其他和GitHub actions 一样
    install     仅安装剪映(测试)
    actions     用于GitHub actions 安装剪映并按照Config.json中的媒体链接转换文件
```

- Github actions 转换完成后会发布到Release下

#### Bug排查
对于自动化测试而言,对于Bug的排查会有些复杂,在Release中会发布截图,可以根据这些信息排查Bug

#### TODO
- [x] 增加Webhook

#### 许可证及引用

License GPL V3.0

[JianYing Srt Server](https://github.com/A-Soul-Database/JianYingSrtServer)  
[Python-UIAutomation-for-Windows](https://github.com/yinkaisheng/Python-UIAutomation-for-Windows)  
[Pyautogui](https://github.com/asweigart/pyautogui)
[requests](https://github.com/psf/requests)  
[You-Get](https://github.com/soimort/you-get)  
