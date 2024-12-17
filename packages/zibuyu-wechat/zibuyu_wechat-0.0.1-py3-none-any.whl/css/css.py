# -*- coding: utf-8 -*-

"""
--------------------------------------------
project: zibuyu_wechat
author: 子不语
date: 2024/12/15
contact: 【公众号】思维兵工厂
description:
--------------------------------------------
"""

import re
from typing import List
from abc import ABC, abstractmethod


class BaseCSS(ABC):
    """
    CSS样式基类
    """

    def __init__(self):
        self.order_item: List[str] = []
        self.unordered_item: List[str] = []

    @abstractmethod
    def convert_h1(self, content: str) -> str:
        return ''

    @abstractmethod
    def convert_h2(self, content: str) -> str:
        return ''

    @abstractmethod
    def convert_h3(self, content: str) -> str:
        return ''

    @abstractmethod
    def convert_h4(self, content: str) -> str:
        return ''

    @abstractmethod
    def convert_h5(self, content: str) -> str:
        return ''

    @abstractmethod
    def convert_h6(self, content: str) -> str:
        return ''

    @abstractmethod
    def convert_p(self, content: str) -> str:
        return ''

    @abstractmethod
    def convert_quote(self, content: str) -> str:
        return ''

    @abstractmethod
    def convert_image(self, url: str, content: str) -> str:
        return ''

    @abstractmethod
    def convert_order_list(self, content: str) -> str:
        return ''

    @abstractmethod
    def convert_unordered_list(self, content: str) -> str:
        return ''

    @abstractmethod
    def convert_table(self, content: str) -> str:
        return ''

    def convert(self, markdown_content: str) -> str:

        if not markdown_content:
            return ""

        if not isinstance(markdown_content, str):
            return ""

        html_content = ""
        lines = markdown_content.split('\n')

        i = 0
        while i < len(lines):

            line = lines[i]

            # 处理标题
            if line.startswith("# "):
                html_content += self.convert_h1(line[2:])
            elif line.startswith("## "):
                html_content += self.convert_h2(line[3:])
            elif line.startswith("### "):
                html_content += self.convert_h3(line[4:])
            elif line.startswith("#### "):
                html_content += self.convert_h4(line[5:])
            elif line.startswith("##### "):
                html_content += self.convert_h5(line[6:])
            elif line.startswith("###### "):
                html_content += self.convert_h6(line[7:])

            # 处理引用
            elif line.startswith("> "):
                html_content += self.convert_quote(line[2:])

            # 处理图片
            elif re.match(r'!\[.*\]\(.*\)', line):
                match = re.match(r'!\[(.*)\]\((.*)\)', line)
                alt_text = match.group(1)
                url = match.group(2)
                html_content += self.convert_image(url, alt_text)

            # 处理有序列表
            elif re.match(r'^\d+\. ', line.strip()):  # 匹配以数字加 `.` 开头的行
                ordered_list_content = ""
                while i < len(lines) and re.match(r'^\d+\. ', lines[i].strip()):
                    ordered_list_content += lines[i].strip() + "\n"
                    i += 1
                html_content += self.convert_order_list(ordered_list_content.strip())
                i -= 1

            # 处理无序列表
            elif line.strip().startswith(("- ", "* ", "+ ")):
                unordered_list_content = ""
                while i < len(lines) and lines[i].strip().startswith(("- ", "* ", "+ ")):
                    unordered_list_content += lines[i].strip() + "\n"
                    i += 1
                html_content += self.convert_unordered_list(unordered_list_content.strip())
                i -= 1

            # 处理表格
            elif line.strip().startswith("|"):
                table_content = ""
                while i < len(lines) and lines[i].strip().startswith("|"):
                    table_content += lines[i].strip() + "\n"
                    i += 1
                html_content += self.convert_table(table_content.strip())
                i -= 1

            # 处理段落
            elif line.strip() == "" and html_content and not html_content.endswith("<br>"):
                html_content += "<br>"
            elif line.strip() != "":
                html_content += self.convert_p(line)
            i += 1

        css = """margin-top: 0px; 
                        margin-bottom: 0px; 
                        margin-left: 0px; 
                        margin-right: 0px; 
                        padding-top: 0px; 
                        padding-bottom: 0px; 
                        padding-left: 10px; 
                        padding-right: 10px; 
                        background-attachment: scroll; 
                        background-clip: border-box; 
                        background-color: rgba(0, 0, 0, 0); 
                        background-image: none; 
                        background-origin: padding-box; 
                        background-position-x: 0%; 
                        background-position-y: 0%; 
                        background-repeat: no-repeat; 
                        background-size: auto; 
                        width: auto; 
                        font-family: Optima, \'Microsoft YaHei\', PingFangSC-regular, serif; 
                        font-size: 16px; 
                        color: rgb(0, 0, 0); 
                        line-height: 1.5em; 
                        word-spacing: 0em; 
                        letter-spacing: 0em; 
                        word-break: break-word; 
                        overflow-wrap: break-word; 
                        text-align: left;"""

        items = css.split(';')
        css_str = '; '.join([item.strip() for item in items if item.strip()])

        return f'<section id="nice" style="{css_str}">{html_content}</section>'


