import os , subprocess
class Media_Type:
    def __init__(self,path:os.PathLike,filename:str) -> None:
        self.path = path
        self.filename = filename
        self.all = os.path.join(path,filename)
        self.rawname = filename.split(".")[-1]
        self.m4a = self.rawname + ".m4a"

    def to_m4a(self):
        subprocess.run(" ".join([
                        "ffmpeg","-y","-i",f"'{self.all}'","-vn","-codec","copy",f"'{os.path.join(self.path,self.m4a)}'" # n is utils/mediatype.py
                    ]) ,stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL)
        self.hasm4a = True