# coding=utf-8
"""
    剪映 Srt Parser uiautomation Version For Github Actions
    Version 2.0.0-alpha-Actions
    @PPPPP
        以某些特征确定窗口(不能以类名确定)
        请注意中英文输入法切换问题
        For Asdb 字幕转换 On Acions
"""
from requests.api import delete
import uiautomation as auto
from uiautomation.uiautomation import Control
import time
import os
import keyboard
import _thread
import requests

global PROCESSING

VIDEO_PATH = ""
VIDEO_ITEM = "" 

CONFIG = {
    "draft_content_directory":"",  #剪映草稿文件地址(结尾为draft_content.json)
    "JianYing_Exe_Path":"",  #剪映客户端路径
    "Video_Path":"./tmp", #default
    "Delay_Times":1
}

targetPath = os.popen("whoami").read().replace("\n","").split("\\")[1]
targetPath,draft_Path = f'C:\\Users\\{targetPath}\\AppData\\Local\\JianyingPro\\Apps',f'C:\\Users\\{targetPath}\\AppData\\Local\\JianyingPro\\User Data\Projects\com.lveditor.draft\\'
def Path_init():
    for i in os.listdir(draft_Path):
        if i.count(".") == 0:
            CONFIG["draft_content_directory"] = os.path.join(draft_Path,i+"\\draft_content.json")
            CONFIG["JianYing_Exe_Path"] = os.path.join(targetPath,"JianYingPro.exe")

    os.system(f"echo {CONFIG}")



def Thread_Access_Multi(video_Path:str=os.path.abspath(CONFIG["Video_Path"]),Video_Item:list=[]):
    with auto.UIAutomationInitializerInThread(debug=True):
        Multi_Video_Process(video_Path,Video_Item)

def Safty_Key():
    """
        无论进行何种操作,当按下 Ctrl+x 时,程序会直接退出
    """
    while 1:
        time.sleep(1)
        if keyboard.is_pressed('ctrl+x'):
            print('Pressed Ctrl+x')
            _thread.interrupt_main()
            auto.WindowControl(Name="JianyingPro", searchDepth=1).SetTopmost(False)
            os._exit()
t = _thread.start_new_thread(Safty_Key,())

def detect_is_truely_fiished(item:list)->bool:
    """检测是否完全拿到字幕文件,若没有则返回False"""
    returnning = False
    errors = []
    item = [item] if type(item) == str else item
    for name in item:
        name = name if name.endswoth(".srt") else name + ".srt"
        if os.path.exists(name):
            srt = open(name,"r",encoding="utf-8").read().replace("\n","").replace(" ","")
            if len(srt):
                returning = True
            else:
                returning = False
                errors.append(name)
    return returning,errors

def classname_include(WindowObj:Control,SubControlType:str,ClassName:str="",Name:str="")->int:
    """
        类名是否包含某一字符串 
            -1: 调用错误
            0: 不包含
            index_found: 包含
                WindowObj: 窗口对象
                SubControlType: 子控件类型
                ClassName: 包含的类名
    """
    if ClassName == "" and Name == "":
        return -2
    index_Found = 1
    for UnkownObj in WindowObj.GetChildren():
        if UnkownObj.ControlTypeName == SubControlType:
            if (ClassName in UnkownObj.ClassName and ClassName!="") or (Name in UnkownObj.Name and Name!=""):
                return index_Found
            index_Found += 1
    return 0

def LocateStatusProxy()->int:
    """外部调用Locate()函数 (多线程) 需要通过代理"""
    with auto.UIAutomationInitializerInThread(debug=True):
        return LocateStatus()

