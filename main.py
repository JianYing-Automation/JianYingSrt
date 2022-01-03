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
import keyboard
import sys
import subprocess
from components import ui
from components import video_Down

targetPath = os.popen("whoami").read().replace("\n","").split("\\")[1]
targetPath,draft_Path = f'C:\\Users\\{targetPath}\\AppData\\Local\\JianyingPro\\Apps',f'C:\\Users\\{targetPath}\\AppData\\Local\\JianyingPro\\User Data\Projects\com.lveditor.draft\\'

os.makedirs("./components/tmp")


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

    def DownloadJy(self):

        os.system("echo Start Download JianYingPro")
        url = "https://lf3-package.vlabstatic.com/obj/faceu-packages/Jianying_pro_2_5_5_6688_jianyingpro_baidupz.exe"
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

    def Initialize_JianYing(self):
        os.system("echo Initialize JianYing")
        Thread(target=self.Open_JianYing).start()
        #for the first time , JianYing will open VEDetector.exe to detect sys environment
        time.sleep(10)
        Upload()
        os.system('%s%s' % ("taskkill /F /IM ","VEDetector.exe"))
        os.system('%s%s' % ("taskkill /F /IM ","JianyingPro.exe"))
        #Turn Off the VEDetector.exe
        self.Get_Draft_Content_Path()
        return True

    def Get_Draft_Content_Path(self):
        os.system("echo Get Draft Content Path")
        Thread(target=self.Open_JianYing).start()
        time.sleep(5)
        Intro_window = auto.WindowControl(Name="JianyingPro",searchDepth=1)
        Intro_window.SetTopmost(True)
        Intro_window.TextControl(Name="HomePageStartProjectName",searchDepth=1).Click()
        time.sleep(1)
        
        if ui.LocateStatus() == 1:
            for i in os.listdir(draft_Path):
                if i.count(".") == 0:
                    os.system('%s%s' % ("taskkill /F /IM ","JianyingPro.exe"))
                    ui.Path_init()
                    return os.path.join(draft_Path,i+"\\draft_content.json")

def Upload():
    """Took a screenshot and upload to Server for debug"""
    name = str(int(time.time()))+'.png'
    im = pyautogui.screenshot("./components/tmp/"+name)
    im.save("./components/tmp/"+name)
    r = requests.post('http://subserver.asdb.live/receveUpload', files={'file': open("./components/tmp/"+name, 'rb')})
    os.system(f"echo {r.text}")



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
bvs = open("./list.txt","r",encoding="utf-8").read().split("\n")
for i in bvs:
    video_Down.Download_Bili_Video(i)

PROCESSING = False
os.system(f"echo {PROCESSING}")
os.system('%s%s' % ("taskkill /F /IM ","JianyingPro.exe"))
version = ','.join(bvs)
os.system(f'echo "::set-output name=version::{version}"')
os.system(f'echo "::set-output name=tags::{version}"')
#Create zip
assets = [fn for fn in os.listdir("./components/tmp") if any(fn.endswith(ext) for ext in [".png",".jpg",".srt"])]
with zipfile.ZipFile("./components/tmp/All.zip",'w') as zip:
    for asset in assets:
        zip.write("./components/tmp/"+asset,asset)

os.system(f"echo assets.zip created")
sys.exit(0)