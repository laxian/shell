import requests
import json
from urllib.parse import urlparse
import os



IMAGE_HOST = "https://static.kejishou.net/wallpaper/"
LIST_HOST= "https://xcx.kejishou.net/wallpaper/api_v2.php"

def get_image_list(page):
	print(page)
	params=(
		('type', 'all'),
		('page', page)
	)
	response = requests.get(LIST_HOST, params=params)
	print(response.status_code)
	if response.status_code == 200:
		return response.content.decode('unicode_escape')


def parse_image_type_all(content):
	map = json.loads(content)
	list = map['list']
	return [ match_imagepath(x['thumbnail']) for x in list]

def match_imagepath(raw_path):
	return  raw_path.split('?')[0]

import requests

def download_img(url):
    # 下载图片
    r = requests.get(url, stream=True)
    result = urlparse(url)
    path = "./{}".format(result.path)
    os.makedirs(os.path.dirname("./{}".format(path)), exist_ok=True)
    print(r.status_code) # 返回状态码
    if r.status_code == 200:
        open(path, 'wb').write(r.content) # 将内容写入图片
        print("done")
    del r

def schedule():
	for i in range(1, 100):
		content = get_image_list(i)
		path_list = parse_image_type_all(content)
		print(path_list)

		for p in path_list:
			url = IMAGE_HOST+p
			download_img(url)
		print('success!')


if __name__ == '__main__':
    schedule()


