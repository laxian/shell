# OCR方式统计视频延迟

> 统计三方视频推拉流延迟，如果没有第三方提供工具，很难大量的采集统计延迟数据。录屏截图的方式，人工计算延迟，效率太低。使用OCR方式识别时间并代码计算的方式，可以大大提高效率。

## 延迟统计方法

电脑屏幕作为推流内容，和拉流终端，屏幕上的秒表，同时也出现在拉流窗口。
录屏或截图，每一帧图片上两个秒表的时间差，即视频的全链路延迟。

如图：

![1_frame_00001](https://raw.githubusercontent.com/laxian/picgo-picbed/main/images/1_frame_00001.jpg)
图1

## OCR识别方案

### 1. 在线API

使用百度AI在线API，将图片base64编码后作为参数传入，通过云端识别，返回识别结果。

```Bash
def ocr(img_path: str) -> list:
    '''
    根据图片路径，将图片转为文字，返回识别到的字符串列表

    '''
    # 请求头
    headers = {
        'Host': 'cloud.baidu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.76',
        'Accept': '*/*',
        'Origin': 'https://cloud.baidu.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://cloud.baidu.com/product/ocr/general',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    }
    # 打开图片并对其使用 base64 编码
    with open(img_path, 'rb') as f:
        img = base64.b64encode(f.read())
    data = {
        'image': 'data:image/jpeg;base64,'+str(img)[2:-1],
        'image_url': '',
        'type': 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic',
        'detect_direction': 'false'
    }
    # 开始调用 ocr 的 api
    response = requests.post(
        'https://cloud.baidu.com/aidemo', headers=headers, data=data)

    # 设置一个空的列表，后面用来存储识别到的字符串
    ocr_text = []
    result = response.json()['data']
    if not result.get('words_result'):
        return []

    # 将识别的字符串添加到列表里面
    for r in result['words_result']:
        text = r['words'].strip()
        ocr_text.append(text)
    # 返回字符串列表
    return ocr_text
```

### 2. 离线OCR

使用百度paddleocr，离线运行，速度更快。

安装paddleocr：

```Bash
pip install paddleocr
```

使用：

```Bash
from paddleocr import PaddleOCR
ocr=PaddleOCR(use_angle_cls = True,use_gpu= False)
text=ocr.ocr(img_path, cls=True)
```

### 整体流程

#### 1. 录制视频

录制视频，需要保证两点：

1. 视频上最好不要有多余文字
2. 尽量清晰

参考图1

#### 1. 视频转图片

方式不限，建议使用ffmpeg，比较方便

下面的命令，文件格式指定数字5位，不足的左边补0，格式bmp（无压缩，体积大）
也可以jpg等格式。paddleocr jpg识别不好，然而API的方式需要网络传输，jpg方式速度很快，识别效果也不错。

```Bash
ffmpeg -i $VIDEO -r 5 -f image2 $OUTPUT_DIR/1_frame_%05d.bmp
```

#### 2. OCR识别与筛选

识别的图片，有些识别的不准确，需要保证移除调不准确的输入，
可以在计算前，根据正则，移除掉不准确的数据。

比如，时间格式：00:00:01.123

```Bash
^(\d{2}[:.]){3}\d{2,}$
```

#### 3. 结果展现

对于识别良好的时间戳，每张图是一对时间，经过计算，得出一个毫秒时间差。
最终输出格式:
00:00:01.123,00:00:01.223,100

过滤掉OCR过程中的debug信息：

```Bash
grep -E ^(\d{2}[:.]){3}\d{3},(\d{2}[:.]){3}\d{3},\d{2,}$
```

结果如下：

![20220902142612](https://raw.githubusercontent.com/laxian/picgo-picbed/main/images/20220902142612.png)
图2

如果需要统计，可以重定向保存到文件

```Bash
python paddle_ocr.py $OUTPUT_DIR | grep -E "^(\d{2}[:.]){3}\d{3},(\d{2}[:.]){3}\d{3},\d{3}$" > delay.csv
```

如图：

![20220902142735](https://raw.githubusercontent.com/laxian/picgo-picbed/main/images/20220902142735.png)
图3
