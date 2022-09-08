import requests
import logging
def Webhooks(WebhookConf,i,mesage:str):
    def Send(inf):
        try:
            logging.info(f"Trying To Send Webhook To ")
            if inf["Method"] == "POST" : requests.post(inf["Url"],data=mesage)
            if inf["Method"] == "GET": requests.get(inf["Url"],data=mesage)
        except: logging.error(f"Error in Sending Webhook To ... ")
        
    if "Webhooks" in i and i["Webhooks"] != None:
        if i["Webhooks"] == True:
            for k in WebhookConf:
                Send(k)
        if type(i["Webhooks"]) == list:
            for q in i["Webhooks"]:
                Send(WebhookConf[q])