def LocateStatus()->int:
    """
        确定现在的状态
            -1: 未启动剪映客户端
             0: 未进入主页面
             1: 已进入主页面
             2: 正在转换字幕文件/正在加载
    """
    if auto.WindowControl(Name="JianyingPro",searchDepth=1).Exists(maxSearchSeconds=0.1)==False:
        #没有窗口说明没有启动剪映客户端,return -1
        Restart_Client()
        return -1
    else:
        UnkownWindow = auto.WindowControl(Name="JianyingPro",searchDepth=1)
        if UnkownWindow.GroupControl(Name="HomePageDraft",searchDepth=1).Exists(maxSearchSeconds=0.1):
            #说明已经进入主页面,但仍未选择草稿
            return 0
        index_Found = 1
        while UnkownWindow.WindowControl(Name="JianyingPro",searchDepth=1,foundIndex=index_Found).Exists(maxSearchSeconds=0.01):
            if classname_include(WindowObj=UnkownWindow,SubControlType="WindowControl",ClassName="LoadingWindow"):
                return 2
                #说明正在转换字幕文件/正在加载
            index_Found += 1
        return 1
        #说明在主页面

def Restart_Client(isReopen:bool=True):
    """
        重启剪映客户端
            isClearTmp : 是否清理缓存
            isReopen: 是否重新启动
    """
    os.system('%s%s' % ("taskkill /F /T /IM ","JianYingPro.exe"))
    time.sleep(1)
    if isReopen:
        os.system(CONFIG["JianYing_Exe_Path"])

def into_Main_Window():
    """
        选择草稿的界面,尝试进入主界面
    """

    if LocateStatus() != 0:
        os.system("echo Not In Main Page")

    Intro_window = auto.WindowControl(Name="JianyingPro",searchDepth=1)
    Intro_window.SetTopmost(True)
    return  Intro_window.GroupControl(Name="HomePageDraft",searchDepth=1).Click()

