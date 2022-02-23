# 爬取壁纸接口分析

## api

### 图片列表

请求接口：
https://xcx.kejishou.net/wallpaper/api_v2.php?type=all&page=1

返回数据：

```Json
{
	"code": 200,
	"msg": "\u83b7\u53d6\u6210\u529f",
	"list": [{
		"id": "2852",
		"thumbnail": "2021\/08\/20\/6.jpg?x-oss-process=image\/resize,m_lfit,h_812,limit_0\/crop,g_center,w_375\/format,jpg\/quality,q_90"
	}, {
		"id": "2851",
		"thumbnail": "2021\/08\/20\/5.jpg?x-oss-process=image\/resize,m_lfit,h_812,limit_0\/crop,g_center,w_375\/format,jpg\/quality,q_90"
	}, {
		"id": "2850",
		"thumbnail": "2021\/08\/20\/4.jpg?x-oss-process=image\/resize,m_lfit,h_812,limit_0\/crop,g_center,w_375\/format,jpg\/quality,q_90"
	}, {
		"id": "2849",
		"thumbnail": "2021\/08\/20\/3.jpg?x-oss-process=image\/resize,m_lfit,h_812,limit_0\/crop,g_center,w_375\/format,jpg\/quality,q_90"
	}, {
		"id": "2848",
		"thumbnail": "2021\/08\/20\/2.jpg?x-oss-process=image\/resize,m_lfit,h_812,limit_0\/crop,g_center,w_375\/format,jpg\/quality,q_90"
	}, {
		"id": "2847",
		"thumbnail": "2021\/08\/20\/1.jpg?x-oss-process=image\/resize,m_lfit,h_812,limit_0\/crop,g_center,w_375\/format,jpg\/quality,q_90"
	}, {
		"id": "2846",
		"thumbnail": "2021\/08\/17\/6.jpg?x-oss-process=image\/resize,m_lfit,h_812,limit_0\/crop,g_center,w_375\/format,jpg\/quality,q_90"
	}, {
		"id": "2845",
		"thumbnail": "2021\/08\/17\/5.jpg?x-oss-process=image\/resize,m_lfit,h_812,limit_0\/crop,g_center,w_375\/format,jpg\/quality,q_90"
	}, {
		"id": "2844",
		"thumbnail": "2021\/08\/17\/4.jpg?x-oss-process=image\/resize,m_lfit,h_812,limit_0\/crop,g_center,w_375\/format,jpg\/quality,q_90"
	}, {
		"id": "2843",
		"thumbnail": "2021\/08\/17\/3.jpg?x-oss-process=image\/resize,m_lfit,h_812,limit_0\/crop,g_center,w_375\/format,jpg\/quality,q_90"
	}],
	"index_collection": [{
		"thumbnail": "collections\/icon\/kejishou.png",
		"id": "3",
		"name": "\u79d1\u6280\u517d\u89c6\u9891\u4e2d\u7528\u8fc7\u7684\u58c1\u7eb8"
	}, {
		"thumbnail": "collections\/icon\/iOS13.png",
		"id": "1",
		"name": "\u9690\u85cfDock\u680f\u58c1\u7eb8"
	}]
}
```

### 图片地址

- host
https://static.kejishou.net/wallpaper/

- 图片地址
图片相对路径，列表的thmbnail部分，非贪婪匹配"*.jpg"部分。host+path就是图片路径

- 访问鉴权
无
