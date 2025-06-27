#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import sys
import json
import requests


class Sender(object):
    @classmethod
    def send_Sms(cls, payload):
        tpl= payload.get("tpl",{})
        if tpl.get("Sms"):
            content = payload.get('tpl', {}).get("Sms", "你有新的告警，请及时到监控平台处理！")
            phones = payload.get('sendtos',[])
            for p in phones:
                cls.send_sms_to_phone(p, content)


    @staticmethod
    def send_sms_to_phone(phone, content):
        # submail api
        url = "https://api-v4.mysubmail.com/sms/send"
        body = {
            "appid": "107445",
            "to": str(phone),
            "content": "【漫星云】" + content,
            "signature": "8b7cb5783671c213180c669749a5a70f"
        }
        headers = {
            "Content-Type": "application/json;charset=utf-8",
        }
        response = requests.post(url, headers=headers, data=json.dumps(body))
        print(f"notify_sms: phone={phone} status_code={response.status_code} response_text={response.text}")


        # feige  api
        if response.status_code != 200 or response.json().get("status") != "success":
            print(f"SMS send failed for phone {phone}, trying backup channel")
            backup_url = "https://api.4321.sh/sms/send"
            backup_headers = {
                "Content-Type": "application/json",
            }
            backup_body = {
                "apikey": "N119649cbab",
                "secret": "119649ef11609b08a",
                "content": content,
                "mobile": str(phone),
                "sign_id": "211691"
            }
            backup_response = requests.post(backup_url, headers=backup_headers, data=json.dumps(backup_body))
            print(f"Backup SMS send status_code={backup_response.status_code} response_text={backup_response.text}")





def main():
    payload = json.load(sys.stdin)
    with open(".payload", 'w') as f:
        f.write(json.dumps(payload, indent=4))
    # 优先从 notify_channels 获取
    channels = payload.get('event', {}).get('notify_channels', [])
    
    # 如果 notify_channels 为空，则从 tpl 中提取可用通道
    if not channels:
        channels = [channel for channel in payload.get('tpl', {}).keys()]
    
    for ch in channels:
        send_func_name = "send_{}".format(ch.strip())
        if not hasattr(Sender, send_func_name):
            print("function: {} not found", send_func_name)
            continue
        send_func = getattr(Sender, send_func_name)
        send_func(payload)

def hello():
    print("hello nightingale")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        main()
    elif sys.argv[1] == "hello":
        hello()
    else:
        print("I am confused")