import os
import requests
import subprocess

def aria2(url,name,args:str=""):
    return subprocess.Popen(f'aria2c -x 16 -s 16 -k 1M -o "./components/tmp/{name}" "{url}" {args}',shell=False,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).wait()

def bilibili(bv:str,ASDB:bool=False,download_sourcer:int=0):
    # Sourcer 
    # 0: h5播放链接
    # 1: api接口
    # 2: 音频
    headers = {"User-Agent":"Mozilla/5.0"}
    if "bilibili" in bv: bv = bv.split("/")[-1].split("?")[0]
    pages = requests.get(f"https://api.bilibili.com/x/web-interface/view?bvid={bv}",headers=headers)
    pages.encoding = 'utf-8'
    pages = pages.json()["data"]["pages"]
    if ASDB: cids = [fn["cid"] for fn in pages
            if "弹幕" not in fn["part"]]
    else: cids = [fn["cid"] for fn in pages]
    os.system(f"echo Start Download For {bv} with {cids}")
    for i in cids:
        if download_sourcer == 0:
            download_url = requests.get(f"https://api.bilibili.com/x/player/playurl?bvid={bv}&cid={i}&otype=json&&platform=html5&high_quality=0",headers=headers)
            download_url.encoding='utf-8'
            download_url = download_url.json()["data"]["durl"][0]["url"]
        if download_sourcer == 1:
            download_url = requests.get(f"https://api.bilibili.com/x/player/playurl?bvid={bv}&cid={i}&qn=16",headers=headers)
            download_url.encoding='utf-8'
            download_url = download_url.json()["data"]["durl"][0]["url"]
        if download_sourcer == 2:
            download_url = requests.get(f"https://api.bilibili.com/x/player/playurl?bvid={bv}&cid={i}&qn=0&fnver=0&fnval=80",headers=headers)
            download_url.encoding='utf-8'
            download_url = download_url.json()["data"]["dash"]["audio"][0]["baseUrl"]

        aria2(url=download_url,name=f"{bv}-{cids.index(i)+1}.mp4" if len(cids) >1 else f"{bv}.mp4",args=' --header="Refer:https://www.bilibili.com" --user-agent="Mozilla/5.0" ')
