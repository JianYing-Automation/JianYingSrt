import os
import requests
from contextlib  import closing
import random

def requests_down(url:str,headers:dict={},cookies:dict={},timeout:int=10,ThreadNum:int=0) -> requests.Response:
    """
    Request Download
    """
    name = url.split("/")[-1] if len(url.split("/")[-1]) <10  else str(random.randint(1,100))
    name+=".mp4"
    print(f"Start Download '{url}' using requests")
    chunk_size = 1024*1024
    with closing(requests.get(url,headers=headers,cookies=cookies,timeout=timeout,stream=True)) as r:
        with open(f"./components/tmp/{name}","wb") as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)

    for item in  os.listdir("./components/tmp"):
        if name in item:
            name = item #We Dont know the format of the video
    os.system("echo 11111111111111")

requests_down("https://nf.asoul-rec.com/ASOUL-REC/2022.01.02%20%E4%B9%83%E7%90%B350%E4%B8%87%E7%B2%89%E7%BA%AA%E5%BF%B5%E5%9B%9E.mp4?proxied&raw")