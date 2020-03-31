# WeChatBot-PCversion

基于`Mocha-L`的项目[WechatPCAPI](https://github.com/Mocha-L/WechatPCAPI)二次开发，接入了`腾讯AI`和`思知机器人`以实现即时回复消息的功能，机器人部分代码来源于[EverydayWechat](https://github.com/sfyc23/EverydayWechat)

项目基于PC端微信客户端开发，账号无需登录网页版，要求微信客户端版本固定（V2.7.1.82），具体细节请移步上面↑的传送门

<img src="https://github.com/antares927/WeChatBot-PCversion/blob/master/img/Screenshot_20200331-112237_WeChat.jpg" width = 40% height = 40% />
<img src="https://github.com/antares927/WeChatBot-PCversion/blob/master/img/b474c483gy1gd9csgaltaj20tz1pxgvq.jpg" width = 40% height = 40% />

## 功能

- 回复单聊微信
- 回复群聊中@自己的信息
- 通过另一个账号进行自动回复功能的开关（更改`test.py`的全局变量`monitor_wxid`，填入另一个账号的微信号或者filehelper）**注：** 使用filehelper的时候记得把`on_message()`里`收到控制消息`的`if`的`message['data']['send_or_recv'][0] == '0'`改成1

### 机器人

- 图灵机器人：http://www.turingapi.com/ (需求实名制认证，并每天免费数量只有 100 条)
- 青云客智能聊天机器人：http://api.qingyunke.com/ (无须申请，无数量限制，但有点智障，分手神器。分手神器，慎用)
- 智能闲聊（腾讯）：https://ai.qq.com/product/nlpchat.shtml (申请使用，免费且无限量。大厂靠谱。)
- 天行机器人 ：https://www.tianapi.com/apiview/47 (认证后有 7 万条免费使用。之后收费：1 万条/1 块钱)
- 海知智能 ：https://ruyi.ai/ (功能很强大，不仅仅用于聊天。需申请 key，免费)
- 思知对话机器人：https://www.ownthink.com/ (免费，可不申请 appid)
- 一个AI：http://www.yige.ai/ (免费且无数量限制。可自定义回复、对话、场景。但高级功能使用比较复杂。但已长时间没人维护)

自己试用下来推荐思知；腾讯的识别范围很广，可以不仅仅作聊天机器人用，还能当百科全书，但聊天功能就比较弱智，经常性找不到回复，不过上下文结合不错；海知是纯机器人；天行总是返回500错误

**注册后把获得的key填入对应的py文件顶部**

*有问题请询问API作者和机器人平台*

## 免责声明

项目仅为技术交流，不对任何其他目的造成的损失与纠纷负责
