import requests
import logging
def Webhooks(WebhookConf,i,mesage:str):
    if i["Webhooks"] != None:
        if i["Webhooks"] == True:
            for k in WebhookConf:
                try:
                    if k["Method"] == "POST": requests.post(k["Url"],data=mesage)
                    if k["Method"] == "GET": requests.get(k["Url"],data=mesage)
                except: logging.error(f"Error in Sending Webhook To ... ")
        if type(i["Webhooks"]) == list:
            for q in i["Webhooks"]:
                try:
                    if WebhookConf[q]["Method"] == "POST": requests.post(WebhookConf[q]["Url"],data=mesage)
                    if WebhookConf[q]["Method"] == "GET": requests.get(WebhookConf[q]["Url"],data=mesage)
                except: logging.error(f"Error in Sending Webhook To ... ")