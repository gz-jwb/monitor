#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import sys
import json
import requests


class Sender(object):
    @classmethod
    def send_Phone(cls, payload):
        tpl= payload.get("tpl",{})
        if tpl.get("Phone"):
            phones = payload.get('sendtos',[])
            for p in phones:
                cls.send_voice_to_phone(p)

        # users = payload.get('event').get("notify_users_obj")
        # if users is not None:
        #     for u in users:
        #         if u.get("phone"):
        #             p = u.get("phone")
        #             cls.send_voice_to_phone(p)

        # else: # 旧版配置方式
        #     phones = {}
        #     # 判断下notify_channels是否包含了Phone
        #     if payload.get('event', {}).get('notify_channels') and 'Phone' in payload.get('event', {}).get('notify_channels'):
        #         phones.update({p: 1 for p in payload.get('sendtos', []) if p})
        #     # 调用发送方法
        #     for phone in phones:
        #         cls.send_voice_to_phone(phone)

    @staticmethod
    def send_voice_to_phone(phone):
        """
        发送语音通知到指定手机号，失败时走备份通道
        """
        url = "https://api-v4.mysubmail.com/voice/xsend"
        body = {
            "appid": "22675",
            "signature": "f0e0f8729173a91e3072ec983d923393",
            "to": str(phone),
            "project": "kLUfq2"
        }
        headers = {
            "Content-Type": "application/json",
        }
        response = requests.post(url, headers=headers, data=json.dumps(body))
        print(f"notify_Phone: phone={phone} status_code={response.status_code} response_text={response.text}")
        if response.status_code != 200 or response.json().get("status") != "success":
            print(f"Phone send failed for phone {phone}, trying backup channel")
            backup_url = "https://api.4321.sh/voicenotice/send"
            backup_headers = {
                "Content-Type": "application/json",
            }
            backup_body = {
                "apikey": "VN119649976",
                "secret": "119649cf286985343",
                "mobile": str(phone),
                "template_id": "101389"
            }
            backup_response = requests.post(backup_url, headers=backup_headers, data=json.dumps(backup_body))
            print(f"Backup Phone send status_code={backup_response.status_code} response_text={backup_response.text}")

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