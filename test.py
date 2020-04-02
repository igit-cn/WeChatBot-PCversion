from WechatPCAPI import WechatPCAPI
import time
import logging
from queue import Queue
import threading
import tencent_bot
import sizhi_bot
import re
import datetime

logging.basicConfig(level=logging.INFO)
queue_recved_message = Queue()
wx_inst = 0
auto_reply = False
count = 0
monitor_wxid = ''


def getAt(string):
    """
    查询是否有人在群里at我
    :param string: 消息字符串
    :return: True：有人at我 False：没有收到at
    """
    global wx_inst
    localname = "@" + wx_inst.get_myself()['data']['wx_nickname']
    if string.find(localname) != -1:
        return True
    else:
        return False


def control(message):
    """
    收到控制消息
    :param message: 消息
    :return: None
    """
    global auto_reply, monitor_wxid

    if message['data']['msg'] == 'on':
        if auto_reply is True:
            wx_inst.send_text(to_user=monitor_wxid, msg='already ON')
            return
        auto_reply = True
        wx_inst.send_text(to_user=monitor_wxid, msg='auto reply ON')
        return
    if message['data']['msg'] == 'off':
        if auto_reply is False:
            wx_inst.send_text(to_user=monitor_wxid, msg='already OFF')
            return
        auto_reply = False
        wx_inst.send_text(to_user=monitor_wxid, msg='auto reply OFF')
        return