def Single_Operation(stage:int=1)->int:
    """
        单次操作
            
        把单个操作分为三部分
            第一部分: 导入媒体文件 --- stage1
            第二部分: 尝试识别字幕并提取 --- stage2
            第三部分: 删除媒体文件 --- stage3
            stage:从某处开始,默认为1
        
        返回值:
            0: 成功
            exception: 失败
    """

    #判断是否在主界面
    if LocateStatus() != 1:
        print("Not in the main page, Restarting")
        Restart_Client()
        time.sleep(5)
        into_Main_Window()
        return Single_Operation(stage)
    #### 定义一些Position
    Main_Window = auto.WindowControl(Name="JianyingPro", searchDepth=1)
    Main_Window.ShowWindow(3,waitTime=CONFIG["Delay_Times"])
    Main_Window.SetTopmost(True)
    #置顶锁,确保元素正常被点击

    Top_Half_Window = Main_Window.PaneControl(searchDepth=1,foundIndex=classname_include(WindowObj=Main_Window,SubControlType="PaneControl",ClassName="SplitView")).PaneControl(searchDepth=1)
    Buttom_Half_Window = Main_Window.PaneControl(searchDepth=1,foundIndex=classname_include(WindowObj=Main_Window,SubControlType="PaneControl",ClassName="SplitView")).GroupControl(searchDepth=1)
    Text_Button = Top_Half_Window.GroupControl(searchDepth=1,foundIndex=classname_include(WindowObj=Top_Half_Window,SubControlType="GroupControl",Name="文本"))
    Media_Button = Top_Half_Window.GroupControl(searchDepth=1,foundIndex=classname_include(WindowObj=Top_Half_Window,SubControlType="GroupControl",Name="媒体"))
    #定位到媒体页面,便于记录媒体位置信息
    Media_Button.Click()
    Local_Media = Top_Half_Window.TextControl(searchDepth=1,foundIndex=classname_include(WindowObj=Top_Half_Window,SubControlType="TextControl",Name="素材"))
    Local_Media_Position = Local_Media.BoundingRectangle
    Buttom_Half_Window_Position = Buttom_Half_Window.BoundingRectangle
    Media_Item = (int(Local_Media_Position.left+Local_Media_Position.width()*2),Local_Media_Position.ycenter())


    def add_item():
        """
            添加文件到轨道
        """
        ######由于剪映的导入元素无法被正确定位,故需要确定两个元素的方位计算得到导入文件坐标 ######
        ######分别是ScroolBar滚动条(ControlType:"ControlType.ScrollBar") 的高度,X轴坐标、和Control(Name:"currentProgress") 的X坐标######
        ScroolBar_Position = Top_Half_Window.ScrollBarControl(searchDepth=1).BoundingRectangle
        Current_Progress_Position = Top_Half_Window.TextControl(Name="currentProgress", searchDepth=1).BoundingRectangle

        delete_media()
        auto.Click(x=int(ScroolBar_Position.left+(Current_Progress_Position.left-ScroolBar_Position.left)/2), y=ScroolBar_Position.ycenter(),waitTime=CONFIG["Delay_Times"]*2) #尝试点击添加文件

        ##########################
        #########添加文件#########
        ##########################
        Media_Window = Main_Window.WindowControl(searchDepth=1)
        Title_x = Media_Window.TitleBarControl(searchDepth=1).BoundingRectangle.left
        Title_width = Media_Window.TitleBarControl(searchDepth=1).BoundingRectangle.width()
        Title_bottom = Media_Window.TitleBarControl(searchDepth=1).BoundingRectangle.bottom
        Content_Window_top = Media_Window.PaneControl(ClassName="DUIViewWndClassName",searchDepth=1).BoundingRectangle.top
        auto.Click(x=int(Title_x+Title_width*3/5),y=int((Title_bottom+Content_Window_top)/2),waitTime=CONFIG["Delay_Times"])#点击路径选择框
        auto.SendKeys(VIDEO_PATH)
        auto.PressKey(13)#按下回车键
        Media_Window.PaneControl(searchDepth=1,foundIndex=classname_include(WindowObj=Media_Window,SubControlType="PaneControl",ClassName="ComboBox")).SendKeys(VIDEO_ITEM)
        #点击文件筐输入
        Media_Window.ButtonControl(searchDepth=1).Click()#打开媒体
        time.sleep(CONFIG["Delay_Times"]*5)
        auto.DragDrop(x1=Media_Item[0],y1=Media_Item[1],x2=Buttom_Half_Window_Position.xcenter(),y2=Buttom_Half_Window_Position.ycenter(),waitTime=CONFIG["Delay_Times"]*2)

    def srt_identify():
        """
            尝试识别字幕
        """
        Text_Button.Click()
        #点击默认的新建文本以收回默认展开
        if classname_include(WindowObj=Top_Half_Window,SubControlType="TextControl",Name="收藏"):
            Top_Half_Window.TextControl(searchDepth=1,foundIndex=classname_include(WindowObj=Top_Half_Window,SubControlType="TextControl",Name="新建文本")).Click()
        #点击智能字幕
        Top_Half_Window.TextControl(searchDepth=1,foundIndex=classname_include(WindowObj=Top_Half_Window,SubControlType="TextControl",Name="智能字幕")).Click()
        Unkown_Button = Top_Half_Window.TextControl(searchDepth=1,foundIndex=classname_include(WindowObj=Top_Half_Window,SubControlType="TextControl",Name="识别歌词")).BoundingRectangle
        auto.Click(x=int(Unkown_Button.xcenter()+Unkown_Button.width()*2),y=int(Unkown_Button.bottom),waitTime=CONFIG["Delay_Times"])
        auto.Click(x=int(Unkown_Button.xcenter()+Unkown_Button.width()*2),y=int(Unkown_Button.bottom+Unkown_Button.height()*2),waitTime=CONFIG["Delay_Times"])
        while 1:
            #等待识别完成
            time.sleep(5)
            os.system("echo Waiting for recognition to complete")
            if LocateStatus() == 1:
                break
        tracks = draft_content.read_draft_content_src(CONFIG["draft_content_directory"])
        if __name__ == "__main__":
            nam = ""
        else:
            nam = "./components/tmp/"
        with open(nam+VIDEO_ITEM.split(".")[0]+".srt", 'w', encoding='utf-8') as f:
            f.write(simple_srt.tracks_to_srt_string(tracks))


    def delete_media():
        """
            删除已经完成的媒体
        """
        Media_Button.Click()
        auto.Click(x=Media_Item[0],y=Media_Item[1])
        auto.PressKey(46)
        if Main_Window.WindowControl(searchDepth=1,foundIndex=classname_include(WindowObj=Main_Window,SubControlType="WindowControl",ClassName="VEToastWindow")).GroupControl(searchDepth=1).Exists(searchIntervalSeconds=0.5):
            Main_Window.WindowControl(searchDepth=1,foundIndex=classname_include(WindowObj=Main_Window,SubControlType="WindowControl",ClassName="VEToastWindow")).GroupControl(searchDepth=1).Click()#删除文件

        #删除轨道中的字幕
        auto.Click(Buttom_Half_Window_Position.xcenter(),Buttom_Half_Window_Position.ycenter(),waitTime=CONFIG["Delay_Times"])
        auto.SendKeys("{Ctrl}A",waitTime=CONFIG["Delay_Times"])
        auto.PressKey(8,waitTime=CONFIG["Delay_Times"])
        #auto.PressKey(46,waitTime=2)

    if stage==1:
        add_item()
        srt_identify()
        delete_media()
    if stage==2:
        srt_identify()
        delete_media()
    if stage==3:
        delete_media()

    Main_Window.SetTopmost(False) #释放置顶锁 
    return 0

