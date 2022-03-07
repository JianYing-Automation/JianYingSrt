"""
    Github Actions Debug Windows Gui Applications Template
    For Asdb 
    By @P_P_P_P_P
"""
import requests
import os
from contextlib import closing
import pyautogui
import uiautomation as auto
from threading import Thread
import time
import shutil
import zipfile
import json
import sys
import subprocess
import time
from components import ui
from components import video_Down

config = json.loads(open("./config.json","r",encoding="utf-8").read())
#Get Current Repo Name to check if tags created
tags = requests.get(url="https://api.github.com/repos/"+os.popen("echo  ${{ github.event.repository.name }}").read().replace("\n","")+"/tags").json()
for i in tags:
    if i in config["url"]:
        print("[+] Found Tag: "+i)
        sys.exit(1)
# Same tag is not allowed

targetPath = os.popen("whoami").read().replace("\n","").split("\\")[1]
targetPath,draft_Path = f'C:\\Users\\{targetPath}\\AppData\\Local\\JianyingPro\\Apps',f'C:\\Users\\{targetPath}\\AppData\\Local\\JianyingPro\\User Data\Projects\com.lveditor.draft\\'

os.makedirs("./components/tmp")

def timmer(func):
    def deco(*args, **kwargs):
        os.system('echo \Function: {_funcname_} Start Run'.format(_funcname_=func.__name__))
        start_time = time.time()
        res = func(*args, **kwargs)
        end_time = time.time()
        os.system('echo Function :{_funcname_} Finished with  {_time_} Seconds'
              .format(_funcname_=func.__name__, _time_=(end_time - start_time)))
        return res
    return deco

# thats where JianYing Pro is to be installed
global PROCESSING
PROCESSING = True


