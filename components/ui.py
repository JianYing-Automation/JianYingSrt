# coding=utf-8
"""
    剪映 Srt Parser uiautomation Version For Github Actions
    Version 2.1.0-beta-Actions
    @PPPPP
        For Asdb 字幕转换 On Acions
    
    Fit version for Jianying 2.9.0 on Windows.
"""
import uiautomation as auto
from uiautomation.uiautomation import Control
import time
import os
import keyboard
import _thread
import subprocess
import requests

global PROCESSING

VIDEO_PATH = ""
VIDEO_ITEM = "" 

CONFIG = {
    "draft_content_directory":r"",  #剪映草稿文件地址(结尾为draft_content.json)
    "JianYing_Exe_Path":r"",  #剪映客户端路径
    "Video_Path":"./tmp", #default
    "Delay_Times":1,
    "webhook":False,
    "webhook_url":r"",
}

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

def Locate_Status(timeout_seconds:int=0.5):
    """
        确定现在的状态
            -1: 未启动剪映客户端
            0: 未进入主页面
            1: 已进入主页面
            2: 正在转换字幕文件/正在加载
    """
    try:
        if auto.WindowControl(Name="JianyingPro",searchDepth=1).Exists(maxSearchSeconds=timeout_seconds)==False: return -1
    except : return -1
    # 未启动客户端自然为-1,但仍需考虑启动但未进入主界面的情况
    jy_main = auto.WindowControl(Name="JianyingPro",searchDepth=1)
    if jy_main.TextControl(Name="HomePageStartProjectName",searchDepth=1).Exists(maxSearchSeconds=timeout_seconds): return 0
    if classname_include(WindowObj=jy_main,SubControlType="WindowControl",ClassName="LoadingWindow"): return 2
    if jy_main.GroupControl(Name="MainWindowTitleBarExportBtn",searchDepth=1).Exists(maxSearchSeconds=timeout_seconds): return 1
    else: return -1

def Restart_Client(isReopen:bool=True):
    def start_Jy(): return subprocess.Popen(CONFIG["JianYing_Exe_Path"],shell=True)
    """
        重启剪映客户端
            isClearTmp : 是否清理缓存
            isReopen: 是否重新启动
    """
    subprocess.Popen('%s%s' % ("taskkill /F /T /IM ","JianYingPro.exe"),stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).communicate()
    while Locate_Status() != -1:...
    if isReopen: 
        _thread.start_new_thread(start_Jy,())
    else: return
    while Locate_Status() != -1:...

def into_Main_Window():
    """
        选择草稿的界面,尝试进入主界面
    """
    Intro_window = auto.WindowControl(Name="JianyingPro",searchDepth=1)
    Intro_window.SetTopmost(True)
    Intro_window.GroupControl(Name="HomePageDraft",searchDepth=1).Click()
    while Locate_Status() !=1:
        if Locate_Status() == 1:return

