"""
Bili 视频下载
bv:str 
p:list
qn{
    16: 360P mp4
    32: 480P flv
    64: 720P flv
    ------ 以下需要登录Cookies才能下载
    80: 1080P flv
    116: 1080P60F flv
}
"""
import subprocess
import requests
from contextlib import closing
import threading
import time
import os
import sys
import random
if __name__ == "__main__":
    import ui
else:
    from components import ui


def Download_Bili_Video(bv:str,p:list=[],qn:str="16",ASDB:bool=False) -> bool:
    if ASDB:
        os.system("echo We Love A-Soul :) ")
    
    VIDEO_NAME = []
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
        "Referer":"https://www.bilibili.com/",
    }

    def init() -> None:
        videoname = For_You_Get(Get_Info(p))
        os.system(f"echo Start Parse {str(videoname)}")
        os.system(f"echo {os.listdir('./components/tmp')}")
        ui.Multi_Video_Process(video_Path=os.path.abspath(os.getcwd()+"./components/tmp"),Video_Item=videoname) ### Call Multi_Video_Process For Parse

    def Get_Info(p)->dict:
        os.system(f"echo Start Download {bv} Using Bili-Download")
        Bili_Video_Info_Api = f"https://api.bilibili.com/x/web-interface/view?bvid={bv}"
        Bili_Video_Info_Json = requests.get(Bili_Video_Info_Api,headers=headers).json()

        if len(Bili_Video_Info_Json["data"]["pages"]) < len(p) or len(p) ==0:
            #print("请求的分P数大于视频分P数或未指定分P,下载全部分P")
            p = [str(i) for i in range(1,len(Bili_Video_Info_Json["data"]["pages"])+1)]
        
        infos = {
            "bv":bv,
            "cover":Bili_Video_Info_Json["data"]["pic"],
            "title":Bili_Video_Info_Json["data"]["title"],
            "p":[],
        }
        rolling = p[:]
        for i in rolling:
            #循环获得每个分P的信息格式 ["分P","Cid","名字(P1 录播/)"]
            if "弹幕" in Bili_Video_Info_Json["data"]["pages"][int(i)-1]["part"] and ASDB:
                p.remove(i)
            else:
                infos["p"].append([i, Bili_Video_Info_Json["data"]["pages"][int(i)-1]["cid"], Bili_Video_Info_Json["data"]["pages"][int(i)-1]["part"] ])
            #Asdb 特有:去除带有 【弹幕】 的所有分P
        return infos
    
    def For_You_Get(info):
        """"Using You-get to download"""
        bv = info["bv"]
        
        for i in info["p"]:
            p = subprocess.Popen(f"you-get -O ./components/tmp/{bv}-{i[0]} --format=dash-flv360 https://www.bilibili.com/video/{bv}?p={i[0]}",stdout=subprocess.DEVNULL) if len(info["p"]) > 1 else subprocess.Popen(f"you-get -O ./components/tmp/{bv} --format=dash-flv360 https://www.bilibili.com/video/{bv}?p={i[0]}",stdout=subprocess.DEVNULL)
            p.wait()
            # if use it as __main__ please attention the path
        if len(info["p"]) == 1:
            return [f"{bv}.mp4"]
        return [f"{bv}-{i[0]}.mp4" for i in info["p"]]

    return init()

def You_Get_Download_Any_url(url:str,Paras:str="") -> bool:
    name = url.split("/")[-1] if len(url.split("/")[-1]) <10  else str(random.randint(1,100))
    os.system(f'echo url named {name}')
    paras = f"-O './components/tmp/{name}'"
    os.system(f"echo Start Download {url} using You-Get")
    os.system(f"you-get --debug {paras} '{url}' ")
    for item in  os.listdir("./components/tmp"):
        if name in item:
            name = item #We Dont know the format of the video
    ui.Multi_Video_Process(video_Path=os.path.abspath(os.getcwd()+"./components/tmp"),Video_Item=name)


def requests_down(url:str,headers:dict={},cookies:dict={},timeout:int=10) -> requests.Response:
    """
    Request Download
    """
    name = url.split("/")[-1] if len(url.split("/")[-1]) <10  else str(random.randint(1,100))
    name+=".mp4"
    os.system(f"echo Start Download '{name}' using requests")
    chunk_size = 1024*20
    with closing(requests.get(url,headers=headers,cookies=cookies,timeout=timeout,stream=True)) as r:
        with open(f"./components/tmp/{name}","wb") as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)

    for item in  os.listdir("./components/tmp"):
        if name in item:
            name = item #We Dont know the format of the video
    ui.Multi_Video_Process(video_Path=os.path.abspath(os.getcwd()+"./components/tmp"),Video_Item=name)
