import os
import requests
from . import bilibili_schema
from . import prepare_env
from . import media_type

def bilibili(i:dict)->list:
    # Sourcer 
    # 1: api接口
    _k = []
    headers = {"User-Agent":"Mozilla/5.0"}
    pages = requests.get(f"https://api.bilibili.com/x/web-interface/view?bvid={i['Bv']}",headers=headers)
    pages.encoding = 'utf-8'
    pages = pages.json()["data"]["pages"]
    if i["P"] != None: cids = [fn["cids"] for fn in pages if pages.index(fn) in i["P"]] # 有优化空间,但是更简洁
    if i["Schema"] != None: cids = bilibili_schema.locals()[i["Schema"]](pages)
    else: cids = bilibili_schema.Default(pages)
    os.system(f"echo Start Download For {i['Bv']} with {cids}")
    for i in cids:
        download_url = requests.get(f"https://api.bilibili.com/x/player/playurl?bvid={i['Bv']}&cid={i}&qn=16",headers=headers)
        download_url.encoding='utf-8'
        download_url = download_url.json()["data"]["durl"][0]["url"]
        pname = f"{i['Bv']}-{cids.index(i)+1}.mp4" if len(cids) >1 else f"{i['Bv']}.mp4"
        prepare_env.aria2(url=download_url,p_name=pname,header=' --header="Refer:https://www.bilibili.com" --user-agent="Mozilla/5.0" ')
        _k.append(media_type.Media_Type(path=os.path.commonpath(os.path.abspath(pname)),
                                        filename=os.path.basename(os.path.abspath(pname))))
    return _k