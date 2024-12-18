# -*- coding: utf-8 -*-

"""
--------------------------------------------
project: zibuyu_wechat
author: 子不语
date: 2024/12/14
contact: 【公众号】思维兵工厂
description: 
--------------------------------------------
"""

import requests

from ..utils.logger import make_logger
from ..apis import OfficialWebApisManager


class WechatWebHandler(object):
    """
    待完善！微信公众号操作类，用于调用微信公众号的web逆向接口
    """

    def __init__(self, cookie_str: str, token: str, is_debug: bool = False):

        self.logger = make_logger(__name__)
        self.cookie_str = cookie_str
        self.token = token
        self.is_debug = is_debug

        self.apis = OfficialWebApisManager()

        self.headers = {
            "authority": "mp.weixin.qq.com",
            "method": "POST",
            "path": f"/advanced/setreplyrule?cgi=setreplyrule&fun=save&t=ajax-response&access_token={self.token}&lang=zh_CN",
            "scheme": "https",
            "sec-ch-ua-platform": "\"Windows\"",
            "x-requested-with": "XMLHttpRequest",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "sec-ch-ua-mobile": "?0",
            "accept": "*/*",
            "origin": "https://mp.weixin.qq.com",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": f"https://mp.weixin.qq.com/advanced/autoreply?action=smartreply&t=ivr/keywords&token={self.token}&lang=zh_CN",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "priority": "u=1, i",
            'cookie': self.cookie_str,
        }

    def set_reply_rule(self, title: str, msg: str) -> bool:
        """
        设置自动回复规则，仅文本，后续需要分析参数，继续优化；

        经测试，仅能设置200个关键词回复规则。

        :param title:
        :param msg:
        :return:
        """

        params = {
            "cgi": "setreplyrule",
            "fun": "save",
            "t": "ajax-response",
            "access_token": self.token,
            "lang": "zh_CN"
        }

        data = {
            "access_token": self.token,
            "lang": "zh_CN",
            "f": "json",
            "ajax": "1",
            "replytype": "smartreply",
            "ruleid": "0",
            "rulename": title,
            "allreply": "0",
            "replycnt": "1",
            "keywordcnt": "1",
            "keyword0": title,
            "matchmode0": "0",
            "type0": "1",
            "fileid0": "undefined",
            "content0": msg
        }

        try:
            response = requests.post(self.apis.set_reply_rule_url, params=params, headers=self.headers, data=data)

            if 'setreplyrule process ok!' in response.text:
                self.is_debug and self.logger.info(f'【{title}】回复关键词创建成功')
                return True

            self.is_debug and self.logger.warning(f'关键字回复创建失败，响应的内容为：【{response.text}】')
        except:
            self.is_debug and self.logger.error(f'设置关键词回复出现未知错误', exc_info=True)

        return False