class DefaultCSS(BaseCSS):
    """
    默认CSS样式
    """

    def convert_h1(self, content: str) -> str:
        return f'<h1 style="margin-top: 30px; margin-bottom: 15px; margin-left: 0px; margin-right: 0px; align-items: unset; background-attachment: scroll; background-clip: border-box; background-color: transparent; background-image: none; background-origin: padding-box; background-position-x: 0%; background-position-y: 0%; background-repeat: no-repeat; background-size: auto; border-top-style: none; border-bottom-style: none; border-left-style: none; border-right-style: none; border-top-width: 1px; border-bottom-width: 1px; border-left-width: 1px; border-right-width: 1px; border-top-color: rgb(0, 0, 0); border-bottom-color: rgb(0, 0, 0); border-left-color: rgb(0, 0, 0); border-right-color: rgb(0, 0, 0); border-top-left-radius: 0px; border-top-right-radius: 0px; border-bottom-left-radius: 0px; border-bottom-right-radius: 0px; box-shadow: none; display: block; flex-direction: unset; float: unset; height: auto; justify-content: unset; line-height: 1.5em; overflow-x: unset; overflow-y: unset; padding-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; position: relative; text-align: left; text-shadow: none; transform: none; width: auto; -webkit-box-reflect: unset;"><span class="prefix" style="display: none;"></span><span class="content" style="font-size: 28px; color: rgb(255, 255, 255); line-height: 1.5em; letter-spacing: 0em; text-align: center; padding-top: 3px; padding-bottom: 3px; padding-left: 11px; padding-right: 11px; background-attachment: scroll; background-clip: border-box; background-color: rgb(231, 100, 43); background-image: none; background-origin: padding-box; background-position-x: 0%; background-position-y: 0%; background-repeat: no-repeat; background-size: auto; width: auto; height: auto; align-items: unset; border-top-style: none; border-bottom-style: none; border-left-style: none; border-right-style: none; border-top-width: 1px; border-bottom-width: 1px; border-left-width: 1px; border-right-width: 1px; border-top-color: rgb(0, 0, 0); border-bottom-color: rgb(0, 0, 0); border-left-color: rgb(0, 0, 0); border-right-color: rgb(0, 0, 0); border-top-left-radius: 0px; border-top-right-radius: 0px; border-bottom-left-radius: 0px; border-bottom-right-radius: 0px; box-shadow: none; display: block; font-weight: bold; flex-direction: unset; float: unset; justify-content: unset; margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; overflow-x: unset; overflow-y: unset; position: relative; text-indent: 0em; text-shadow: none; transform: none; -webkit-box-reflect: unset;">{content}</span><span class="suffix" style="display: none;"></span></h1>'

    def convert_h2(self, content: str) -> str:
        return f'<h2 style="border-bottom-color: rgba(224, 144, 70, 0.85); margin-top: 30px; margin-bottom: 15px; margin-left: 0px; margin-right: 0px; padding-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; align-items: unset; background-attachment: scroll; background-clip: border-box; background-color: unset; background-image: none; background-origin: padding-box; background-position-x: 0%; background-position-y: 0%; background-repeat: no-repeat; background-size: auto; border-top-style: none; border-bottom-style: solid; border-left-style: none; border-right-style: none; border-top-width: 1px; border-bottom-width: 2px; border-left-width: 1px; border-right-width: 1px; border-top-color: rgb(0, 0, 0); border-left-color: rgb(0, 0, 0); border-right-color: rgb(0, 0, 0); border-top-left-radius: 0px; border-top-right-radius: 0px; border-bottom-left-radius: 0px; border-bottom-right-radius: 0px; box-shadow: none; display: flex; flex-direction: unset; float: unset; height: auto; justify-content: unset; line-height: 1.1em; overflow-x: unset; overflow-y: unset; position: relative; text-align: left; text-shadow: none; transform: none; width: auto; -webkit-box-reflect: unset;"><span class="prefix" style="display: none;"></span><span class="content" style="font-size: 22px; color: rgb(255, 255, 255); background-color: rgba(224, 144, 70, 0.85); line-height: 1.5em; letter-spacing: 0em; align-items: unset; background-attachment: scroll; background-clip: border-box; background-image: none; background-origin: padding-box; background-position-x: 0%; background-position-y: 0%; background-repeat: no-repeat; background-size: auto; border-top-style: none; border-bottom-style: none; border-left-style: none; border-right-style: none; border-top-width: 1px; border-bottom-width: 1px; border-left-width: 1px; border-right-width: 1px; border-top-color: rgb(0, 0, 0); border-bottom-color: rgb(0, 0, 0); border-left-color: rgb(0, 0, 0); border-right-color: rgb(0, 0, 0); border-top-left-radius: 3px; border-top-right-radius: 3px; border-bottom-left-radius: 0px; border-bottom-right-radius: 0px; box-shadow: none; display: inline-block; font-weight: bold; flex-direction: unset; float: unset; height: auto; justify-content: unset; margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 5px; overflow-x: unset; overflow-y: unset; padding-top: 3px; padding-bottom: 1px; padding-left: 10px; padding-right: 10px; position: relative; text-align: left; text-indent: 0em; text-shadow: none; transform: none; width: auto; -webkit-box-reflect: unset;">{content}</span><span class="suffix" style="display: none;"></span><span style="border-bottom-color: rgba(194, 130, 130, 0.1); align-items: unset; background-attachment: scroll; background-clip: border-box; background-color: unset; background-image: none; background-origin: padding-box; background-position-x: 0%; background-position-y: 0%; background-repeat: no-repeat; background-size: auto; border-top-style: none; border-bottom-style: solid; border-left-style: none; border-right-style: solid; border-top-width: 1px; border-bottom-width: 36px; border-left-width: 1px; border-right-width: 20px; border-top-color: rgb(0, 0, 0); border-left-color: rgb(0, 0, 0); border-right-color: transparent; border-top-left-radius: 0px; border-top-right-radius: 0px; border-bottom-left-radius: 0px; border-bottom-right-radius: 0px; box-shadow: none; color: rgb(0, 0, 0); display: inline-block; font-size: 16px; font-weight: bold; flex-direction: unset; float: unset; height: auto; justify-content: unset; letter-spacing: 0px; line-height: 1.1em; margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; overflow-x: unset; overflow-y: unset; padding-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; position: relative; text-align: left; text-indent: 0em; text-shadow: none; transform: none; width: auto; -webkit-box-reflect: unset;"> </span></h2>'

    def convert_h3(self, content: str) -> str:
        return f'<h3 style="margin-top: 30px; margin-bottom: 15px; margin-left: 0px; margin-right: 0px; padding-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; align-items: unset; background-attachment: scroll; background-clip: border-box; background-color: transparent; background-image: none; background-origin: padding-box; background-position-x: 0%; background-position-y: 0%; background-repeat: no-repeat; background-size: auto; border-top-style: none; border-bottom-style: none; border-left-style: none; border-right-style: none; border-top-width: 1px; border-bottom-width: 1px; border-left-width: 1px; border-right-width: 1px; border-top-color: rgb(0, 0, 0); border-bottom-color: rgb(0, 0, 0); border-left-color: rgb(0, 0, 0); border-right-color: rgb(0, 0, 0); border-top-left-radius: 0px; border-top-right-radius: 0px; border-bottom-left-radius: 0px; border-bottom-right-radius: 0px; box-shadow: none; display: block; flex-direction: unset; float: unset; height: auto; justify-content: unset; line-height: 1.5em; overflow-x: unset; overflow-y: unset; position: relative; text-align: left; text-shadow: none; transform: none; width: auto; -webkit-box-reflect: unset;"><span class="prefix" style="display: none;"></span><span class="content" style="font-size: 24px; color: rgb(117, 32, 94); border-bottom-color: rgb(117, 32, 94); line-height: 1.5em; letter-spacing: 0em; align-items: unset; background-attachment: scroll; background-clip: border-box; background-color: transparent; background-image: none; background-origin: padding-box; background-position-x: 0%; background-position-y: 0%; background-repeat: no-repeat; background-size: auto; border-top-style: none; border-bottom-style: solid; border-left-style: none; border-right-style: none; border-top-width: 1px; border-bottom-width: 4px; border-left-width: 1px; border-right-width: 1px; border-top-color: rgb(0, 0, 0); border-left-color: rgb(0, 0, 0); border-right-color: rgb(0, 0, 0); border-top-left-radius: 0px; border-top-right-radius: 0px; border-bottom-left-radius: 0px; border-bottom-right-radius: 0px; box-shadow: none; display: block; font-weight: bold; flex-direction: unset; float: unset; height: auto; justify-content: unset; margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; overflow-x: unset; overflow-y: unset; padding-top: 2px; padding-bottom: 0px; padding-left: 0px; padding-right: 4px; position: relative; text-align: left; text-indent: 0em; text-shadow: none; transform: none; width: auto; -webkit-box-reflect: unset;">{content}</span><span class="suffix" style="display: none;"></span></h3>'

    def convert_h4(self, content: str) -> str:
        return f'<h4 style="margin-top: 30px; margin-bottom: 15px; margin-left: 0px; margin-right: 0px; padding-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; align-items: unset; background-attachment: scroll; background-clip: border-box; background-color: transparent; background-image: none; background-origin: padding-box; background-position-x: 0%; background-position-y: 0%; background-repeat: no-repeat; background-size: auto; border-top-style: none; border-bottom-style: none; border-left-style: none; border-right-style: none; border-top-width: 1px; border-bottom-width: 1px; border-left-width: 1px; border-right-width: 1px; border-top-color: rgb(0, 0, 0); border-bottom-color: rgb(0, 0, 0); border-left-color: rgb(0, 0, 0); border-right-color: rgb(0, 0, 0); border-top-left-radius: 0px; border-top-right-radius: 0px; border-bottom-left-radius: 0px; border-bottom-right-radius: 0px; box-shadow: none; display: block; flex-direction: unset; float: unset; height: auto; justify-content: unset; line-height: 1.5em; overflow-x: unset; overflow-y: unset; position: relative; text-align: left; text-shadow: none; transform: none; width: auto; -webkit-box-reflect: unset;"><span class="prefix" style="display: none;"></span><span class="content" style="font-size: 22px; color: rgb(37, 132, 181); border-bottom-color: rgb(37, 132, 181); line-height: 1.5em; letter-spacing: 0em; align-items: unset; background-attachment: scroll; background-clip: border-box; background-color: transparent; background-image: none; background-origin: padding-box; background-position-x: 0%; background-position-y: 0%; background-repeat: no-repeat; background-size: auto; border-top-style: none; border-bottom-style: solid; border-left-style: none; border-right-style: none; border-top-width: 1px; border-bottom-width: 4px; border-left-width: 1px; border-right-width: 1px; border-top-color: rgb(0, 0, 0); border-left-color: rgb(0, 0, 0); border-right-color: rgb(0, 0, 0); border-top-left-radius: 0px; border-top-right-radius: 0px; border-bottom-left-radius: 0px; border-bottom-right-radius: 0px; box-shadow: none; display: block; font-weight: bold; flex-direction: unset; float: unset; height: auto; justify-content: unset; margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; overflow-x: unset; overflow-y: unset; padding-top: 2px; padding-bottom: 0px; padding-left: 0px; padding-right: 4px; position: relative; text-align: left; text-indent: 0em; text-shadow: none; transform: none; width: auto; -webkit-box-reflect: unset;">{content}</span><span class="suffix" style="display: none;"></span></h4>'

    def convert_h5(self, content: str) -> str:
        return f'<h5 style="border-bottom-color: rgb(37, 181, 170); margin-top: 30px; margin-bottom: 15px; margin-left: 0px; margin-right: 0px; align-items: unset; background-attachment: scroll; background-clip: border-box; background-color: transparent; background-image: none; background-origin: padding-box; background-position-x: 0%; background-position-y: 0%; background-repeat: no-repeat; background-size: auto; border-top-style: none; border-bottom-style: solid; border-left-style: none; border-right-style: none; border-top-width: 1px; border-bottom-width: 1px; border-left-width: 1px; border-right-width: 1px; border-top-color: rgb(0, 0, 0); border-left-color: rgb(0, 0, 0); border-right-color: rgb(0, 0, 0); border-top-left-radius: 0px; border-top-right-radius: 0px; border-bottom-left-radius: 0px; border-bottom-right-radius: 0px; box-shadow: none; display: block; flex-direction: unset; float: unset; height: auto; justify-content: unset; line-height: 1.5em; overflow-x: unset; overflow-y: unset; padding-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; position: relative; text-align: left; text-shadow: none; transform: none; width: auto; -webkit-box-reflect: unset;"><span class="prefix" style="display: none;"></span><span class="content" style="font-size: 20px; color: rgb(37, 181, 170); line-height: 1.5em; letter-spacing: 0em; padding-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; align-items: unset; background-attachment: scroll; background-clip: border-box; background-color: transparent; background-image: none; background-origin: padding-box; background-position-x: 0%; background-position-y: 0%; background-repeat: no-repeat; background-size: auto; border-top-style: none; border-bottom-style: none; border-left-style: none; border-right-style: none; border-top-width: 1px; border-bottom-width: 1px; border-left-width: 1px; border-right-width: 1px; border-top-color: rgb(0, 0, 0); border-bottom-color: rgb(0, 0, 0); border-left-color: rgb(0, 0, 0); border-right-color: rgb(0, 0, 0); border-top-left-radius: 0px; border-top-right-radius: 0px; border-bottom-left-radius: 0px; border-bottom-right-radius: 0px; box-shadow: none; display: block; font-weight: bold; flex-direction: unset; float: unset; height: auto; justify-content: unset; margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; overflow-x: unset; overflow-y: unset; position: relative; text-align: left; text-indent: 0em; text-shadow: none; transform: none; width: auto; -webkit-box-reflect: unset;">{content}</span><span class="suffix" style="display: none;"></span></h5>'

    def convert_h6(self, content: str) -> str:
        return f'<h6 style="border-bottom-color: rgb(181, 95, 37); margin-top: 30px; margin-bottom: 15px; margin-left: 0px; margin-right: 0px; align-items: unset; background-attachment: scroll; background-clip: border-box; background-color: transparent; background-image: none; background-origin: padding-box; background-position-x: 0%; background-position-y: 0%; background-repeat: no-repeat; background-size: auto; border-top-style: none; border-bottom-style: solid; border-left-style: none; border-right-style: none; border-top-width: 1px; border-bottom-width: 1px; border-left-width: 1px; border-right-width: 1px; border-top-color: rgb(0, 0, 0); border-left-color: rgb(0, 0, 0); border-right-color: rgb(0, 0, 0); border-top-left-radius: 0px; border-top-right-radius: 0px; border-bottom-left-radius: 0px; border-bottom-right-radius: 0px; box-shadow: none; display: block; flex-direction: unset; float: unset; height: auto; justify-content: unset; line-height: 1.5em; overflow-x: unset; overflow-y: unset; padding-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; position: relative; text-align: left; text-shadow: none; transform: none; width: auto; -webkit-box-reflect: unset;"><span class="prefix" style="display: none;"></span><span class="content" style="font-size: 18px; color: rgb(181, 95, 37); line-height: 1.5em; letter-spacing: 0em; padding-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; align-items: unset; background-attachment: scroll; background-clip: border-box; background-color: transparent; background-image: none; background-origin: padding-box; background-position-x: 0%; background-position-y: 0%; background-repeat: no-repeat; background-size: auto; border-top-style: none; border-bottom-style: none; border-left-style: none; border-right-style: none; border-top-width: 1px; border-bottom-width: 1px; border-left-width: 1px; border-right-width: 1px; border-top-color: rgb(0, 0, 0); border-bottom-color: rgb(0, 0, 0); border-left-color: rgb(0, 0, 0); border-right-color: rgb(0, 0, 0); border-top-left-radius: 0px; border-top-right-radius: 0px; border-bottom-left-radius: 0px; border-bottom-right-radius: 0px; box-shadow: none; display: block; font-weight: bold; flex-direction: unset; float: unset; height: auto; justify-content: unset; margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; overflow-x: unset; overflow-y: unset; position: relative; text-align: left; text-indent: 0em; text-shadow: none; transform: none; width: auto; -webkit-box-reflect: unset;">{content}</span><span class="suffix" style="display: none;"></span></h6>'

    def convert_p(self, content: str) -> str:
        return f'<p style="color: rgb(0, 0, 0); font-size: 18px; line-height: 1.5em; letter-spacing: 0em; text-align: left; text-indent: 0em; margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; padding-top: 8px; padding-bottom: 8px; padding-left: 0px; padding-right: 0px;">{content}</p>'

    def convert_quote(self, content: str) -> str:
        return f'''<blockquote class="custom-blockquote multiquote-1" style="margin-top: 20px; margin-bottom: 20px; margin-left: 0px; margin-right: 0px; padding-top: 10px; padding-bottom: 10px; padding-left: 20px; padding-right: 10px; border-top-style: none; border-bottom-style: none; border-left-style: solid; border-right-style: none; border-top-width: 3px; border-bottom-width: 3px; border-left-width: 3px; border-right-width: 3px; border-top-color: rgba(0, 0, 0, 0.4); border-bottom-color: rgba(0, 0, 0, 0.4); border-left-color: rgb(239, 112, 96); border-right-color: rgba(0, 0, 0, 0.4); border-top-left-radius: 0px; border-top-right-radius: 0px; border-bottom-right-radius: 0px; border-bottom-left-radius: 0px; background-attachment: scroll; background-clip: border-box; background-color: rgb(255, 249, 249); background-image: none; background-origin: padding-box; background-position-x: 0%; background-position-y: 0%; background-repeat: no-repeat; background-size: auto; width: auto; height: auto; box-shadow: rgba(0, 0, 0, 0) 0px 0px 0px 0px; display: block; overflow-x: auto; overflow-y: auto;"><span style="display: none; color: rgb(0, 0, 0); font-size: 16px; line-height: 1.5em; letter-spacing: 0px; text-align: left; font-weight: normal;"></span>
<p style="text-indent: 0em; padding-top: 8px; padding-bottom: 8px; padding-left: 0px; padding-right: 0px; color: rgb(0, 0, 0); font-size: 15px; line-height: 1.8em; letter-spacing: 0px; text-align: left; font-weight: normal; margin-top: 0px; margin-right: 0px; margin-bottom: 0px; margin-left: 0px;">{content}</p>
</blockquote>'''

    def convert_image(self, url: str, content: str) -> str:
        return f'<figure style="margin-top: 10px; margin-bottom: 10px; margin-left: 0px; margin-right: 0px; padding-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; display: flex; flex-direction: column; justify-content: center; align-items: center;"><img src="{url}" alt="{content}" style="display: block; margin-top: 0px; margin-right: auto; margin-bottom: 0px; margin-left: auto; max-width: 100%; border-top-style: none; border-bottom-style: none; border-left-style: none; border-right-style: none; border-top-width: 3px; border-bottom-width: 3px; border-left-width: 3px; border-right-width: 3px; border-top-color: rgba(0, 0, 0, 0.4); border-bottom-color: rgba(0, 0, 0, 0.4); border-left-color: rgba(0, 0, 0, 0.4); border-right-color: rgba(0, 0, 0, 0.4); border-top-left-radius: 0px; border-top-right-radius: 0px; border-bottom-right-radius: 0px; border-bottom-left-radius: 0px; object-fit: fill; box-shadow: rgba(0, 0, 0, 0) 0px 0px 0px 0px;"><figcaption style="color: rgb(136, 136, 136); font-size: 14px; line-height: 1.5em; letter-spacing: 0em; text-align: center; font-weight: normal; margin-top: 5px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; padding-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px;">{content}</figcaption></figure>'

    def convert_order_list(self, content: str):
        item_list = [item.split('. ', maxsplit=1)[-1].strip() for item in content.split('\n') if item.strip()]

        new_item_list = []
        for item in item_list:
            new_item_list.append(
                f'<li><section style="margin-top: 5px; margin-bottom: 5px; color: rgb(1, 1, 1); font-size: 16px; line-height: 1.8em; letter-spacing: 0em; text-align: left; font-weight: normal;">{item}</section></li>'
            )

        item_str = ''.join(new_item_list)

        return f'''<ol style="list-style-type: decimal; margin-top: 8px; margin-bottom: 8px; margin-left: 0px; margin-right: 0px; padding-top: 0px; padding-bottom: 0px; padding-left: 25px; padding-right: 0px; color: rgb(0, 0, 0);">{item_str}</ol>'''

    def convert_unordered_list(self, content: str) -> str:
        item_list = [item.replace('- ', '').strip() for item in content.split('\n') if item.strip()]

        new_item_list = []
        for item in item_list:
            new_item_list.append(
                f'<li><section style="margin-top: 5px; margin-bottom: 5px; color: rgb(1, 1, 1); font-size: 16px; line-height: 1.8em; letter-spacing: 0em; text-align: left; font-weight: normal;">{item}</section></li>'
            )

        item_str = ''.join(new_item_list)

        return f'<ul style="list-style-type: disc; margin-top: 8px; margin-bottom: 8px; margin-left: 0px; margin-right: 0px; padding-top: 0px; padding-bottom: 0px; padding-left: 25px; padding-right: 0px; color: rgb(0, 0, 0);">{item_str}</ul>'

    def convert_table(self, content: str) -> str:

        # 分割表格为行
        lines = content.strip().split('\n')

        # 初始化HTML表格
        html_table = '<table style="display: table; text-align: left;">\n'

        # 处理表头
        header_row = lines[0].strip()
        header_cells = header_row.split('|')
        header_cells = [cell.strip() for cell in header_cells if cell.strip()]
        html_table += '  <tr>\n'
        for cell in header_cells:
            html_table += f'<th style="color: rgb(10, 0, 0); font-size: 17px; line-height: 1.5em; letter-spacing: 0em; text-align: center; font-weight: bold; background-attachment: scroll; background-clip: border-box; background-color: rgb(240, 240, 240); background-image: none; background-origin: padding-box; background-position-x: 0%; background-position-y: 0%; background-repeat: no-repeat; background-size: auto; width: auto; height: auto; border-top-style: solid; border-bottom-style: solid; border-left-style: solid; border-right-style: solid; border-top-width: 1px; border-bottom-width: 1px; border-left-width: 1px; border-right-width: 1px; border-top-color: rgba(204, 204, 204, 0.4); border-bottom-color: rgba(204, 204, 204, 0.4); border-left-color: rgba(204, 204, 204, 0.4); border-right-color: rgba(204, 204, 204, 0.4); border-top-left-radius: 0px; border-top-right-radius: 0px; border-bottom-right-radius: 0px; border-bottom-left-radius: 0px; padding-top: 5px; padding-right: 10px; padding-bottom: 5px; padding-left: 10px; min-width: 85px;">{cell}</th>\n'
        html_table += '  </tr>\n'

        # 处理分隔行（用于确定对齐方式）
        separator_row = lines[1].strip()
        separator_cells = separator_row.split('|')
        alignments = []
        for cell in separator_cells:
            cell = cell.strip()
            if cell.startswith(':') and cell.endswith(':'):
                alignments.append('center')
            elif cell.startswith(':'):
                alignments.append('left')
            elif cell.endswith(':'):
                alignments.append('right')
            else:
                alignments.append('left')

        # 处理数据行
        for line in lines[2:]:
            data_row = line.strip()
            data_cells = data_row.split('|')
            data_cells = [cell.strip() for cell in data_cells if cell.strip()]

            html_table += '<tr style="color: rgb(0, 0, 0); background-attachment: scroll; background-clip: border-box; background-color: rgb(255, 255, 255); background-image: none; background-origin: padding-box; background-position-x: 0%; background-position-y: 0%; background-repeat: no-repeat; background-size: auto; width: auto; height: auto;">'
            for i, cell in enumerate(data_cells):
                align = alignments[i]
                html_table += f'<td style="text-align: {align}; padding-top: 5px; padding-right: 10px; padding-bottom: 5px; padding-left: 10px; min-width: 85px; border-top-style: solid; border-bottom-style: solid; border-left-style: solid; border-right-style: solid; border-top-width: 1px; border-bottom-width: 1px; border-left-width: 1px; border-right-width: 1px; border-top-color: rgba(204, 204, 204, 0.4); border-bottom-color: rgba(204, 204, 204, 0.4); border-left-color: rgba(204, 204, 204, 0.4); border-right-color: rgba(204, 204, 204, 0.4); border-top-left-radius: 0px; border-top-right-radius: 0px; border-bottom-right-radius: 0px; border-bottom-left-radius: 0px;">{cell}</td>'

            html_table += '  </tr>\n'

        html_table += '</table>'

        return f'''<section class="table-container"
         style="margin-top: 0px;
         margin-bottom: 0px;
         margin-left: 0px;
         margin-right: 0px;
         padding-top: 0px;
         padding-bottom: 0px;
         padding-left: 0px;
         padding-right: 0px;
         overflow-x: auto;">{html_table}</section>'''
