import requests


def api_broken(robotId, env='dev', errorCode=110123, msg='test'):
    params = (
        ('robotId', robotId),
        ('code', errorCode),
        ('msg', msg),
    )

    response = requests.get(
        'https://api-gate-%s-delivery.${host_part_2}.com/test/robot/simulation/error' % env, params=params)

    print(response.content.decode('utf-8'))
