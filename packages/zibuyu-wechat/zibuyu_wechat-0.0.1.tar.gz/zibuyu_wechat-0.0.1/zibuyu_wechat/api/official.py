# -*- coding: utf-8 -*-

"""
--------------------------------------------
project: zibuyu_wechat
author: 子不语
date: 2024/11/15
contact: 【公众号】思维兵工厂
description: 公众号操作SDK，未完成
--------------------------------------------
"""

import os
import time
import json
import logging
import requests
from typing import Tuple, Union

from ..utils.logger import make_logger
from ..error import TokenError, ParamsTypeError, error_dict
from ..apis import OfficialApisManager
from ..types import *


class BaseHandler(object):
    """
    微信公众号操作类，用于调用微信公众号的官方接口
    """

    def __init__(
            self,
            app_id: str,
            app_secret: str,
            access_token: str = None,
            token_expires_in: int = 0,
            logger: logging.Logger = None,
            is_debug: bool = True,
    ):

        # 设置日志记录器
        if not logger or not isinstance(logger, logging.Logger):
            logger = make_logger()
        self.logger = logger

        self.logger.info("初始化微信公众号操作类")

        self.app_id = app_id
        self.app_secret = app_secret
        self.is_debug = is_debug

        # 相关请求所需的access_token
        self._access_token = access_token

        # access_token的有效期：时间戳，整型
        self.token_expires_in = token_expires_in

        self.apis = OfficialApisManager()

        self.error_code: int = 0  # 错误码，为0时表示无错误
        self.error_msg: str = ""  # 错误信息
        self.suggest: str = ""  # 建议信息

    def reset_request_msg(self):
        self.error_code: int = 0  # 错误码，为0时表示无错误
        self.error_msg: str = ""  # 错误信息
        self.suggest: str = ""  # 建议信息

    def _post(
            self,
            url: str,
            params: dict = None,
            data: [dict, bytes] = None,
            headers: dict = None,
            files=None,
            has_json: bool = False
    ) -> dict:
        """
        发送post请求，出现错误时重试两次
        :param url: 请求的url
        :param params: 请求的参数
        :param data: 请求的data
        :param headers: 请求的headers
        :param files: 传输的文件
        :param has_json: 请求数据是否已经json处理
        :return: 返回的json数据
        """

        if not params:
            params = self.params

        for i in range(3):
            self.reset_request_msg()

            try:
                if has_json:
                    response = requests.post(url, params=params, data=data, headers=headers, files=files)
                else:
                    response = requests.post(url, params=params, json=data, headers=headers, files=files)

                #  这里必须自行解码，使用response.json()会出错，原因未知
                result = json.loads(response.content.decode('utf8'))

                self.error_code = result.get('errcode')
                self.error_msg = result.get('errmsg')
                self.suggest = error_dict.get(self.error_code)

                return result
            except:
                self.is_debug and self.logger.error(
                    f"发送 post 请求时出错! \nurl：{url}, \nparams：{params}, \ndata：{data}, \nheaders：{headers}",
                    exc_info=True
                )
            self.is_debug and self.logger.info(f"发送 post 请求时出错，即将重试")

    def _get(self, url: str, params: dict = None, headers: dict = None) -> dict:
        """
        发送get请求，出现错误时重试两次
        :param url: 请求的url
        :param params: 请求的参数
        :param headers: 请求的headers
        :return: 返回的json数据
        """

        if not params:
            params = self.params

        for i in range(3):
            self.reset_request_msg()

            try:
                response = requests.get(url, params=params, headers=headers)

                #  这里必须自行解码，使用response.json()会出错，原因未知
                result = json.loads(response.content.decode('utf8'))

                self.error_code = result.get('errcode')
                self.error_msg = result.get('errmsg')
                self.suggest = error_dict.get(self.error_code)

                return result
            except:
                self.is_debug and self.logger.error(
                    f"发送 get 请求时出错! \nurl：{url}, \nparams：{params}, \nheaders：{headers}",
                    exc_info=True
                )
            self.is_debug and self.logger.error(f"发送 get 请求时出错，即将重试")

    def clear_quota(self) -> bool:
        """
        清空公众号 |小程序 |第三方平台等接口的每日调用接口次数。
        每个账号每月共10次清零操作机会，清零生效一次即用掉一次机会
        :return: bool，清空成功返回True，否则返回False
        """

        data = {'appid': self.app_id}

        result = self._post(self.apis.clear_quota_url, data=data)

        if result.get('errcode') == 0:
            return True

        return False

    def get_token(self):
        """
        微信的接口鉴权token，有效期为两小时
        可以本地保存token，有效期内不用反复获取
        :return:
        """

        # 检验本地存储的access_token，仍然有效则直接返回
        now_timestamp = int(time.time())
        if self._access_token and self.token_expires_in > now_timestamp:
            return self._access_token

        params = {'grant_type': 'client_credential', 'appid': self.app_id, 'secret': self.app_secret}

        result = self._get(self.apis.token_url, params=params)

        if not result:
            raise TokenError("获取token失败")

        self._access_token = result.get('access_token')

        if not self._access_token:
            self.is_debug and self.logger.error(f"获取token失败，返回结果为：{result}")
            self.is_debug and self.logger.info(self.suggest)
            raise TokenError("获取token失败")

        # 官方设置access_token的有效期为7200秒，这里为确保其有效性，取整处理
        self.token_expires_in = now_timestamp + 7000

        return self._access_token

    def get_keyword(self) -> Optional[WechatOfficialKeyword]:
        """获取公众号目前设置的关键字回复"""

        result = self._get(self.apis.get_keyword_url)

        if not result:
            return None

        obj = WechatOfficialKeyword(
            is_add_friend_reply=bool(result.get('is_add_friend_reply_open')),
            is_auto_reply=bool(result.get('is_autoreply_open')),
            add_friend_reply_content=result.get('add_friend_autoreply_info', {}).get('content'),
            add_friend_reply_type=result.get('add_friend_autoreply_info', {}).get('type'),
            keyword_reply_info_list=[
                KeywordInfo(
                    rule_name=reply_info_dict.get('rule_name'),
                    create_time=reply_info_dict.get('create_time'),
                    reply_mode=reply_info_dict.get('reply_mode'),
                    keyword_list=[
                        Keyword(
                            keyword_type=k.get('type'),
                            match_mode=k.get('match_mode'),
                            content=k.get('content'),
                        ) for k in reply_info_dict.get('keyword_list_info')
                    ],
                    reply_list=[
                        Reply(
                            reply_type=j.get('type'),
                            content=j.get('content'),
                            news_info=j.get('news_info'),
                            title=j.get('title'),
                            digest=j.get('digest'),
                            author=j.get('author'),
                            show_cover=j.get('show_cover'),
                            cover_url=j.get('cover_url'),
                            content_url=j.get('content_url'),
                            source_url=j.get('source_url'),
                        ) for j in reply_info_dict.get('reply_list_info')
                    ]
                ) for reply_info_dict in result.get('keyword_autoreply_info', {}).get('list')
            ] if result.get('keyword_autoreply_info') else []
        )

        return obj

    @property
    def params(self):
        return {"access_token": self.access_token, }

    @property
    def access_token(self):
        """
        检验本地存储的access_token，仍然有效则直接返回
        :return: access_token
        """
        now_timestamp = int(time.time())
        if self._access_token and self.token_expires_in > now_timestamp:
            return self._access_token

        return self.get_token()