def reply_single(message):
    """
    单聊回复
    :param message: 消息
    :return: None
    """
    global auto_reply, count, monitor_wxid

    msg = message['data']['msg']
    # 去除emoji
    emoji = re.compile(r'\[.*?\]').findall(msg)
    for a in emoji:
        msg = msg.replace(a, "")
    # 腾讯机器人
    # msg = tencent_bot.get_response(message['data']['msg'], message['data']['from_nickname'])
    # 思知机器人
    # msg = sizhi_bot.get_response(msg, message['data']['from_nickname'])
    if msg:
        time.sleep(len(msg) // 4)
        wx_inst.send_text(to_user=message['data']['from_wxid'], msg=msg)
        count += 1
    return


def reply_group(message):
    """
    群聊回复
    :param msg: 消息
    :return: None
    """
    global auto_reply, count, monitor_wxid

    msg = message['data']['msg']
    print("收到at")
    # 去除所有at
    allAt = re.compile(r'@(.*)\?').findall(msg)
    for a in allAt:
        msg = msg.replace(a, "")
    msg = msg.replace("@", "")
    msg = msg.replace("?", "")
    # 去除emoji
    emoji = re.compile(r'\[.*?\]').findall(msg)
    for a in emoji:
        msg = msg.replace(a, "")
    print(msg)
    # 腾讯机器人
    # msg = tencent_bot.get_response(msg, message['data']['from_chatroom_wxid'])
    # 思知机器人
    # msg = sizhi_bot.get_response(message['data']['msg'], message['data']['from_member_wxid'])
    time.sleep(len(msg) // 4)
    if msg:
        wx_inst.send_text(to_user=message['data']['from_chatroom_wxid'], msg=msg)
        count += 1
    return


def counter():
    global auto_reply, count, monitor_wxid

    while True:
        time.sleep(3600)
        now = datetime.datetime.now().hour
        wx_inst.send_text(to_user=monitor_wxid, msg='运行中，已回复' + str(count) + '条消息')
        if now == 0 and auto_reply is False:
            auto_reply = True
            wx_inst.send_text(to_user=monitor_wxid, msg='auto reply ON')
            count = 0
        if now == 10 and auto_reply is True:
            auto_reply = False
            wx_inst.send_text(to_user=monitor_wxid, msg='auto reply OFF')


def on_message(message):
    """
    这是消息回调函数，所有的返回消息都在这里接收，建议异步处理，防止阻塞
    :param message: 发送/接收的消息详情
    :return: null
    """
    print(message)
    # 收到群聊消息且有@
    if auto_reply and message['type'] == 'msg::chatroom' and message['data']['send_or_recv'][0] == '0' \
            and message['data']['data_type'] == '1' and getAt(message['data']['msg']):
        threading.Thread(target=reply_group, args=(message,)).start()
        return
    # 收到控制消息
    if message['type'] == 'msg::single' and message['data']['from_wxid'] == monitor_wxid \
            and message['data']['send_or_recv'][0] == '0' and (message['data']['msg'] == 'on' or message['data']['msg'] == 'off'):
        threading.Thread(target=control, args=(message,)).start()
        return
    # 收到单聊消息
    if auto_reply and message['type'] == 'msg::single' and message['data']['send_or_recv'][0] == '0' \
            and message['data']['data_type'] == '1':
        threading.Thread(target=reply_single, args=(message,)).start()


def main():
    """
    初始化
    :return: null
    """
    global wx_inst
    wx_inst = WechatPCAPI(on_message=on_message, log=logging)
    wx_inst.start_wechat(block=True)

    while not wx_inst.get_myself():
        time.sleep(5)

    print('登陆成功')
    print(wx_inst.get_myself())

    time.sleep(5)


if __name__ == '__main__':
    threading.Thread(target=counter).start()
    main()

""" 收到消息dict
单人
{
'user': '', 
'type': 'msg::single', 
'data': {
    'data_type': '1', (1=文字, 还有3, 4, 43记不得是啥了, 不过分别对应图片、表情包、视频)
    'send_or_recv': '0+[收到]', (0=收到, 1=发送)
    'from_wxid': 'wxid_xxxxx', 
    'time': '2020-03-28 08:25:53', 
    'msg': '1', 
    'msg_byte_hex': '31', 
    'from_nickname': 'xxxx'}
}

群
{
'user': '', 
'type': 'msg::chatroom', 
'data': {
    'data_type': '1', 
    'send_or_recv': '0+[收到]', 
    'from_chatroom_wxid': 'xxxxxx@chatroom', 
    'from_member_wxid': 'wxid_xxxxx', 
    'time': '2020-03-28 08:27:34', 
    'msg': 'xxxxx', 
    'msg_byte_hex': 'BFCFB6A8D3D0B9D8', 
    'from_chatroom_nickname': 'xxxxxx'}
}
"""

"""发送消息dict
{
'user': '', 
'type': 'msg::single', 
'data': {
    'data_type': '1', 
    'send_or_recv': '1+[Demo]', 
    'from_wxid': 'wxid_xxxxxx', 
    'time': '2020-3-28 00:25:55', 
    'msg': '你好', 
    'msg_byte_hex': 'C4E3BAC3', 
    'from_nickname': 'xxxxxx'}
}
"""

"""
开启保存文件图片等功能，不调用默认不保存，调用需要放在登陆成功之后
wx_inst.start_auto_save_files()

发送消息
wx_inst.send_text(to_user='filehelper', msg='1446684220')

发送图片
wx_inst.send_img(to_user='filehelper', img_abspath='C:')

发送链接卡片
wx_inst.send_link_card(
     to_user='filehelper',
     title='博客',
     desc='我的博客，红领巾技术分享网站',
     target_url='http://www.honglingjin.online/',
     img_url='http://honglingjin.online/wp-content/uploads/2019/07/0-1562117907.jpeg'
)

这个是获取群具体成员信息的，成员结果信息也从上面的回调返回
wx_inst.get_member_of_chatroom('22941059407@chatroom')

删除好友
wx_inst.get_friends("wx_123231212121")  # 参数写wxid

更新好友，一般不用调，后台会维护好友表，但是不放心表不准，可以先调用这个再调get_friends
wx_inst.update_frinds()

这个是更新所有好友、群、公众号信息的，结果信息也从上面的on_message返回
wx_inst.get_friends()

get_myself()
{
'code': 0, 
'data': {
    'wx_id': '', 
    'wx_nickname': 'xxxxx', 
    'avatar_url': 'http://wx.qlogo.cn/mmhead/ver_1/Ay0U5bD3icLqXM......'}
}
"""
