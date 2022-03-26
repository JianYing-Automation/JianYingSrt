import os
import requests


def aria2(url,name,args:str=""):
    return os.system(f'aria2c -x 16 -s 16 -k 1M -o ./components/tmp/{name} "{url}" {args}')

def bilibili(bv:str,ASDB:bool=False):
    headers = {"User-Agent":"Mozilla/5.0"}
    if "bilibili" in bv: bv = bv.split("/")[-1].split("?")[0]

    if ASDB: cids = [fn["cid"] for fn in requests.get(f"https://api.bilibili.com/x/web-interface/view?bvid={bv}",headers=headers).json()["data"]["pages"]
            if "弹幕" not in fn["part"]]
    else: cids = [fn["cid"] for fn in requests.get(f"https://api.bilibili.com/x/web-interface/view?bvid={bv}",headers=headers).json()["data"]["pages"]]

    for i in cids:
        download_url = requests.get(f"https://api.bilibili.com/x/player/playurl?bvid={bv}&cid={i}&otype=json&&platform=html5&high_quality=0",headers=headers).json()["data"]["durl"][0]["url"]
        aria2(url=download_url,name=f"{bv}-{cids.index(i)+1}.mp4" if len(cids) >1 else f"{bv}.mp4",args=' --header="Refer:bilibili.com" ')