class CustomService(BaseHandler):
    """客服相关操作"""

    def get_msg_record(self):
        """
        获取消息记录；待完成！
        :return:
        """

        now = int(time.time())
        yesterday = now - 86000
        data = {
            "starttime": yesterday,
            "endtime": now,
            "msgid": 1,
            "number": 10000,
        }

        response = self._post(self.apis.msg_record_url, data=data)
        print(response)


class CheckQuote(BaseHandler):
    """查询接口调用次数"""

    def __check_quota(self, uri: str):
        """检查公众号接口调用次数"""
        result = self._post(self.apis.check_quota_url, data={"cgi_path": uri, })
        print(result)

        result_obj = QuotaResult(
            daily_limit=result.get("quota", {}).get('daily_limit'),
            used=result.get("quota", {}).get('used'),
            remain=result.get("quota", {}).get('remain'),
        )

        return result_obj

    def check_quota_get_keyword(self):
        """检查自动回复规则查询接口的调用次数"""
        return self.__check_quota(self.apis.get_menu_uri)

    def check_quota_soft_src_upload(self):
        """检查上传临时素材接口的调用次数"""
        return self.__check_quota(self.apis.soft_src_upload_uri)

    def check_quota_soft_src_download(self):
        """检查下载临时素材接口的调用次数"""
        return self.__check_quota(self.apis.soft_src_download_uri)

    def check_quota_hard_img_upload(self):
        """检查上传图文消息内的图片获取URL接口的调用次数"""
        return self.__check_quota(self.apis.hard_img_upload_uri)

    def check_quota_hard_src_upload(self):
        """检查上传其他类型永久素材接口的调用次数"""
        return self.__check_quota(self.apis.hard_src_upload_uri)

    def check_quota_hard_src_download(self):
        """检查下载永久素材接口的调用次数"""
        return self.__check_quota(self.apis.hard_src_download_uri)

    def check_quota_hard_src_delete(self):
        """检查删除永久素材接口的调用次数"""
        return self.__check_quota(self.apis.hard_src_delete_uri)

    def check_quota_hard_src_count(self):
        """检查获取永久素材的各类总数列表接口的调用次数"""
        return self.__check_quota(self.apis.hard_src_count_uri)

    def check_quota_hard_src_list(self):
        """检查获取永久素材的列表接口的调用次数"""
        return self.__check_quota(self.apis.hard_src_list_uri)

    def check_quota_get_menu(self):
        """检查查询当前菜单接口的调用次数"""
        return self.__check_quota(self.apis.get_menu_uri)

    def check_quota_create_menu(self):
        """检查创建菜单接口的调用次数"""
        return self.__check_quota(self.apis.create_menu_uri)

    def check_quota_delete_menu(self):
        """检查删除菜单接口的调用次数"""
        return self.__check_quota(self.apis.delete_menu_uri)

    def check_quota_create_draft(self):
        """检查新建素材接口的调用次数"""
        return self.__check_quota(self.apis.create_draft_uri)

    def check_quota_get_draft(self):
        """检查获取素材接口的调用次数"""
        return self.__check_quota(self.apis.get_draft_uri)

    def check_quota_delete_draft(self):
        """检查删除素材接口的调用次数"""
        return self.__check_quota(self.apis.delete_draft_uri)

    def check_quota_update_draft(self):
        """检查修改素材接口的调用次数"""
        return self.__check_quota(self.apis.update_draft_uri)

    def check_quota_get_draft_count(self):
        """检查获取素材总数接口的调用次数"""
        return self.__check_quota(self.apis.get_draft_count_uri)

    def check_quota_get_draft_list(self):
        """检查获取素材列表接口的调用次数"""
        return self.__check_quota(self.apis.get_draft_list_uri)

    def check_quota_clear_quota(self):
        """检查清空api的调用quota接口的调用次数"""
        return self.__check_quota(self.apis.clear_quota_uri)

    def check_quota_check_quota(self):
        """检查查询api接口的每日调用额度和调用次数接口的调用次数"""
        return self.__check_quota(self.apis.check_quota_uri)

    def check_quota_publish_news(self):
        """检查发布草稿接口的调用次数"""
        return self.__check_quota(self.apis.publish_news_uri)

    def check_quota_publish_status(self):
        """检查查询发布状态接口的调用次数"""
        return self.__check_quota(self.apis.publish_status_uri)

    def check_quota_article_list(self):
        """检查获取已发布图文列表接口的调用次数"""
        return self.__check_quota(self.apis.article_list_uri)

    def check_quota_get_article(self):
        """检查获取已发布的图文接口的调用次数"""
        return self.__check_quota(self.apis.get_article_uri)

    def check_quota_voice_to_text(self):
        """检查智能接口-语音转文本接口的调用次数"""
        return self.__check_quota(self.apis.voice_to_text_uri)


