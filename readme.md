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
    "Jy_Download_Url":"https://lf3-package.vlabstatic.com/obj/faceu-packages/Jianying_pro_2_8_0_7815_jianyingpro_0.exe", #剪映的下载链接,不用动
    "ASDB":true, 
    "url":["BV1D3411W7K6"],
    "Sources_Path":"./components/tmp/",
    "webhooks":[]
}
```
- 转换完成后会发布到Release下

#### Bug排查
对于自动化测试而言,对于Bug的排查会有些复杂,在Release中会发布截图,可以根据这些信息排查Bug

#### TagExist
字幕转换完成之后会发布一个Release,Tag是Bv号,但如果这个Tag已经存在**则会报错**,尝试Clone项目到本地执行`tag git push origin :refs/tags/Tag名称` 即可

#### TODO
- [x] 增加Webhook

#### 许可证及引用

License GPL V3.0

[JianYing Srt Server](https://github.com/A-Soul-Database/JianYingSrtServer)  
[Python-UIAutomation-for-Windows](https://github.com/yinkaisheng/Python-UIAutomation-for-Windows)  
[Pyautogui](https://github.com/asweigart/pyautogui)
[requests](https://github.com/psf/requests)  
[You-Get](https://github.com/soimort/you-get)  
