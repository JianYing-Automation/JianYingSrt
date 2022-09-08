from JianYingApi import JianYingApi as Api
_a = Api.Jy_Warp.Instance(Start_Jy=False)
while True:
    print(_a._detect_viewport())