class SourceHandler(BaseHandler):

    def check_file_requirements(
            self,
            file_path: str,
            file_type: Literal["image", "voice", "video", "thumb"]
    ) -> Tuple[bool, str]:
        """
        检查文件是否符合要求
        :param file_path: 文件路径
        :param file_type: 文件类型
        :return:
        """

        # 检查文件是否存在
        if not os.path.exists(file_path):
            return False, "文件不存在"

        # 获取文件大小（以字节为单位）
        file_size_bytes = os.path.getsize(file_path)

        # 获取文件扩展名
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        # 将文件大小转换为MB，并保留两位小数
        file_size_mb = file_size_bytes / (1024 * 1024)

        # 根据文件类型检查要求
        if file_type == "image":
            # 图片要求：不超过10MB
            max_size_mb = 10
            max_size_str = f"{max_size_mb}M"

            if ext not in ['.png', '.jpeg', '.jpg', '.gif']:
                return False, "不支持的文件类型；image 类型只支持 png, jpeg, jpg, gif 格式"

        elif file_type == "voice":
            # 语音要求：不超过2MB，播放长度不超过60s
            max_size_mb = 2
            max_size_str = f"{max_size_mb}M"

            if ext not in ['.amr', '.mp3']:
                return False, "不支持的文件类型；voice 类型只支持 amr, mp3 格式"

        elif file_type == "video":
            # 视频要求：不超过10MB
            max_size_mb = 10
            max_size_str = f"{max_size_mb}M"

            if ext not in ['.mp4']:
                return False, "不支持的文件类型；video 类型只支持 mp4 格式"

        elif file_type == "thumb":
            # 缩略图要求：不超过64KB，转换为MB
            max_size_kb = 64
            max_size_mb = max_size_kb / 1024
            max_size_str = f"{max_size_kb}KB"

            if ext not in ['.jpg', ]:
                return False, "不支持的文件类型；thumb 类型只支持 jpg 格式"

        else:
            return False, "不支持的文件类型"

        # 检查文件大小
        if file_size_mb > max_size_mb:
            return False, f"文件超过{max_size_str}"

        # TODO 待完善后再开启 -> 特殊检查：语音文件播放长度
        # if file_type == "voice":
        #     try:
        #         from pydub import AudioSegment
        #         audio = AudioSegment.from_file(file_path)
        #         if len(audio) > 60 * 1000:  # 60秒
        #             return False, "语音播放长度超过60秒"
        #     except ModuleNotFoundError:
        #         self.is_debug and self.logger.info("未安装依赖包：pydub；跳过检查")
        #         pass
        #     except Exception as e:
        #         return False, f"检查语音文件时长时出错：{e}"

        return True, "文件符合要求"

    def upload_source(
            self,
            file_type: Literal["image", "voice", "video", "thumb"],
            file_path: str,
            source_type: Literal["soft", "hard", "other"] = "soft"
    ):
        """
        公共方法：用于上传临时素材或永久素材
        :param file_type:素材类别：image、voice、video、thumb（缩略图）等
        :param file_path:所上传文件的路径，用于读取文件
        :param source_type:永久素材hard或临时素材soft；另加一个other（上传图文消息内的图片获取URL，不占用永久素材额度的接口）
        :return:
        """

        check_result, check_msg = self.check_file_requirements(file_path, file_type)
        if not check_result:
            raise ParamsTypeError(f"文件不符合要求：【{check_msg}】")

        if source_type == "soft":
            url = self.apis.soft_src_upload_url
        elif source_type == "hard":
            url = self.apis.hard_src_upload_url
        elif file_type == 'image' and source_type == "other":
            url = self.apis.hard_src_upload_url
        else:
            raise ParamsTypeError('素材类型传入错误。\n临时素材source_type=soft\n永久素材source_type=hard')

        params = {'access_token': self.access_token, 'type': file_type, 'media': ''}

        with open(file_path, "rb") as f:
            files = {"media": f}
            return self._post(url, params=params, files=files)

    def upload_soft_source(
            self,
            file_path: str,
            file_type: Literal["image", "voice", "video", "thumb"] = "image",
    ) -> Optional[CommonItem]:
        """
        上传临时素材，
        临时素材的有效期是3天
        注意，各类素材的大小有要求：
            图片（image）: 10M，支持PNG|JPEG|JPG|GIF格式
            语音（voice）：2M，播放长度不超过60s，支持AMR|MP3格式
            视频（video）：10MB，支持MP4格式
            缩略图（thumb）：64KB，支持JPG格式
        :param file_type:
        :param file_path:
        :return:
        """
        result = self.upload_source(file_type=file_type, file_path=file_path, source_type='soft')

        media_id = result.get('media_id')

        if not media_id:
            self.is_debug and self.logger.error(
                f"上传图片失败；错误信息：\n错误码：{self.error_code}；\n错误信息：{self.error_msg}")
            return

        return CommonItem(
            media_id=media_id,
            url=result.get('url'),
            update_time=result.get('created_at'),
        )

    def upload_hard_source(
            self,
            file_path: str,
            file_type: Literal["image", "voice", "video", "thumb"] = "image",
    ) -> Optional[CommonItem]:
        """
        上传永久素材。待完善，需要添加文件大小判断
        总数量有上限：图文消息素材、图片素材上限为100000，其他类型为1000。
        注意，各类素材的大小有要求：
            图片（image）: 10M，支持PNG|JPEG|JPG|GIF格式
            语音（voice）：2M，播放长度不超过60s，支持AMR|MP3格式
            视频（video）：10MB，支持MP4格式
            缩略图（thumb）：64KB，支持JPG格式
        :param file_type:
        :param file_path:
        :return:
        """

        result = self.upload_source(file_type=file_type, file_path=file_path, source_type='hard')

        media_id = result.get('media_id')

        if not media_id:
            self.is_debug and self.logger.error(
                f"上传图片失败；错误信息：\n错误码：{self.error_code}；\n错误信息：{self.error_msg}")
            return

        return CommonItem(
            media_id=media_id,
            url=result.get('url'),
            update_time=result.get('created_at'),
        )

    def upload_img_get_url(self, file_path: str) -> Optional[CommonItem]:

        """
        上传图文消息内的图片获取URL
        本接口所上传的图片不占用公众号的素材库中图片数量的100000个的限制。
        图片仅支持jpg/png格式，大小必须在1MB以下。
        :param file_path: 上传图片所在路径
        :return:
        """

        result = self.upload_source(file_type='image', file_path=file_path, source_type='other')

        media_id = result.get('media_id')
        url = result.get('url')

        if not media_id or not url:
            self.is_debug and self.logger.error(
                f"上传图片失败；错误信息：\n错误码：{self.error_code}；\n错误信息：{self.error_msg}")
            return

        obj = CommonItem(
            media_id=media_id,
            url=url
        )

        return obj

    def download_source(
            self,
            media_id: str,
            file_dir,
            source_type: Literal["soft", "hard", "other"] = "soft"
    ) -> str:
        """
        公共方法，用于下载临时素材或永久素材：
            1. 如果该临时素材是视频，返回结果为json：
                { "video_url":DOWN_URL }
            2. 永久素材比临时素材多了一个类型：图文素材。返回结果为json：
                {
                     "news_item":
                     [
                         {
                         "title":TITLE,  # 图文消息的标题
                         "thumb_media_id":THUMB_MEDIA_ID,  # 图文消息的封面图片素材id（必须是永久mediaID）
                         "show_cover_pic":SHOW_COVER_PIC(0/1),  # 是否显示封面，0为false，即不显示，1为true，即显示
                         "author":AUTHOR,  # 作者
                         "digest":DIGEST,  # 图文消息的摘要，仅有单图文消息才有摘要，多图文此处为空
                         "content":CONTENT,  # 图文消息的具体内容，支持HTML标签，必须少于2万字符，小于1M，且此处会去除JS
                         "url":URL,  # 图文页的URL
                         "content_source_url":CONTENT_SOURCE_URL  # 图文消息的原文地址，即点击“阅读原文”后的URL
                         },
                        # 多图文消息有多篇文章
                      ]
                }
            3. 其他类型的临时素材，返回该素材本身内容，可直接以二进制方式写入文件；
            4. 错误情况下，返回：
                { "errcode":40007,"errmsg":"invalid media_id" }

            5. 该请求的返回头中携带素材类型信息，可通过请求头中的信息判断素材类型、获取文件名称：
                HTTP/1.1 200 OK
                Connection: close
                Content-Type: voice/speex
                Content-disposition: attachment; filename="MEDIA_ID.speex"
                Date: Sun, 06 Jan 2016 10:20:18 GMT
                Cache-Control: no-cache, must-revalidate
                Content-Length: 339721
                curl -G "https://api.weixin.qq.com/cgi-bin/media/get/jssdk?access_token=ACCESS_TOKEN&media_id=MEDIA_ID"
        :param media_id:
        :param file_dir:  素材下载后的存放目录
        :param source_type:
        :return:
        """

        if source_type == "soft":
            url = self.apis.soft_src_download_url
        elif source_type == "hard":
            url = self.apis.hard_src_download_url
        else:
            raise Exception('素材类型传入错误。\n临时素材source_type=soft\n永久素材source_type=hard')

        params = {'access_token': self.access_token, 'media_id': media_id}
        response = requests.get(url, params=params)
        file_name = response.headers.get('filename')
        file_path = file_dir / file_name

        with open(file_path, mode='wb') as wf:
            wf.write(response.content)
        return file_path

    def download_soft_source(self, media_id: str, file_dir) -> str:
        """
        下载临时素材
        :param media_id:
        :param file_dir:
        :return:成功时返回文件路径，失败返回None
        """
        return self.download_source(media_id, file_dir)

    def download_hard_source(self, media_id: str, file_dir) -> str:
        """
        下载永久素材
        :param media_id:
        :param file_dir:
        :return:成功时返回文件路径，失败返回None
        """
        return self.download_source(media_id, file_dir, source_type='hard')

    def delete_hard_src(self, media_id: str) -> bool:
        """
        删除永久素材，放回：{ "errcode":ERRCODE, "errmsg":ERRMSG }
        其中，成功删除时，errcode=0
        :param media_id:
        :return:
        """

        data = {'media_id': media_id}
        self._post(self.apis.hard_src_delete_url, data=data)
        if self.error_code == 0:
            self.is_debug and self.logger.info(f'删除永久素材成功！media_id:{media_id}')
            return True
        self.is_debug and self.logger.error(f'删除永久素材失败！\n错误码：{self.error_code}；\n错误信息：{self.error_msg}')
        return False

    def get_source_count(self) -> SourceCount:
        """
        获取永久素材各类型的数量。
        数据格式：
            {'voice_count': 0, 'video_count': 0, 'image_count': 0, 'news_count': 0}
        :return:
        """
        result = self._get(self.apis.hard_src_count_url)
        return SourceCount(**result) if result else None

    def get_source_list(
            self,
            src_type: Literal['image', 'video', 'voice', 'news'] = 'image',
            offset: int = 0,
            count: int = 20
    ) -> Union[SourceNewsItemList, SourceCommonItemList]:
        """
        获取永久素材列表
        :param src_type:素材的类型，图片（image）、视频（video）、语音 （voice）、图文（news）
        :param offset:从全部素材的该偏移位置开始返回，0表示从第一个素材 返回
        :param count:返回素材的数量，取值在1到20之间
        :return:
        """

        if src_type not in ['image', 'video', 'voice', 'news']:
            raise ValueError("src_type must be 'image' or 'video' or 'voice' or 'news'")

        data = {"type": src_type, "offset": offset, "count": count}

        result = self._post(self.apis.hard_src_list_url, data=data)

        if src_type in ['image', 'video', 'voice']:
            obj = SourceCommonItemList(
                type=src_type,
                total_count=result.get('total_count'),
                item_count=result.get('item_count'),
                item_list=[
                    CommonItem(
                        media_id=item.get('media_id'),
                        name=item.get('name'),
                        update_time=item.get('update_time'),
                        url=item.get('url'),
                        tags='；'.join(item.get('tags') if item.get('tags') else []),
                    ) for item in result.get('item')
                ] if result.get('item') else [],
            )
        else:
            obj = SourceNewsItemList(
                total_count=result.get('total_count'),
                item_count=result.get('item_count'),
                item_list=[SourceNewsItem(
                    media_id=item.get('media_id'),
                    update_time=item.get('update_time'),
                    item_list=[NewsItem(
                        title=news_item.get('title'),
                        thumb_media_id=news_item.get('thumb_media_id'),
                        show_cover_pic=news_item.get('show_cover_pic'),
                        author=news_item.get('author'),
                        digest=news_item.get('digest'),
                        content=news_item.get('content'),
                        url=news_item.get('url'),
                        content_source_url=news_item.get('content_source_url')
                    ) for news_item in item.get('content', {}).get('news_item')
                    ] if item.get('content', {}).get('news_item') else []
                ) for item in result.get('item')
                ] if result.get('item') else [],
            )
        return obj


