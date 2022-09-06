from JianYingApi import JianYingApi as Api
import subprocess
import os
import argparse
import json
import time
import logging
from utils import  bilibili_schema , prepare_env , download_bilibili , media_type , Webhooks

os.path.exists("./outputs") == False and os.mkdir("./outputs")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler(filename=f'log.log', encoding='UTF-8')
logger.addHandler(console_handler)
logger.addHandler(file_handler)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
Ga_Running = True

def install_jianYing():
    '''
        Down and install Jianying
    '''
    prepare_env.DownloadJianYing()
    Api.Logic_warp._install_JianYing("jy.exe")

def took_screenshot(lap:float=2.0):
    '''Took Screen shot Every lap'''
    os.path.exists("./outputs/screenshots") == False and os.mkdir("./outputs/screenshots")
    import pyautogui , time
    _i = 0
    while Ga_Running:
        _i += 1
        time.sleep(lap)
        pyautogui.screenshot(f"./outputs/{_i}.png")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-m','--mode',default="local",help='Working mode. [ Ga | local ]. Default is local, Ga(Github Actions) Will install essentials | 在Github Actions 模式下请选择')
    parser.add_argument('--install_jianying',type=bool,default=False,help='It helps you to install jianying | 安装剪映')
    parser.add_argument('-c','--Config',default="./Config.json",help='Parser Config | 指定Config文件解析')
    parser.add_argument('--bilibili',help='parse a bilibili bv | 通过Bv号进行字幕转换')
    parser.add_argument('--local',help='Parse a local video | 转换一个本地文件')
    args = parser.parse_args()
    Config = json.loads(open(args.Config,"r",encoding="utf-8").read())
    assert ((args.bilibili != None) or (len(Config["Sources"]) > 0) or (args.local != None)) == True , IndexError("Please Add One Source | 请至少设置一个文件以转换字幕")
    if Config["Basic"]["Screenshot"] == True:
        from threading import Thread
        Thread(target=took_screenshot,daemon=True).start()
    # 安装剪映
    logging.debug("Installing JianYing.")
    if (args.install_jianying == True) or (Config["Basic"]["Install_JianYing"]==True) or (args.mode == "Ga"): install_jianYing()

    Api.Logic_warp._kill_jianYing()
    if os.path.exists(Api.Logic_warp._Get_JianYing_Default_Path()) == False:
        assert ("JianYing_Path" in Config["Basic"]) or os.path.exists(Config["Basic"].get("JianYing_Path")) == True , FileNotFoundError("Cannot Found Jianying Paath | 无法在默认目录中找到剪映文件")

    # 下面进行一些Config中的语法检查
    logging.debug("Grammar Checking.")
    if args.mode == "Ga":
        try:
            Config["Webhooks"] += json.loads(os.environ["WEBHOOKS"])
        except KeyError: logger.info("No Webhooks Detected In Github Action Keys. Passed ... ")
    _w_n = len(Config["Webhooks"])
    for i in Config["Sources"]:
        if type(i["Webhooks"]) == list:
            for n in i["Webhooks"]: assert n < _w_n , IndexError(f"Webhook Sequence{n} Should Less Than Num {_w_n} | Webhook 序号{n} 应小于总个数 {_w_n}")
        if i["Position"] == "Local": assert os.path.exists(i["Url"]) == True , FileNotFoundError(f"Couldn't Found Media | 文件不存在 ")
        if i.get("Schema"):
            if i["Schema"] != None:
                if i["Position"] != "BiliBili": logging.warn("Dismatch Attribute(Schema) | 属性错误(Schema)")
                getattr(bilibili_schema,i["Schema"]) # This Will Through An Error If Your Schema Is Error
        if i["Position"] == "BiliBili":assert i["Bv"] != None, FileNotFoundError("No Bv Found | 未填写Bv号")
    del _w_n

    # 下载安装并启动剪映
    Api.Logic_warp._kill_jianYing()
    if "JianYing_Path" in Config["Basic"] and Config["Basic"]["JianYing_Path"] != "": _ins = Api.Jy_Warp.Instance(Start_Jy=True,JianYing_Exe_Path=os.path.join(Config["Basic"]["JianYing_Path"],"Apps","JianyingPro.exe"))
    else: _ins = Api.Jy_Warp.Instance(Start_Jy=True) # Default Path

    _ins._Start_New_Draft_Content(wait=True) #进入主页面

    # 准备媒体文件
    logging.debug("Preparing Media.")
    for i in Config["Sources"]:
        _roll = []
        if i["Position"] == "BiliBili" : _roll = download_bilibili.bilibili(i)
        if i["Position"] == "Local": 
            _roll.append(media_type.Media_Type(
                path=os.path.dirname(os.path.abspath(i["Url"])),filename=os.path.basename(os.path.abspath(i["Url"]))
            ))
        if i["Audio"] == True:
            for n in _roll: 
                n.to_m4a() # n is defined in  utils/media_type.py
        i["roll"] = _roll

    # 开始转换
    logging.debug("Converting Subtitle.")
    for n in Config["Sources"]:
        for i in n["roll"]:
            exp = Api.Jy_Warp.Export_Options(export_sub=True,export_name=i.rawname,export_path=i.path,export_vid=False)
            if i.hasm4a: Api.Api.Recognize_Subtitle(filename=i.m4a,filepath=i.path,export_options=exp,jianying_instance=_ins)
            else: Api.Api.Recognize_Subtitle(filename=i.filename,filepath=i.path,export_options=exp,jianying_instance=_ins)
            Webhooks.Webhooks(Config["Webhooks"],n,mesage=json.dumps({
                "TransformFinished":i.rawname,
                "Finish_Time":time.ctime(),
                "Subtitle_Path":i.path,
                "Subtitle_Name":i.rawname
            },ensure_ascii=False,indent=4))

    # 若以Github Actions模式运行,则有
    logging.debug("Assets Packing for GithubActions.")
    if args.mode == "Ga":
        # 打包output
        subprocess.run(f"7z a ./GA.zip ./outputs")
        Api.Logic_warp._kill_jianYing()
        Ga_Running = False