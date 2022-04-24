"""
    JianYing Srt Parser
    For Asdb 
    By @P_P_P_P_P
"""
import pyautogui , time , os , subprocess, json , sys, subprocess , datetime , base64 , pytz, os
import uiautomation as auto
import components.ui as ui
import components.video_Down as vd

Start_Time = time.time()
Config = json.loads(open("./Config.json","r",encoding="utf-8").read())

def Start_Func(func):
    def deco(*args, **kwargs):
        os.system('echo Function: {_funcname_}'.format(_funcname_=func.__name__))
        start_time = time.time()
        res = func(*args, **kwargs)
        os.system('echo Function :{_funcname_} Finished in  {_time_} Sec'
              .format(_funcname_=func.__name__, _time_=(time.time() - start_time)))
        return res
    return deco

class Etcs:
    def Screenshot(self,delay:int):
        while True:
            time.sleep(delay)
            pyautogui.screenshot(f"{Config['Sources_Path']}{int(time.time()-Start_Time)}.png")
    
    @Start_Func
    def Get_Paths(self):
        whoami = os.popen("whoami").read().replace("\n","").split("\\")[1]
        Base_Dir = "C:/Users/{}/AppData/Local/JianyingPro".format(whoami)
        Config["Base_Dir"] ,Config["JianYing_App_Path"]  = Base_Dir , '/'.join([Base_Dir,"Apps/JianyingPro.exe"])

    def Kill_All(self):
        subprocess.Popen('%s%s' % ("taskkill /F /T /IM ","VEDetector.exe"),stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).wait()
        subprocess.Popen('%s%s' % ("taskkill /F /T /IM ","JianYingPro.exe"),stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).wait()
        return 

    def Start_JianYing(self):
        return subprocess.Popen(Config["JianYing_App_Path"],shell=True)

class Actions:

    @Start_Func
    def Install_JianYing(self):
        os.mkdir("./components/tmp") if not os.path.exists("./components/tmp") else None
        #subprocess.run("choco install -y ffmpeg aria2 7zip",shell=False
        #    ,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        subprocess.Popen(f"aria2c  -x 16 -s 16 -k 1M -o ./_tmp.exe {Config['Jy_Download_Url']}",shell=False,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).wait()
        os.system(f"echo Finish Install Dependiencies")
        install_process = subprocess.Popen("_tmp.exe",shell=True)
        while True:
            if auto.WindowControl(searchDepth=1,ClassName="#32770").Exists(): break
        Instance = auto.WindowControl(searchDepth=1,ClassName="#32770")
        auto.Click(x=Instance.BoundingRectangle.xcenter(),y=int(Instance.BoundingRectangle.ycenter()-Instance.BoundingRectangle.height()/8))
        while True:
            if os.path.exists(Config["JianYing_App_Path"]): break
        install_process.kill()
        Etcs().Kill_All()
        while auto.WindowControl(searchDepth=1,ClassName="#32770").Exists(): auto.Click(x=Instance.BoundingRectangle.xcenter(),y=int(Instance.BoundingRectangle.ycenter()-Instance.BoundingRectangle.height()/8))


    @Start_Func
    def Took_Draft_Content_Path(self):
        Etcs().Kill_All()
        Jian_Ying_Process = Etcs().Start_JianYing()
        while ui.Locate_Status(timeout_seconds=2) != 0:...
        before_list = os.listdir(Config["Base_Dir"]+"/User Data/Projects/com.lveditor.draft")
        jy_window = auto.WindowControl(Name="JianyingPro",searchDepth=1)
        jy_window.SetTopmost()
        jy_window.TextControl(Name="HomePageStartProjectName",searchDepth=1).Click()
        while ui.Locate_Status(timeout_seconds=2) != 1:...
        Jian_Ying_Process.kill()
        Etcs().Kill_All()
        after_list = os.listdir(Config["Base_Dir"]+"/User Data/Projects/com.lveditor.draft")
        Config["Draft_Content_Json"] = Config["Base_Dir"] + "/User Data/Projects/com.lveditor.draft/" +  [i for i in after_list if i not in before_list][0] + "/draft_content.json"

class Release:


    Release_Introduce = ""
    def Create_Assets(self):
        os.system("7z a -tzip {}All.zip {}*.srt {}*.png {}*.jpg".format(Config["Sources_Path"],Config["Sources_Path"],Config["Sources_Path"],Config["Sources_Path"]))

    def Output_Version(self):
        env_file = os.getenv('GITHUB_ENV')
        tz = pytz.timezone('Asia/Shanghai')
        date = datetime.datetime.now(tz).strftime("%Y.%m.%d_%H/%M")
        tags = base64.encodebytes(self.Release_Introduce.encode('utf-8')).decode('utf-8').replace('\n','') + date
        os.system(f"echo Introduce : {self.Release_Introduce} , date:{date} , tags:{tags}")
        with open(env_file, "a") as f:
            f.write(f"Version=1.0")
            f.write("\n")
            f.write(f"Tags={tags}")
            f.write("\n")
            f.write(f"Introduce={self.Release_Introduce}")
        os.system(f"echo env: {env_file}")

if __name__ == "__main__":
    Running_Type = sys.argv[1] if len(sys.argv) > 1 else "local"

    if Running_Type == "local":
        Etcs().Get_Paths()
        Actions().Took_Draft_Content_Path()
        ui.CONFIG["draft_content_directory"] = Config["Draft_Content_Json"]
        ui.CONFIG["JianYing_Exe_Path"] = Config["JianYing_App_Path"]
        ui.Multi_Video_Process(video_path=Config['Sources_Path'])

    elif Running_Type == "actions":
        from threading import Thread
        # Run on Github
        r = Release()
        Thread(target=Etcs().Screenshot,args=(1,),daemon=True).start()

        Etcs().Get_Paths()
        Actions().Install_JianYing()
        Actions().Took_Draft_Content_Path()
        ui.CONFIG["draft_content_directory"] = Config["Draft_Content_Json"]
        ui.CONFIG["JianYing_Exe_Path"] = Config["JianYing_App_Path"]
    
        for item in Config["url"]:
            r.Release_Introduce += item+";"
            if "bv" in item.lower() or "bilibili.com" in item.lower(): vd.bilibili(item,ASDB=Config["ASDB"],download_sourcer=0)
            else: vd.aria2(item,item.split("/")[-1])
        try:
            ui.Multi_Video_Process(video_path=Config['Sources_Path'])
        except Exception as e: os.system(f"echo {e}")
        r.Create_Assets(),r.Output_Version()

    elif Running_Type == "install": Actions().Install_JianYing()
    elif Running_Type == "nonactions":
        Etcs().Get_Paths()
        Actions().Took_Draft_Content_Path()
        ui.CONFIG["draft_content_directory"] = Config["Draft_Content_Json"]
        ui.CONFIG["JianYing_Exe_Path"] = Config["JianYing_App_Path"]
        for item in Config["url"]:
            if "bv" in item.lower() or "bilibili.com" in item.lower(): vd.bilibili(item,ASDB=Config["ASDB"],download_sourcer=0)
            else: vd.aria2(item,item.split("/")[-1])
        ui.Multi_Video_Process(video_path=Config['Sources_Path'])