class MenuHandler(BaseHandler):
    def get_menu(self):
        """ 获取公众号菜单"""
        return self._get(self.apis.get_menu_url, params={'access_token': self.access_token, })

    def create_menu(self, menu_data: dict):
        """公众号创建菜单"""
        json_data = json.dumps(menu_data, ensure_ascii=False).encode('utf8')
        return self._post(self.apis.create_menu_url, params={'access_token': self.access_token, }, data=json_data)

    def delete_menu(self):
        """删除当前菜单"""
        return self._get(self.apis.delete_menu_url, params={'access_token': self.access_token, })


class DraftHandler(BaseHandler):

    def get_draft(self, media_id: str):
        """获取草稿"""

        data = {"media_id": media_id, }
        return self._post(self.apis.get_draft_url, data=data)

    def create_draft(self, article_list: List[Draft]) -> Optional[str]:
        """
        新增草稿
        :param article_list:
        :return: 成功时返回草稿的media_id
        """

        article_data = {"articles": [article.to_dict() for article in article_list]}

        # 对数据进行json处理，注意编码格式，微信不接受Unicode编码
        json_data = json.dumps(article_data, ensure_ascii=False).encode('utf8')

        result = self._post(self.apis.create_draft_url, data=json_data, has_json=True)

        if not result or not isinstance(result, dict):
            self.is_debug and self.logger.error(f'获取草稿失败！\n错误码：{self.error_code}；\n错误信息：{self.error_msg}')
            return None

        return result.get('media_id')

    def update_draft(self, article_data):
        """更新草稿"""

        # 对数据进行json处理，注意编码格式，微信不接受Unicode编码
        json_data = json.dumps(article_data, ensure_ascii=False).encode('utf8')
        return self._post(self.apis.update_draft_url, data=json_data)

    def get_draft_count(self) -> Optional[int]:

        result = self._get(self.apis.get_draft_count_url)

        if not result or not isinstance(result, dict):
            self.is_debug and self.logger.error(
                f'获取草稿数量失败！\n错误码：{self.error_code}；\n错误信息：{self.error_msg}')
            return
        return result.get('total_count')

    def get_draft_list(self, offset: int = 0, count: int = 20, no_content: int = 1) -> Optional[DraftList]:
        """
        获取草稿列表
        :param offset: 从全部素材的该偏移位置开始返回，0表示从第一个素材返回
        :param count: 返回素材的数量，取值在1到20之间
        :param no_content: 1 表示不返回 content 字段，0 表示正常返回，默认为 0
        :return:
        """

        data = {"offset": offset, "count": count, "no_content": no_content}
        result = self._post(self.apis.get_draft_list_url, data=data)

        if not result or not isinstance(result, dict):
            self.is_debug and self.logger.error(
                f'获取草稿列表失败！\n错误码：{self.error_code}；\n错误信息：{self.error_msg}')
            return

        return DraftList(
            total_count=result.get('total_count'),
            item_count=result.get('item_count'),
            draft_list=[Draft(

                media_id=item.get('media_id'),  # 草稿的media_id
                update_time=item.get('update_time'),  # 草稿的更新时间

                title=news.get('title'),  # 草稿标题，必填
                content=news.get('content'),  # 草稿内容，必填
                thumb_media_id=news.get('thumb_media_id'),  # 封面图片素材id（必须是永久MediaID），必填

                author=news.get('author'),  # 作者，非必填
                digest=news.get('digest'),  # 图文摘要；仅单图文消息才有摘要，多图文此处为空。如果本字段为没有填写，则默认抓取正文前54个字。

                content_source_url=news.get('content_source_url'),  # 图文消息的原文地址，即点击“阅读原文”后的URL
                need_open_comment=news.get('need_open_comment'),  # 是否打开评论；0不打开(默认)，1打开
                only_fans_can_comment=news.get('only_fans_can_comment'),  # 是否粉丝才可评论；0所有人可评论(默认)，1粉丝才可评论

                url=news.get('url'),  # 草稿的临时链接

            ) for item in result.get('item') for news in item.get('content', {}).get('news_item')] if result.get(
                'item') else [],
        )


