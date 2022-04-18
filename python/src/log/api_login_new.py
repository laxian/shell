import requests

import json
from src.log.config import Config
from src.log.token_exception import TokenException
from functools import wraps


def p(obj, *args, **kw):
    print(obj)


def check_response(response):
    j = json.loads(response)
    code = j["code"]
    if code == 4006 or code == 4007:
        raise TokenException(j["message"])
    elif code != 200:
        raise Exception(j["message"])
    else:
        return j


def relogin(h=p, **kw):
    def logging_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            token = (
                login_and_save_token(args[3])
                if len(args) > 3
                else login_and_save_token()
            )
            # print("%s %s %s" % (token, args, kwargs))
            content = func(token, *args, **kwargs)
            try:
                j = check_response(content)
                return h(j, *args, **kwargs)
            except TokenException as ex:
                clear_token()
                return wrapped_function(*args, **kwargs)
            except Exception as ex:
                print(ex)
            # return func(token, *args, **kwargs)

        return wrapped_function

    return logging_decorator


def login(username, password):

    """JWT登录

    Returns:
        _type_: RequestsCookieJar
    """
    url = "http://account-test.{host_n}/login"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "http://account-test.{host_n}",
        "Referer": "http://account-test.{host_n}/login",
    }
    data = "username=%s&password=%s" % (username, password)
    response = requests.request(
        "POST", url, headers=headers, data=data, allow_redirects=False
    )

    print(response.text)
    print(response.status_code)
    print(response.cookies)
    print(response.url)
    return response.cookies


def login4(cookies=None, env="dev"):
    """业务后台登录

    Args:
        cookies (_type_, RequestsCookieJar): JWT cookies. Defaults to None.

    Raises:
        Exception: 重定向获取token失败，抛出异常

    Returns:
        _type_: str
    """
    env = env + "-" if env else ""
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Referer": "https://%s{host_part_sg}.{host_sr}/" % env,
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
    }

    url = (
        "https://%scustomer-{host_part_sg}.{host_sr}/oauth2/login?domain=https://%s{host_part_sg}.{host_sr}/&feCallBackUrl=/home_page"
        % (env, env)
    )
    response = requests.get(
        url,
        headers=headers,
        cookies=cookies,
        allow_redirects=False,
    )
    print(response)
    print(response.cookies)
    print(response.headers)
    print(response.url)

    redirect = response.headers["Location"]
    print(redirect)
    token = None
    while True:
        print("==== REDIRECT ====> %s" % redirect)
        response = requests.get(
            redirect,
            headers=headers,
            cookies=cookies,
            allow_redirects=False,
        )
        cks = response.cookies.get_dict()
        if "token" in cks:
            print("token: %s" % cks["token"])
            token = cks["token"]
            break
        redirect = response.headers["Location"]
        if not redirect:
            raise Exception("token not found")
    return token


def login_and_save_token(env="dev"):
    config = Config("config.json").config
    if "token2" in config:
        return config["token2"]
    username = config["username_biz"]
    password = config["password_biz"]
    cookies = login(username, password)
    token = login4(cookies)
    print(token)
    if token:
        config["token2"] = token
        Config.dump(config)
        return token
    else:
        print("登录失败")
        raise Exception("登录失败，token is None")


def clear_token():
    config = Config("config.json").config
    config["token2"] = None
    Config.dump(config)


@relogin()
def robot_list(token, env="dev"):
    env = env + "-" if env else ""
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Origin": "https://%s{host_part_sg}.{host_sr}" % env,
        "Referer": "https://%s{host_part_sg}.{host_sr}/" % env,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "token": token,
        "x-requested-with": "XMLHttpRequest",
    }

    url = "https://api-gate-%sdelivery.${host_l}/web/transport/c/robot/down/list" % env
    
    response = requests.get(
        url,
        headers=headers,
    )
    return response.content.decode("utf-8")


