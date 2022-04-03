class SrtFile:
    # 没有对其他的(格式化、位置进行格式)
    def __init__(self,path):
        self.raw = open(path,"r",encoding="utf-8").read()
        self.Parse_List()

    def Parse_List(self):
        # 把字幕的Raw文件转换为对象
        def to_sec(srt:str):
            sec = 0
            for i in range(len(srt.split(":"))): sec+=int(srt.split(":")[i])*60**(2-i)
            return sec
        def to_milsec(srt:str): 
            return to_sec(srt.split(",")[0])*1000+int(srt.split(",")[1])
        Srt_List = []
        Raw_List = [fn for fn in self.raw.split("\n") if len(fn)>0] # 去除空行
        assert len(Raw_List)%3 == 0,"Length of Srt Error"
        for i in range(0,len(Raw_List),3):
            Srt_List.append({
                "Index":Raw_List[i],
                "Time":{
                    "Start":to_milsec(Raw_List[i+1].split(" --> ")[0]),
                    "End":to_milsec(Raw_List[i+1].split(" --> ")[1])
                },
                "Content":Raw_List[i+2]
            })
        self.Srt_List = Srt_List

    def __str__(self):
        def combine_sec(time:int):
            hour,min,sec,millsec = time//3600000,time//60000%60,time//1000%60,time%1000
            return f"{hour:02d}:{min:02d}:{sec:02d},{millsec:03d}"
        Raw = ""
        for i in self.Srt_List:
            Raw += i["Index"] + "\n" + str(combine_sec(i["Time"]["Start"])) + " --> " + str(combine_sec(i["Time"]["End"])) + "\n" + i["Content"] + "\n\n"
        self.raw = Raw
    
    def plus(self,Other:object):
        this_last_index , this_last_time = self.Srt_List[-1]["Index"], self.Srt_List[-1]["Time"]["End"]
        for i in Other.Srt_List:
            self.Srt_List.append({
                "Index":str(int(i["Index"])+int(this_last_index) +1 ),
                "Time":{
                    "Start":int(i["Time"]["Start"])+int(this_last_time),
                    "End":int(i["Time"]["End"])+int(this_last_time)
                },
                "Content":i["Content"]
            })

if __name__ == "__main__":
    A = SrtFile(r"2-1.srt")
    B = SrtFile(r"2-2.srt")
    A.plus(B)
    A.__str__()
    open("./2.srt","w",encoding="utf-8").write(A.raw)