def Single_Operation(media_path:str,media_name:str)->int:
    """
        单次操作
            
        把单个操作分为三部分
            第一部分: 导入媒体文件 --- stage1
            第二部分: 尝试识别字幕并提取 --- stage2
            第三部分: 删除媒体文件 --- stage3
        
        返回值:
            0: 成功
            exception: 失败
    """
    while Locate_Status() !=1:
        Restart_Client()
        into_Main_Window()
    #### 定义一些Position
    Main_Window = auto.WindowControl(Name="JianyingPro", searchDepth=1)
    Main_Window.ShowWindow(3,waitTime=CONFIG["Delay_Times"])
    Main_Window.SetTopmost(True)
    Main_Window.SetTopmost(False)
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
        while not classname_include(WindowObj=Main_Window,SubControlType="WindowObj"):... #Fix issue 8
        while not Main_Window.WindowControl(searchDepth=1).Exists(searchIntervalSeconds=0.5): time.sleep(0.5) # Wait Unitl Media Window Loadded Out
        # Fix issue 10
        Media_Window = Main_Window.WindowControl(searchDepth=1) # 媒体选择框
        Title_x = Media_Window.TitleBarControl(searchDepth=1).BoundingRectangle.left
        Title_width = Media_Window.TitleBarControl(searchDepth=1).BoundingRectangle.width()
        Title_bottom = Media_Window.TitleBarControl(searchDepth=1).BoundingRectangle.bottom
        Content_Window_top = Media_Window.PaneControl(ClassName="DUIViewWndClassName",searchDepth=1).BoundingRectangle.top
        auto.Click(x=int(Title_x+Title_width*3/5),y=int((Title_bottom+Content_Window_top)/2),waitTime=CONFIG["Delay_Times"])#点击路径选择框
        auto.SendKeys(media_path)
        auto.PressKey(13)#按下回车键
        Media_Window.PaneControl(searchDepth=1,foundIndex=classname_include(WindowObj=Media_Window,SubControlType="PaneControl",ClassName="ComboBox")).SendKeys(media_name)
        #点击文件筐输入
        #Media_Window.ButtonControl(searchDepth=1).Click()#打开媒体
        #auto.SendKeys("{Alt}O",waitTime=CONFIG["Delay_Times"])#按下回车键
        auto.SendKeys("{Enter}")#按下回车键
        time.sleep(CONFIG["Delay_Times"]*2)
        auto.MoveTo(x=Media_Item[0],y=Media_Item[1],waitTime=CONFIG["Delay_Times"]) # 防止元素没加载完成就拖动导致的文件无法选中
        auto.DragDrop(x1=Media_Item[0],y1=Media_Item[1],x2=Buttom_Half_Window_Position.xcenter(),y2=Buttom_Half_Window_Position.ycenter(),waitTime=CONFIG["Delay_Times"]*2)

    def srt_identify():
        """
            尝试识别字幕
        """
        Text_Button.Click()
        #点击默认的新建文本以收回默认展开
        if classname_include(WindowObj=Top_Half_Window,SubControlType="TextControl",Name="收藏"):
            Top_Half_Window.TextControl(searchDepth=1,foundIndex=classname_include(WindowObj=Top_Half_Window,SubControlType="TextControl",Name="新建文本")).Click()
        #点击智能字幕\
        try:
            last_time = os.path.getmtime(CONFIG["draft_content_directory"])
        except:...
        Top_Half_Window.TextControl(searchDepth=1,foundIndex=classname_include(WindowObj=Top_Half_Window,SubControlType="TextControl",Name="智能字幕")).Click(waitTime=CONFIG["Delay_Times"]*2) # 增加了等待时间,防止点击时文件还没加载完成
        Unkown_Button = Top_Half_Window.TextControl(searchDepth=1,foundIndex=classname_include(WindowObj=Top_Half_Window,SubControlType="TextControl",Name="识别歌词")).BoundingRectangle
        auto.Click(x=int(Unkown_Button.xcenter()+Unkown_Button.width()*2),y=int(Unkown_Button.bottom),waitTime=CONFIG["Delay_Times"])
        auto.Click(x=int(Unkown_Button.xcenter()+Unkown_Button.width()*2),y=int(Unkown_Button.bottom+Unkown_Button.height()*2),waitTime=CONFIG["Delay_Times"])
        os.system("echo Waiting For Srt Recognition Finished")
        action_start_time = time.time()
        if os.path.exists(CONFIG["draft_content_directory"]):
            #last_time = os.path.getmtime(CONFIG["draft_content_directory"])
            while os.path.getmtime(CONFIG["draft_content_directory"]) == last_time:...
        else:
            while os.path.exists(CONFIG["draft_content_directory"]) == False:...

        os.system("echo Srt Recognition Finished with {} Seconds.".format(str(int(time.time()-action_start_time))))
        while Locate_Status() == 2: ...
        tracks = draft_content.read_draft_content_src(CONFIG["draft_content_directory"])
        if __name__ == "__main__":
            path = ""
        else:
            path = "./components/tmp/"
        with open(path+'.'.join(media_name.split(".")[:-1])+".srt", 'w', encoding='utf-8') as f:  f.write(simple_srt.tracks_to_srt_string(tracks))

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

    add_item()
    srt_identify()
    delete_media()
    Main_Window.SetTopmost(False) #释放置顶锁 
    return 0

def Multi_Video_Process(video_path:str=os.path.abspath(CONFIG["Video_Path"])):
    video_path = os.path.abspath(video_path)
    media_list = [fn for fn in os.listdir(video_path) if any(fn.endswith(format) for format in ['.mp4','.avi','.mkv','.mov','.flv'])]
    for item in media_list:
        m4a_name = item.split('.')[0]+".m4a"
        subprocess.Popen(f'ffmpeg -y -i "{video_path}/{item}" -vn -codec copy "{video_path}/{m4a_name}"',shell=True,
            stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL).wait()
        os.system(f"echo Start Processing {m4a_name}")
        result = Single_Operation(media_path=video_path,media_name=m4a_name)
        if result == 0: os.system(f"echo {m4a_name} Success")
        Restart_Client(True)
        if CONFIG["webhook"] : requests.post(CONFIG["webhook_url"],headers={"User-Agent":"JySrtParser"},json={"content":f"{m4a_name} Success","time":time.time()})
        
    Restart_Client(False)

if __name__ == "__main__":
    from srtParser import draft_content as draft_content
    from srtParser import simple_srt as simple_srt
    Restart_Client(True)
else:
    from components.srtParser import draft_content as draft_content
    from components.srtParser import simple_srt as simple_srt
