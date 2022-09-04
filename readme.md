# JianYingActionsSrt
![Powered_By](https://img.shields.io/badge/JianYingApi-blue.svg)  ![Python](https://img.shields.io/badge/Language-Python-green.svg) [![CI](https://github.com/P-PPPP/ActionsGui/actions/workflows/main.yml/badge.svg)](https://github.com/P-PPPP/ActionsGui/actions/workflows/main.yml) 

## 使用Github Actions 使用剪映自动转换字幕文件  

![202201300956_1_.gif](https://s2.loli.net/2022/03/24/G92tQ6RfJdYivPK.gif)  

### 使用方法
#### Github Actions
- Fork 本仓库
- 启用Actions
- 修改`Config.json`

#### 本地调用或服务器部署
- 克隆/下载 本仓库
- 通过 `pip install -r requirements.txt` 安装依赖
- 执行 `python3 main.json --local D://Moives/Pulp_Fiction.mkv` 或者 `python3 main.json --bilibili BV1C64y1m7on`

#### 通过 `Config.json` 调用
`Config.json`是高级配置文件,如果希望载入其他配置文件,请使用`python3 -c xxxx.json`  
其格式如下
```json
{
    "Basic":{
        "JianYing_Path":"", // 自定义的剪映客户端安装地址,默认为 C:\Users\你的用户名\AppData\Local\JianyingPro\Apps
        "Screenshot":false, // 是否截图用于debug
        "Install_JianYing":false // 是否安装剪映
    },
    "Webhooks":[ //定义Webhooks用于文件流操作
        { "Url":"https://example.example", "Method":"POST" },
        { "Url":"https://example.example/CallBack", "Method":"GET" },
        { "Url":"https://1.2.3.45/Hi", "Method":"GET" }
    ],
    "Sources":[
        { "Position":"Local","Url":"D://Movies/PulpFiction.mkv" ,"Webhooks":true , "Audio":true}, //单个文件粒化管理
        { "Position":"BiliBili","Bv":"BV17x411w7KC" ,"Webhooks":[0,3] ,"Schema":"Default"}, // 单个Schema
        { "Position":"BiliBili","Bv":"BV1LV4y1s74c" ,"Webhooks":[0,3] ,"P":[0,3]} //分P转换
    ]
}
```
#### Webhook 安全
如果你使用例如Server酱,钉钉机器人等推送服务，或者不想暴露自己的Webhook链接.    
你可以在Settings->Secrets->Actions添加一个名为**Webhooks**的Secret,内容和以下类似:    
```json
[
    { "Url":"https://sctapi.ftqq.com/<SENDKEY>.send", "Method":"GET" }
]
```
这样可以确保你的Token安全.  
请注意,此时你的Webhook序号在 Config.json 中设定的Webhook之后,假如Config中已经设定了两个Webhook的地址,那么在Secret中的第一个Webhook地址将会是2(前面已有0,1).  
#### Sources
- Bilibili Schema  
BiliBiliSchema是针对于某些特定的录播组/节目,允许用户自定义分P选择功能.  
**注意**当使用Schema时,指定的`P`(如果有)就会失效.  
- Audio  
在转换大文件时可以转录音频代理以避免大文件导致的卡死,在GithubActions中建议启用.    

#### 许可证及引用
License GPL V3.0
[JianYingApi](https://github.com/P-PPPP/JianYingApi)  
[JianYing Srt Server](https://github.com/A-Soul-Database/JianYingSrtServer)  
[Python-UIAutomation-for-Windows](https://github.com/yinkaisheng/Python-UIAutomation-for-Windows)  
[Pyautogui](https://github.com/asweigart/pyautogui)
[requests](https://github.com/psf/requests)  

