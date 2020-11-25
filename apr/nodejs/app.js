
const fetch = require('node-fetch');

let wiki = "https://wiki.segwayrobotics.com/pages/viewpage.action?pageId=50280499";

let env = process.argv[2];
let version = process.argv[3] ? process.argv[3] : "2.x.x";


if ((env == "dev" || env == "release")) {
    if (env == "dev") {
        env = "测试";
    } else {
        env = "正式";
    }

    _sendMessage();
} else {
    console.log("参数错误");
}

function _sendMessage() {
    let timestamp = _timestamp();

    let content = `业务软件在<font color="info">${env}</font>环境下发布, 请相关同学注意 \n 
    >版本:${version}
    >更新日志:${wiki}
    >发布时间:${timestamp}`;

    fetch("https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=e67b06b1-08ff-4053-b8b3-496a40c6b363", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            "msgtype": "markdown",
            "markdown": {
                "content": content
            }
        })
    }).then(info => {
        console.log("发送成功");
    }).catch(error => {
        console.log(`发送失败 ${error}`);
    });
}

function _timestamp() {
    let date = new Date();
    return date.toLocaleString();
}