def Multi_Video_Process(video_Path:str=os.path.abspath(CONFIG["Video_Path"]),Video_Item:list=[]):
    """
        多媒体文件使用 自动扫描目录下所有媒体文件
        目录配置:  CONFIG["Video_Path"]
    """
    global VIDEO_PATH,VIDEO_ITEM
    VIDEO_PATH = video_Path
    def convert_to_m4a(filename)->str:
        """转换视频为m4a 文件以排除码率问题"""
        try:
            os.system(f"ffmpeg -y -loglevel error -i {VIDEO_PATH}/{filename} -vn -codec copy {VIDEO_PATH}/{filename.split('.')[0]}.m4a")
        except:
            os.system(f".\\ffmpeg.exe -y -loglevel error -i {VIDEO_PATH}/{filename} -vn -codec copy {VIDEO_PATH}/{filename.split('.')[0]}.m4a") 
            #Choose local ffmpeg.exe
        return f"{filename.split('.')[0]}.m4a"

    if len(Video_Item):
        Video_List = Video_Item
    else:
        Video_List = [fn for fn in os.listdir(VIDEO_PATH) if any(fn.endswith(format) for format in ['.mp4','.avi','.mkv','.mov','.flv'])]

    for Video_Item in Video_List:
        if os.path.exists(VIDEO_PATH+"/"+Video_Item.split(".")[0]+".srt"):
            #说明已经转换过了
            print(f"{Video_Item} Has Parsed, Skip")
            continue
        VIDEO_ITEM = convert_to_m4a(Video_Item)

        
        Tried_times = 0
        with auto.UIAutomationInitializerInThread(debug=True):
            result = Single_Operation()
            while result!= 0:
                Restart_Client()
                result = Single_Operation()
                if result == 0 or Tried_times>3:
                    break
                Tried_times += 1
            process_result = True if result == 0 else False
        os.system(f"echo {Video_Item} with result  {result} (0 represents success)")

    return process_result


if __name__ == "__main__":
    from srtParser import draft_content as draft_content
    from srtParser import simple_srt as simple_srt
    Multi_Video_Process()
else:
    from components.srtParser import draft_content as draft_content
    from components.srtParser import simple_srt as simple_srt