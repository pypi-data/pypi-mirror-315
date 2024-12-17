# -*- coding: utf-8 -*-

"""
--------------------------------------------
project: zibuyu_wechat
author: 子不语
date: 2024/11/15
contact: 【公众号】思维兵工厂
description: 
--------------------------------------------
"""

import logging
import logging.config
from builtins import ModuleNotFoundError


def make_logger(logger_name: str = 'main_logger') -> logging.Logger:
    """
    配置日志对象
    :return: logging.Logger
    """

    fmt = "%(asctime)s.%(msecs)04d | %(levelname)8s | %(module)s | 行号：%(lineno)d | %(message)s "

    logger_config = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "verbose": {
                "format": fmt,
                "style": "%"
            }
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "verbose"
            }
        },
        "loggers": {
            "main_logger": {
                "handlers": ["console", ],
                "propagate": True,
                "level": 'DEBUG'
            }
        }
    }

    logging.config.dictConfig(logger_config)
    logger = logging.getLogger(logger_name)

    try:

        import coloredlogs

        level_color_mapping = {
            'DEBUG': {'color': 'blue'},
            'INFO': {'color': 'green'},
            'WARNING': {'color': 'yellow', 'bold': True},
            'ERROR': {'color': 'red'},
            'CRITICAL': {'color': 'red', 'bold': True}
        }

        # 自定义日志的字段颜色
        field_color_mapping = dict(
            asctime=dict(color='green'),
            hostname=dict(color='magenta'),
            levelname=dict(color='white', bold=True),
            name=dict(color='blue'),
            programname=dict(color='cyan'),
            username=dict(color='yellow'),
        )

        coloredlogs.install(
            level=logging.DEBUG,
            logger=logger,
            milliseconds=True,
            datefmt='%X',
            fmt=fmt,
            level_styles=level_color_mapping,
            field_styles=field_color_mapping
        )
    except ModuleNotFoundError:
        logger.info("温馨提示：安装 coloredlogs 模块，可使得终端日志输出更好看~")
    except:
        logger.error('初始化 logger 出现未知错误！')
    finally:
        return logger
