import requests


url = "https://api.ownthink.com/bot"
appid = ''


def get_response(msg, userid):
    """
    获取回复
    :param msg: 待回复字符串
    :param userid: 会话识别码
    :return: string: 成功的回复 None: 失败
    """
    params = {
        'spoken': msg,
        'appid': appid,
        'userid': userid
    }
    req = requests.get(url, params=params)
    if req.status_code == 200:
        content = req.json()
        print(content)
        return content['data']['info']['text']
    else:
        return None


if __name__ == '__main__':
    url = "https://api.ownthink.com/bot"
    params = {
        'spoken': '在吗',
        'sappid': appid,
        'userid': 'user'
    }
    req = requests.get(url, params=params)
    print(req)
    content = req.json()
    print(content)