class Prepare():
    """
        This Class Will Install JianYing Pro and Dependencies
    """
    def __init__(self):
        self.DownloadJy()
        self.Install()
        self.Initialize_JianYing()
    
    Status = {
        "Installed":False
    }

    @timmer
    def DownloadJy(self):

        os.system("echo Start Download JianYingPro")
        url = "https://lf3-package.vlabstatic.com/obj/faceu-packages/Jianying_pro_2_7_0_7723_jianyingpro_0.exe"
        name = url.split("/")[-1]
        os.system(f"echo Downloading {name} ...")
        with closing(requests.session().get(url,stream=True)) as response:
            chunk_size = 1024
            with open(f"{name}", "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
        os.system("echo JianYingPro download complete")

        os.system("echo Start Donwload ffmpeg")
        ffmpeg = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-n4.4-latest-win64-lgpl-4.4.zip"
        with closing(requests.session().get(ffmpeg,stream=True)) as response:
            chunk_size = 1024
            with open("ffmpeg.zip", "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
        for i in zipfile.ZipFile("./ffmpeg.zip").namelist():
            if i.split("/")[-1] == "ffmpeg.exe":
                zipfile.ZipFile("./ffmpeg.zip").extract(i,"./")
                shutil.move(i,"./ffmpeg.exe")
                break
        os.system("echo ffmpeg extracted")
        
        def Install_JianYing():
            # it's necessary to run a install command with a new thread to avoid blocking
            p = subprocess.Popen(name)
            while self.Status["Installed"]==False:
                time.sleep(10)
            p.kill()
        t = Thread(target=Install_JianYing)
        t.start()
        os.system("echo Download complete")

    @timmer
    def Install(self):
        """ Install JianYing """
        Install_Window = auto.WindowControl(searchDepth=1,ClassName="#32770")
        auto.Click(x=Install_Window.BoundingRectangle.xcenter(),y=int(Install_Window.BoundingRectangle.ycenter()-Install_Window.BoundingRectangle.height()/8)) 
        # stimulate the click to the install button
        while True:
            try:
                if "JianyingPro.exe" in os.listdir(targetPath):
                    break
                    # check if the install process is complete
                else:
                    time.sleep(10)
            except:
                pass
        self.Status["Installed"] = True
        os.system("echo found JianyingPro.exe, Install Complete")
    

    def Open_JianYing(self):
        p = subprocess.Popen(targetPath+"\\JianyingPro.exe")
        while PROCESSING:
            time.sleep(20)
        p.kill()

    @timmer
    def Initialize_JianYing(self):
        os.system("echo Initialize JianYing")
        Thread(target=self.Open_JianYing).start()
        #for the first time , JianYing will open VEDetector.exe to detect sys environment
        time.sleep(10)
        Upload()
        os.system('%s%s' % ("taskkill /F /T /IM ","VEDetector.exe"))
        os.system('%s%s' % ("taskkill /F /T /IM ","JianYingPro.exe"))
        #Turn Off the VEDetector.exe
        self.Get_Draft_Content_Path(1)
        return True

    @timmer
    def Get_Draft_Content_Path(self,mode:int):
        os.system("echo Get Draft Content Path")
        if mode:
            Thread(target=self.Open_JianYing).start()
        time.sleep(5)
        if auto.WindowControl(Name="JianyingPro",searchDepth=1).Exists() == False:
            time.sleep(2)
            return self.Get_Draft_Content_Path(0)
        Intro_window = auto.WindowControl(Name="JianyingPro",searchDepth=1)
        Intro_window.SetTopmost(True)
        Intro_window.TextControl(Name="HomePageStartProjectName",searchDepth=1).Click()
        time.sleep(1)
        
        if ui.LocateStatus() == 1:
            for i in os.listdir(draft_Path):
                if i.count(".") == 0:
                    os.system('%s%s' % ("taskkill /F /T /IM ","JianYingPro.exe"))
                    ui.Path_init()
                    return os.path.join(draft_Path,i+"\\draft_content.json")

def Upload():
    """Took a screenshot and upload to Server for debug"""
    name = str(int(time.time()))+'.png'
    im = pyautogui.screenshot("./components/tmp/"+name)
    im.save("./components/tmp/"+name)
    #r = requests.post('http://subserver.asdb.live/receveUpload', files={'file': open("./components/tmp/"+name, 'rb')})
    #os.system(f"echo {r.text}")



# Maybe We Should Let The Game Play
#扔一个进程每隔十秒钟上传图片
def Upload_Thread():
    while PROCESSING:
        time.sleep(20)
        Upload()

t = Thread(target=Upload_Thread,daemon=True)
t.start()

Prepare()

os.system("echo Prepare Complete , Satrting Parse")

for i in config["url"]:
    try:
        if config["types"] == "requests":
            video_Down.requests_down(i)
        elif config["types"] == "you-get":
            video_Down.You_Get_Download_Any_url(i)
        elif config["types"] == "bili":
            video_Down.Download_Bili_Video(i,ASDB=config["ASDB"]) #### Call Video_Down.py to download the video and next operations
        exitcode = 0
    except :
        pass

os.system('%s%s' % ("taskkill /F /T /IM ","JianYingPro.exe"))
if config["types"] == "bili":
    version = ','.join(config["url"])
else:
    version = ','.join(config["url"]).replace("?","").replace("&","").replace(" ","")
env_file = os.getenv('GITHUB_ENV')
with open(env_file, "a") as f:
    f.write(f"Version={version}")
    f.write("\n")
    f.write(f"Tags={version}")
PROCESSING = False
#Create zip
assets = [fn for fn in os.listdir("./components/tmp") if any(fn.endswith(ext) for ext in [".png",".jpg",".srt"])]
with zipfile.ZipFile("./components/tmp/All.zip",'w') as zip:
    for asset in assets:
        zip.write("./components/tmp/"+asset,asset)

os.system(f"echo assets.zip created")

#sending webhooks
for webs in config["webhooks"]:
    r = requests.post(webs,json={"SrtRunning":"ends"})
    os.system(f"echo Send Webhook to {webs} with {r.status_code}")
sys.exit(0)
