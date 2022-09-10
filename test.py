#from JianYingApi import JianYingApi as Api
import uiautomation as api32
if __name__ == "__main__":
   Window = api32.WindowControl(searchDepth=1,Name="JianyingPro")
   Window = api32.WindowControl(searchDepth=1,Name="JianyingPro",foundIndex=Window.foundIndex+1)
   print(Window.ClassName)