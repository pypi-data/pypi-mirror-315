"""
企业微信开发者中心

    https://developer.work.weixin.qq.com/
    https://developer.work.weixin.qq.com/document/path/90313 (全局错误码)

参考文档:

    https://www.gaoyuanqi.cn/python-yingyong-qiyewx/
    https://www.jianshu.com/p/020709b130d3
"""
import json
import time

import requests
from loguru import logger

from . import utils


class QYWX:
    """企业微信"""

    url_prefix = "https://qyapi.weixin.qq.com"
    work_id: str | None = None
    agent_id: str | None = None
    agent_secret: str | None = None
    access_token: str | None = None

    def __init__(self, work_id: str | None, agent_id: str | None, agent_secret: str | None):
        """Initiation"""
        self.work_id = work_id
        self.agent_id = agent_id
        self.agent_secret = agent_secret

        """获取 Token"""
        self.getaccess_token()

    def getaccess_token(self) -> str | None:
        try:
            response = requests.get(f"{self.url_prefix}/cgi-bin/gettoken?corpid={self.work_id}&corpsecret={self.agent_secret}", timeout=10)
            if response.status_code == 200:
                result: dict = response.json()
                self.access_token = result.get('access_token')
            else:
                self.access_token = None
            return result.get('access_token')
        except Exception as e:
            logger.exception(e)
            return None

    def get_agent_list(self) -> dict | str | None:
        try:
            if self.access_token is None:
                self.getaccess_token()
            response = requests.get(f"{self.url_prefix}/cgi-bin/agent/list?access_token={self.access_token}", timeout=10)
            if response.status_code == 200:
                response_data: dict = response.json()
                if response_data.get('errcode') == 42001:
                    self.getaccess_token()
                    time.sleep(1)
                    self.get_agent_list()
                return response_data
            return response.text
        except Exception as e:
            logger.exception(e)
            return None

    def get_department_list(self, eid: str | None = None) -> dict | str | None:
        """eid: Enterprise ID"""
        try:
            if self.access_token is None:
                self.getaccess_token()
            response = requests.get(f"{self.url_prefix}/cgi-bin/department/list?access_token={self.access_token}&id={eid}", timeout=10)
            if response.status_code == 200:
                response_data: dict = response.json()
                if response_data.get('errcode') == 42001:
                    self.getaccess_token()
                    time.sleep(1)
                    self.get_department_list(eid)
                return response_data
            return response.text
        except Exception as e:
            logger.exception(e)
            return None

    def get_user_list(self, eid: str | None = None) -> dict | str | None:
        """eid: Enterprise ID"""
        try:
            if self.access_token is None:
                self.getaccess_token()
            response = requests.get(f"{self.url_prefix}/cgi-bin/user/list?access_token={self.access_token}&department_id={eid}", timeout=10)
            if response.status_code == 200:
                response_data: dict = response.json()
                if response_data.get('errcode') == 42001:
                    self.getaccess_token()
                    time.sleep(1)
                    self.get_user_list(eid)
                return response_data
            return response.text
        except Exception as e:
            logger.exception(e)
            return None

    def get_user_id_by_mobile(self, mobile: str | None = None) -> dict | str | None:
        try:
            if self.access_token is None:
                self.getaccess_token()
            json_string = json.dumps({'mobile': mobile})
            response = requests.post(f"{self.url_prefix}/cgi-bin/user/getuserid?access_token={self.access_token}", data=json_string, timeout=10)
            if response.status_code == 200:
                response_data: dict = response.json()
                if response_data.get('errcode') == 42001:
                    self.getaccess_token()
                    time.sleep(1)
                    self.get_user_id_by_mobile(mobile)
                return response_data
            return response.text
        except Exception as e:
            logger.exception(e)
            return None

    def get_user_info(self, eid: str | None = None) -> dict | str | None:
        """eid: Enterprise ID"""
        try:
            if self.access_token is None:
                self.getaccess_token()
            response = requests.get(f"{self.url_prefix}/cgi-bin/user/get?access_token={self.access_token}&userid={eid}", timeout=10)
            if response.status_code == 200:
                response_data: dict = response.json()
                if response_data.get('errcode') == 42001:
                    self.getaccess_token()
                    time.sleep(1)
                    self.get_user_info(eid)
                return response_data
            return response.text
        except Exception as e:
            logger.exception(e)
            return None

    def send_message_by_mobile(self, mobile: str | list, message: str) -> bool:
        """发送消息"""

        # 参考文档:
        # https://developer.work.weixin.qq.com/document/path/90235

        try:
            if self.access_token is None:
                self.getaccess_token()

            users: list = []

            match True:
                case True if utils.v_true(mobile, list):
                    users = mobile
                case True if utils.v_true(mobile, str):
                    users.append(mobile)
                case _:
                    return None

            for user in users:
                user_object = self.get_user_id_by_mobile(user)
                json_dict = {
                    'touser': user_object.get('userid'),
                    'msgtype': 'text',
                    'agentid': self.agent_id,
                    'text': {'content': message},
                    'safe': 0,
                    'enable_id_trans': 0,
                    'enable_duplicate_check': 0,
                    'duplicate_check_interval': 1800
                }
                json_string = json.dumps(json_dict)
                response = requests.post(f"{self.url_prefix}/cgi-bin/message/send?access_token={self.access_token}", data=json_string, timeout=10)
                if response.status_code == 200:
                    response_data: dict = response.json()
                    if response_data.get('errcode') == 42001:
                        self.getaccess_token()
                        time.sleep(1)
                        self.send_message_by_mobile(mobile, message)

            return True

        except Exception as e:
            logger.exception(e)
            return False