def pretty_status(data):
    robotId = data["robotId"] if "robotId" in data else ""
    robotStatus = data["robotStatus"] if "robotStatus" in data else ""
    available = data["available"] if "available" in data else ""
    battery = data["battery"] if "battery" in data else ""
    online = data["online"] if "online" in data else ""
    bizVersion = data["bizVersion"] if "bizVersion" in data else ""
    navVersion = data["navVersion"] if "navVersion" in data else ""
    areaName = data["areaName"] if "areaName" in data else ""
    waitingStation = data["waitingStation"] if "waitingStation" in data else ""
    ota = data["ota"] if "ota" in data else ""
    navOta = data["navOta"] if "navOta" in data else ""
    boxOta = data["boxOta"] if "boxOta" in data else ""
    customerName = data["customerName"] if "customerName" in data else ""
    warn = data["warn"] if "warn" in data else ""
    deployDone = data["deployDone"] if "deployDone" in data else ""
    boxSize = data["boxSize"] if "boxSize" in data else ""
    preemptBoxSize = data["preemptBoxSize"] if "preemptBoxSize" in data else ""
    boxIndexes = data["boxIndexes"] if "boxIndexes" in data else ""
    print(
        """
    ID：\t\t%s
    状态：\t\t%s
    可用：\t\t%s
    电量：\t\t%s
    在线：\t\t%s
    业务版本：\t\t%s
    导航版本：\t\t%s
    楼宇：\t\t%s
    待命点：\t\t%s
    OTA：\t\t%r
    导航OTA：\t\t%r
    业务OTA：\t\t%r
    企业账户：\t\t%s
    警告：\t\t%s
    部署完成：\t\t%s
    箱格数：\t\t%s
    预留箱格：\t\t%s
    箱格位置：\t\t%s
          """
        % (
            robotId,
            robotStatus,
            available,
            battery,
            online,
            bizVersion,
            navVersion,
            areaName,
            waitingStation,
            ota,
            navOta,
            boxOta,
            customerName,
            warn,
            deployDone,
            boxSize,
            preemptBoxSize,
            boxIndexes,
        )
    )


def status_parser(datas, robotId=None):
    if robotId:
        pretty_status(datas["data"])
    else:
        status = datas["data"]["list"]
        for robot in datas["data"]["list"]:
            print('------------ robot status ------------')
            pretty_status(robot)


@relogin(h=status_parser)
def new_status(token, robotId=None, env="dev"):

    env = env + "-" if env else ""
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Origin": "https://%s{host_part_sg}.{host_sr}" % env,
        "Referer": "https://%s{host_part_sg}.{host_sr}/" % env,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        "sec-ch-ua-mobile": "?0",
        "token": token,
        "sec-ch-ua-platform": '"macOS"',
        "x-requested-with": "XMLHttpRequest",
    }

    params = {
        "pageNo": "1",
        "pageSize": "20",
    }
    if robotId:
        url = (
            "https://api-gate-%sdelivery.${host_l}/web/transport/c/robot/detail/rm?robotId=%s"
            % (env, robotId)
        )
    else:
        url = (
            "https://api-gate-%sdelivery.${host_l}/business-order/web/transport/c/robot/rm"
            % env
        )
    # print(url)
    response = requests.get(
        url,
        headers=headers,
        params=params,
    )
    return response.content.decode("utf-8")


@relogin()
def new_restore(token, robotId, env="dev"):
    env = env + "-" if env else ""
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://%s{host_part_sg}.{host_sr}" % env,
        "Referer": "https://%s{host_part_sg}.{host_sr}/" % env,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "token": token,
        "x-requested-with": "XMLHttpRequest",
    }

    json_data = {
        "robotId": robotId,
    }

    url = "https://api-gate-%sdelivery.${host_l}/web/transport/c/robot/restore" % env
    
    response = requests.post(
        url,
        headers=headers,
        json=json_data,
    )
    return response.content.decode("utf-8")


@relogin()
def new_available(token, robotId, available, env="dev"):
    env = env + "-" if env else ""
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://%s{host_part_sg}.{host_sr}" % env,
        "Referer": "https://%s{host_part_sg}.{host_sr}/" % env,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "token": token,
        "x-requested-with": "XMLHttpRequest",
    }

    json_data = {
        "robotId": robotId,
        "available": available,
    }

    url = (
        "https://api-gate-%sdelivery.${host_l}/web/transport/c/robot/config/available"
        % env
    )
    print(url)
    print(json_data)
    response = requests.post(url, headers=headers, json=json_data)
    return response.content.decode("utf-8")


if __name__ == "__main__":
    # login_and_save_token()
    # print(new_restore('EVT6-2-1'))
    # print(new_available('EVT6-2-1'))
    # print(new_arrive('EVT6-2-1'))
    # p("hello", robotId="EVT6-2-2")

    # token = login_and_save_token()
    # print(token)
    # robot_list()
    # new_status()
    # new_restore("EVT8-7")
    new_available("EVT8-7")
