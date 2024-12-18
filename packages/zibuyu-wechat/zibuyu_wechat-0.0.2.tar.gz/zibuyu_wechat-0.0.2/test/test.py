# -*- coding: utf-8 -*-

"""
--------------------------------------------
project: zibuyu_wechat
author: 子不语
date: 2024/12/16
contact: 【公众号】思维兵工厂
description: 
--------------------------------------------
"""

from zibuyu_wechat.css import DefaultCSS
from zibuyu_wechat.api.official import *

access_token = '''
87_sJWacHvNqETN2m1TJUw0Yz8MN0-0nVxvDwOOzTCdiLGLSWTrOfgum4ze89loX1MQjMgfBReRdW7PzD3mpJubiBrp2aTVGymW8TmuKfdiMtiMiDRYk0744DoAxykGHLcAHACDH
'''

token_expires_in = int(time.time()) + 7000

handler = WechatOfficial(
    app_id="wx3b2fd309f9f0710d",
    app_secret="fcc9c14c2c38c33554fac1eabe1eb577",
    access_token=access_token.strip(),
    token_expires_in=token_expires_in
)

print(handler.access_token)

md_content = """
# 标题一

## 标题二

### 标题三

#### 标题四

##### 标题五

###### 标题六

> 引用文本

![图片样式](http://mmbiz.qpic.cn/sz_mmbiz_jpg/KSl3Ku9NC8EKuypPBkzSkYeibereA2eKOVv8eEN1la0oNVib7YnUL3pjJgKNvOhUr7xs4An7xCGB0AiaA83srNlIw/0?wx_fmt=jpeg)

|序号|单词|释义|
| -------- | -------- | -------- |
| |foul|(1)  To stop breathing for a short time (for a challenge, for a bad smell, for an X-rayâ¦.|
| |rotting|(2)  Very bad or unpleasant (often used to describe a strong, bad smell).|
| |flesh|(3)  Made someone or something come closer.|

## 文章原文

People who like foul-smelling flowers were in luck this week.

They had a chance to see and smell the world's smelliest plant, called the corpse flower.

A corpse is a dead body.

The flower gets its name because it smells like rotting flesh.

The bloom attracted thousands of visitors to the Geelong Botanic Garden, just south of Melbourne, Australia.

The plant began blooming on Monday.

More than five thousand people visited the garden to see it.

Some people had to hold their nose when they were near the flower.

Others coughed and held their breath because of the foul smell.

Australia's Nine News channel reported that visitors described the smell as being like a dead mouse or rotting garbage.

The corpse flower is extremely rare.

The plant is native to Indonesia.

An international conservation group listed it as an endangered species.

The group says there are only a few hundred of the plants left in the wild.

A lot of the forest in which the plant grows has been cut down.

Corporations are using the land to grow palm oil.

The flower is one of the biggest in the world.

It can grow to a height of three metres and live over 40 years.

However, it blooms just once a decade and opens only for a day or two.

The flower smells like the rotting flesh of a dead animal.

This smell attracts beetles and flies.

The insects pollinate the flower so it can bloom again.


## 词汇练习

为下面的单词寻找正确释义：

foul; rotting; flesh; bloom; attracted; hold one's nose; hold their breath; extremely; rare; native; conservation; endangered; in the wild; pollinate;

### 释义列表
1. To stop breathing for a short time (for a challenge, for a bad smell, for an X-rayâ¦.)
2. Very bad or unpleasant (often used to describe a strong, bad smell).
3. Made someone or something come closer.
4. Slowly breaking down and becoming bad; often has a bad smell (like old food or a dead plant).
5. A flower.
6. To close your nose with your fingers to avoid a bad smell.
7. The soft parts of an animal or human body, not the bones.
8. Very, very much.
9. To move pollen from one flower to another to help it grow seeds.
10. From a certain place; growing or living naturally in a certain area.
11. Not often found or seen; uncommon.
12. Protecting nature and animals so they are safe and don’t disappear.
13. In nature, not in a place made by people, like a zoo or a garden.
14. At risk of disappearing forever.


## 判断对错

- People who like bad-smelling flowers are lucky.
- The corpse flower is the world's smelliest flower.
- Fifteen thousand people waited to see the corpse flower.
- Someone said the corpse flower smelled like a dead mouse.
- There are thousands of corpse flowers growing in Indonesia.
- Forests where the corpse flower lives are being cut down for coconut oil.
- Corpse flowers can live for 40 years.
- The corpse flower attracts butterflies and dragonflies.


## 讨论问答

- Who does the article say was in luck?
- In what kind of garden do people go to see the corpse flower?
- How many people visited the garden?
- What two things did people hold when they were near the flower?
- What dead animal did someone say the flower smelled like?
- Where does the corpse flower usually grow?
- How many corpse plants are growing in the wild?
- What is land being used for where corpse flowers used to grow?
- For how long can a corpse flower grow?
- What do beetles and flies do to the corpse flower?

"""

css_handler = DefaultCSS()
html = css_handler.convert(md_content)

image_path = 'D:\\06_program_code\\zibuyu_wechat\\2.jpg'

# result = handler.upload_hard_source(image_path)
# if not result:
#     exit(0)
# print(result.media_id)

draft_obj = Draft(
    title='测试英文阅读33332',
    author='子不语',
    digest='测试文档2',
    content=html,
    thumb_media_id='x6lBIVCeGMg_tlN-qAPFWpITCARMLD1wDYgwFjLD-RPdGlNNGlIdOfRhX7I9G0dV',
    need_open_comment=1
)

# result = handler.create_draft([draft_obj, ])
# print(result)

# result = handler.get_draft_list()
# print(result)

# result = handler.publish_news( media_id='x6lBIVCeGMg_tlN-qAPFWvIiRI5KJqS-peYmOspLpUJPgXfvGDBvfbBkYFjXRi7C')
# print(result)
# 2247483692

# result = handler.publish_status(publish_id='2247483692')
# print(result)

result = handler.get_article('lcl7QHZYV7f-btPXGE2iedNYvohPhFbV1Lltk0ea-1zCgybZ0zF5BTQR2GI-_x88')
print(result)