class ArticleHandler(BaseHandler):
    def publish_article(self, media_id) -> Optional[str]:
        """
        需要先将图文素材以草稿的形式保存，传入草稿的 media_id 进行发布
        :param media_id:
        :return: publish_id
        """

        result = self._post(self.apis.publish_news_url, data={"media_id": media_id, })
        if not result or not isinstance(result, dict):
            self.is_debug and self.logger.error(f'发布文章失败！\n错误码：{self.error_code}；\n错误信息：{self.error_msg}')
            return

        if self.error_code != 0:
            self.is_debug and self.logger.error(f'发布文章失败！\n错误码：{self.error_code}；\n错误信息：{self.error_msg}')

        return result.get('publish_id')

    def publish_status(self, publish_id) -> Optional[ArticlePublishStatus]:
        """获知发布情况"""

        result = self._post(self.apis.publish_status_url, data={"publish_id": publish_id, })
        if not result or not isinstance(result, dict):
            self.is_debug and self.logger.error(
                f'获取发布文章状态失败！\n错误码：{self.error_code}；\n错误信息：{self.error_msg}')

        publish_status = result.get('publish_status')

        if publish_status == 0:
            self.is_debug and self.logger.info('文章发布成功！')
        elif publish_status == 1:
            self.is_debug and self.logger.info('文章还在发布中！')
        elif publish_status == 2:
            self.is_debug and self.logger.info('文章原创失败！')
        elif publish_status == 3:
            self.is_debug and self.logger.info('文章常规失败！')
        elif publish_status == 4:
            self.is_debug and self.logger.info('文章平台审核不通过！')
        elif publish_status == 5:
            self.is_debug and self.logger.info('文章发布成功后用户删除了所有文章！')
        elif publish_status == 6:
            self.is_debug and self.logger.info('文章发布成功后系统封禁了所有文章！')
        else:
            self.is_debug and self.logger.info('未知的发布状态！')

        return ArticlePublishStatus(
            publish_id=result.get('publish_id'),
            publish_status=result.get('publish_status'),
            fail_idx=result.get('fail_idx'),
            article_id=result.get('article_id'),
            article_detail=ArticleDetail(
                count=result.get('article_detail', {}).get('count'),
                item_list=[ArticleDetailItem(
                    idx=item.get('idx'),  # 文章索引
                    article_url=item.get('article_url')  # 文章URL
                ) for item in result.get('article_detail', {}).get('item')],
            ),
        )

    def delete_article(self, article_id: Union[str, int], index: int = 0) -> bool:
        """
        发布成功之后，随时可以通过该接口删除。此操作不可逆，请谨慎操作。
        :param article_id: 成功发布时返回的 article_id
        :param index: 要删除的文章在图文消息中的位置，第一篇编号为1，该字段不填或填0会删除全部文章
        :return: bool, 删除成功返回True，否则返回False
        """

        data = {'article_id': article_id, 'index': index, }
        result = self._post(self.apis.del_article_url, data=data)

        if not result or not isinstance(result, dict):
            self.is_debug and self.logger.error(f'删除文章失败！\n错误码：{self.error_code}；\n错误信息：{self.error_msg}')
            return False

        if result.get('errcode') == 0:
            return True

        return False

    def get_article_list(self, offset: str = 0, count: int = 20, no_content: int = 1):
        """
        获取已发布文章列表；待完善！
        :param offset: 从全部素材的该偏移位置开始返回，0表示从第一个素材返回
        :param count: 返回素材的数量，取值在1到20之间
        :param no_content: 1 表示不返回 content 字段，0 表示正常返回，默认为 0
        :return:
        """

        data = {"offset": offset, "count": count if count <= 20 else 20, "no_content": no_content}
        return self._post(self.apis.article_list_url, data=data)

    def get_article(self, article_id: Union[str, int]) -> Optional[List[Draft]]:

        result = self._post(self.apis.get_article_url, data={"article_id": article_id, })

        if not result or not isinstance(result, dict):
            self.is_debug and self.logger.error(
                f'获取文章详情失败！\n错误码：{self.error_code}；\n错误信息：{self.error_msg}')
            return None

        return [Draft(**item) for item in result.get('news_item')]


class IntelligenceHandler(BaseHandler):
    """智能接口："""

    def voice_to_text(
            self,
            file_path: str,
            voice_format: str,
            voice_id: str,
            lang: Literal['zh_CN', 'en_US'] = "zh_CN"
    ):
        """
        语音转文字接口；待完善
        官方文档：https://developers.weixin.qq.com/doc/offiaccount/Intelligent_Interface/AI_Open_API.html
        :param file_path:
        :param voice_format:
        :param voice_id:
        :param lang:
        :return:
        """
        params = {
            "access_token": self.access_token,
            "format": voice_format,  # 文件格式 （只支持mp3，16k，单声道，最大1M）
            "voice_id": voice_id,
            "lang": lang,
        }

        with open(file_path, "rb") as f:
            files = {"media": f}
            response = requests.post(self.apis.voice_to_text_url, files=files, params=params)

        return response.json()


class WechatOfficial(
    CustomService,
    CheckQuote,
    SourceHandler,
    MenuHandler,
    DraftHandler,
    ArticleHandler,
    IntelligenceHandler
):
    pass
