import requests
from src.log.api_login_new import relogin


deploy_status = {
    -1: "--",
    1: "部署中",
    2: "重新部署",
    3: "部署完成",
}

used_status = {
    -1: "--",
    1: "正常",
    2: "冻结",
    3: "解绑",
}

used_type = {
    -1: "未知",
    1: "客户租赁",
    2: "客户试用",
    3: "客户购买",
    4: "内部测试",
    5: "代理商测试",
}

pallet_type = {
    -1: "--",
    0: "圆盘",
    1: "方盘",
    2: "圆盘带壳",
    3: "方盘带壳",
}

task_status = {-1: "--", 2: "未知", 1: "闲置", 3: "不明"}


def status_parser(datas, robotId=None, **kwargs):
    print(robotId)
    if robotId:
        pretty_status(datas["data"])
    else:
        status = datas["data"]["list"]
    for robot in datas["data"]["list"]:
        print("------------")
        pretty_status(robot)


def pretty_status(data):
    robotId = data["robotId"] if "robotId" in data else ""
    shopId = data["shopId"] if "shopId" in data else ""
    shopName = data["shopName"] if "shopName" in data else ""
    countryName = data["countryName"] if "countryName" in data else ""
    cityName = data["cityName"] if "cityName" in data else ""
    usedType = data["usedType"] if "usedType" in data else ""
    deployStatus = data["deployStatus"] if "deployStatus" in data else ""
    usedMapName = data["usedMapName"] if "usedMapName" in data else ""
    palletType = data["palletType"] if "palletType" in data else ""
    onLine = data["onLine"] if "onLine" in data else ""
    taskStatus = data["taskStatus"] if "taskStatus" in data else ""
    remainingPower = data["remainingPower"] if "remainingPower" in data else ""
    currentVersion = data["currentVersion"] if "currentVersion" in data else ""
    usedStatus = data["usedStatus"] if "usedStatus" in data else ""
    print(
        """
    robotId:		%s
    shopId:		%s
    shopName:		%s
    countryName:	%s
    cityName:		%s
    usedType:		%s
    deployStatus:	%s
    usedMapName:	%s
    palletType:		%s
    onLine:		%s
    taskStatus:		%s
    remainingPower:   	%s
    currentVersion:   	%s
    usedStatus:		%s
          """
        % (
            robotId,
            shopId,
            shopName,
            countryName,
            cityName,
            used_type[usedType],
            deploy_status[deployStatus],
            usedMapName,
            pallet_type[palletType],
            onLine,
            task_status[taskStatus],
            remainingPower,
            currentVersion,
            used_status[usedStatus],
        )
    )


@relogin(h=status_parser)
def s1_list(token, env="dev"):
    return raw_s1_list(token, env)

    #     print(res)
    if res:
        robots = [l["robotId"] for l in res["data"]["list"]]
        # for robot in robots:
        print(robots)
    else:
        print(res)


def raw_s1_list(token, env="dev"):
    env = "-dev" if env == "dev" else ""
    url = (
        "https://restaurant%s.${host_l}/restaurant/robot/actual/list?page=1&pageSize=100000"
        % env
    )
    payload = {}
    if url.find("restaurant%s.${host_l}" % env):
        origin = "https://crss%s.{host_sr}" % env
    elif url.find("crss-oregon.${host_l}"):
        origin = "https://crss-oregon.${host_l}"
    else:
        print("Unknown URL: %s" % url)

    headers = {
        "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        "language": "zh-CN",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "authToken": token,
        "token": token,
        "withCredentials": "true",
        "sec-ch-ua-platform": '"macOS"',
        "Origin": origin,
    }

    response = requests.get(
        url,
        headers=headers,
    )
    print(url)
    #     print(response.content.decode("utf-8"))
    return response.content.decode("utf-8")


if __name__ == "__main__":
    s1_list("7a80f8275b7643a0aafb7c3328b59afe")
