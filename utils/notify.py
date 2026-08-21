import os
import smtplib
from email.mime.text import MIMEText
from typing import Literal

import httpx


class NotificationKit:
    def __init__(self):
        self.email_user: str = os.getenv('EMAIL_USER', '')
        self.email_pass: str = os.getenv('EMAIL_PASS', '')
        self.email_to: str = os.getenv('EMAIL_TO', '')
        self.email_sender: str = os.getenv('EMAIL_SENDER', '')
        self.smtp_server: str = os.getenv('CUSTOM_SMTP_SERVER', '')
        self.pushplus_token = os.getenv('PUSHPLUS_TOKEN')
        self.server_push_key = os.getenv('SERVERPUSHKEY')
        self.dingding_webhook = os.getenv('DINGDING_WEBHOOK')
        self.feishu_webhook = os.getenv('FEISHU_WEBHOOK')
        self.weixin_webhook = os.getenv('WEIXIN_WEBHOOK')
        self.gotify_url = os.getenv('GOTIFY_URL')
        self.gotify_token = os.getenv('GOTIFY_TOKEN')
        gotify_priority_env = os.getenv('GOTIFY_PRIORITY', '9')
        self.gotify_priority = int(gotify_priority_env) if gotify_priority_env.strip() else 9
        self.telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.bark_key = os.getenv('BARK_KEY')
        self.bark_server = os.getenv('BARK_SERVER', 'https://api.day.app')

    def send_email(self, title: str, content: str, msg_type: Literal['text', 'html'] = 'text'):
        if not self.email_user or not self.email_pass or not self.email_to:
            return  # 配置缺失，静默跳过

        sender = self.email_sender if self.email_sender else self.email_user
        mime_subtype = 'plain' if msg_type == 'text' else 'html'
        try:
            msg = MIMEText(content, mime_subtype, 'utf-8')
            msg['From'] = f'AnyRouter Assistant <{sender}>'
            msg['To'] = self.email_to
            msg['Subject'] = title

            smtp_server = self.smtp_server if self.smtp_server else f'smtp.{self.email_user.split("@")[1]}'
            with smtplib.SMTP_SSL(smtp_server, 465) as server:
                server.login(self.email_user, self.email_pass)
                server.send_message(msg)
            print('[Email]: Message push successful!')
        except Exception as e:
            print(f'[Email]: Message push failed! Reason: {e}')

    def send_pushplus(self, title: str, content: str):
        if not self.pushplus_token:
            return
        try:
            data = {'token': self.pushplus_token, 'title': title, 'content': content, 'template': 'html'}
            with httpx.Client(timeout=30.0) as client:
                resp = client.post('http://www.pushplus.plus/send', json=data)
                if resp.status_code != 200 or resp.json().get('code') != 200:
                    print(f'[PushPlus]: Message push failed! Response: {resp.text[:100]}')
                else:
                    print('[PushPlus]: Message push successful!')
        except Exception as e:
            print(f'[PushPlus]: Message push failed! Reason: {e}')

    def send_serverPush(self, title: str, content: str):
        if not self.server_push_key:
            return
        try:
            data = {'title': title, 'desp': content}
            with httpx.Client(timeout=30.0) as client:
                resp = client.post(f'https://sctapi.ftqq.com/{self.server_push_key}.send', json=data)
                if resp.status_code != 200 or resp.json().get('code') != 0:
                    print(f'[Server Push]: Message push failed! Response: {resp.text[:100]}')
                else:
                    print('[Server Push]: Message push successful!')
        except Exception as e:
            print(f'[Server Push]: Message push failed! Reason: {e}')

    def send_dingtalk(self, title: str, content: str):
        if not self.dingding_webhook:
            return
        try:
            data = {'msgtype': 'text', 'text': {'content': f'{title}\n{content}'}}
            with httpx.Client(timeout=30.0) as client:
                resp = client.post(self.dingding_webhook, json=data)
                if resp.status_code != 200 or resp.json().get('errcode') != 0:
                    print(f'[DingTalk]: Message push failed! Response: {resp.text[:100]}')
                else:
                    print('[DingTalk]: Message push successful!')
        except Exception as e:
            print(f'[DingTalk]: Message push failed! Reason: {e}')

    def send_feishu(self, title: str, content: str):
        if not self.feishu_webhook:
            return
        try:
            data = {
                'msg_type': 'interactive',
                'card': {
                    'elements': [{'tag': 'markdown', 'content': content, 'text_align': 'left'}],
                    'header': {'template': 'blue', 'title': {'content': title, 'tag': 'plain_text'}},
                },
            }
            with httpx.Client(timeout=30.0) as client:
                resp = client.post(self.feishu_webhook, json=data)
                if resp.status_code != 200 or resp.json().get('StatusCode') != 0:
                    print(f'[Feishu]: Message push failed! Response: {resp.text[:100]}')
                else:
                    print('[Feishu]: Message push successful!')
        except Exception as e:
            print(f'[Feishu]: Message push failed! Reason: {e}')

    def send_wecom(self, title: str, content: str):
        if not self.weixin_webhook:
            return
        try:
            data = {'msgtype': 'text', 'text': {'content': f'{title}\n{content}'}}
            with httpx.Client(timeout=30.0) as client:
                resp = client.post(self.weixin_webhook, json=data)
                if resp.status_code != 200 or resp.json().get('errcode') != 0:
                    print(f'[WeChat Work]: Message push failed! Response: {resp.text[:100]}')
                else:
                    print('[WeChat Work]: Message push successful!')
        except Exception as e:
            print(f'[WeChat Work]: Message push failed! Reason: {e}')

    def send_gotify(self, title: str, content: str):
        if not self.gotify_url or not self.gotify_token:
            return
        try:
            priority = max(1, min(10, self.gotify_priority))
            data = {'title': title, 'message': content, 'priority': priority}
            url = f'{self.gotify_url}?token={self.gotify_token}'
            with httpx.Client(timeout=30.0) as client:
                resp = client.post(url, json=data)
                if resp.status_code != 200:
                    print(f'[Gotify]: Message push failed! Response: {resp.text[:100]}')
                else:
                    print('[Gotify]: Message push successful!')
        except Exception as e:
            print(f'[Gotify]: Message push failed! Reason: {e}')

    def send_telegram(self, title: str, content: str):
        if not self.telegram_bot_token or not self.telegram_chat_id:
            return
        try:
            message = f'<b>{title}</b>\n\n{content}'
            data = {'chat_id': self.telegram_chat_id, 'text': message, 'parse_mode': 'HTML'}
            url = f'https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage'
            with httpx.Client(timeout=30.0) as client:
                resp = client.post(url, json=data)
                if resp.status_code != 200 or not resp.json().get('ok'):
                    print(f'[Telegram]: Message push failed! Response: {resp.text[:100]}')
                else:
                    print('[Telegram]: Message push successful!')
        except Exception as e:
            print(f'[Telegram]: Message push failed! Reason: {e}')

    def send_bark(self, title: str, content: str):
        if not self.bark_key:
            return
        try:
            url = f'{self.bark_server.rstrip("/")}/push'
            data = {
                'device_key': self.bark_key,
                'title': title,
                'body': content,
                'icon': 'https://anyrouter.top/favicon.ico',
                'group': 'AnyRouter',
            }
            with httpx.Client(timeout=30.0) as client:
                resp = client.post(url, json=data)
                if resp.status_code != 200 or resp.json().get('code') != 200:
                    print(f'[Bark]: Message push failed! Response: {resp.text[:100]}')
                else:
                    print('[Bark]: Message push successful!')
        except Exception as e:
            print(f'[Bark]: Message push failed! Reason: {e}')

    def push_message(self, title: str, content: str, msg_type: Literal['text', 'html'] = 'text'):
        """统一推送入口，依次调用各渠道，各方法内部自行处理配置缺失和结果输出"""
        self.send_email(title, content, msg_type)
        self.send_pushplus(title, content)
        self.send_serverPush(title, content)
        self.send_dingtalk(title, content)
        self.send_feishu(title, content)
        self.send_wecom(title, content)
        self.send_gotify(title, content)
        self.send_telegram(title, content)
        self.send_bark(title, content)


notify = NotificationKit()
