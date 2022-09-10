from JianYingApi import JianYingApi as Api
if __name__ == "__main__":
    _a = Api.Jy_Warp.Instance(Start_Jy=False)
    print(_a._close_advertise(advertise_type=1))