// ==UserScript==
// @name         Lexiang auto play
// @namespace    weixian.zhou@ninebot.com
// @version      0.1
// @description  auto play lexiang.com course, course_list by xpath
// @description  https://lexiangla.com/classes?category_id=&company_from=d05406eccd0b11ea8bac5254002f1020&page=2
// @author       weixian.zhou@ninebot.com
// @match        https://lexiangla.com/*
// @grant        none
// ==/UserScript==

(function () {
    'use strict';

    // Your code here...
    var course_list = ["https://lexiangla.com/classes/79d62ba4008911eba6e152540005f435?type=0&company_from=d05406eccd0b11ea8bac5254002f1020",
        "https://lexiangla.com/classes/33515eb8fe2411eab32252540005f435?type=0&company_from=d05406eccd0b11ea8bac5254002f1020",
        "https://lexiangla.com/classes/d43d8e90fd5d11ea874152540005f435?type=0&company_from=d05406eccd0b11ea8bac5254002f1020",
        "https://lexiangla.com/classes/decff072fc9111ea835052540005f435?type=0&company_from=d05406eccd0b11ea8bac5254002f1020",
        "https://lexiangla.com/classes/4a7987e4fbce11ea828552540005f435?type=0&company_from=d05406eccd0b11ea8bac5254002f1020",
        "https://lexiangla.com/classes/659893c6f97111eab65152540005f435?type=0&company_from=d05406eccd0b11ea8bac5254002f1020",
        "https://lexiangla.com/classes/0a75b1aef8a411eaab0752540005f435?type=0&company_from=d05406eccd0b11ea8bac5254002f1020",
        "https://lexiangla.com/classes/45bb940ef7dc11eab10752540005f435?type=0&company_from=d05406eccd0b11ea8bac5254002f1020",
        "https://lexiangla.com/classes/b6109752f71111ea926752540005f435?type=0&company_from=d05406eccd0b11ea8bac5254002f1020",
        "https://lexiangla.com/classes/8b50f454f64811ea9c7052540005f435?type=0&company_from=d05406eccd0b11ea8bac5254002f1020",
        "https://lexiangla.com/classes/9ea3bfc4f3f911eab4e252540005f435?type=0&company_from=d05406eccd0b11ea8bac5254002f1020",
        "https://lexiangla.com/classes/b096d75af31f11ea9e2552540005f435?type=0&company_from=d05406eccd0b11ea8bac5254002f1020",
        "https://lexiangla.com/classes/45c6ebf6f26e11eaa54452540005f435?type=0&company_from=d05406eccd0b11ea8bac5254002f1020",
        "https://lexiangla.com/classes/8c7ca9e2f19111ea8dfd52540005f435?type=0&company_from=d05406eccd0b11ea8bac5254002f1020",
        "https://lexiangla.com/classes/935a3510f0cc11eaa41652540005f435?type=0&company_from=d05406eccd0b11ea8bac5254002f1020",
        "https://lexiangla.com/classes/db4da1f8ee7a11ea8d8752540005f435?type=0&company_from=d05406eccd0b11ea8bac5254002f1020",
        "https://lexiangla.com/classes/87c362eced9f11eab90b52540005f435?type=0&company_from=d05406eccd0b11ea8bac5254002f1020",
        "https://lexiangla.com/classes/59d5326aecdd11ea9b3052540005f435?type=0&company_from=d05406eccd0b11ea8bac5254002f1020",
        "https://lexiangla.com/classes/94f9bceeec1511ea829252540005f435?type=0&company_from=d05406eccd0b11ea8bac5254002f1020",
        "https://lexiangla.com/classes/39963aa8eb4811eab71c52540005f435?type=0&company_from=d05406eccd0b11ea8bac5254002f1020",
        "https://lexiangla.com/classes/418d075ae90e11eabda952540005f435?type=0&company_from=d05406eccd0b11ea8bac5254002f1020",
        "https://lexiangla.com/classes/81a6c226e8f611ea95cd52540005f435?type=0&company_from=d05406eccd0b11ea8bac5254002f1020",
        "https://lexiangla.com/classes/c1d9c446e8de11eaa96052540005f435?type=0&company_from=d05406eccd0b11ea8bac5254002f1020",
        "https://lexiangla.com/classes/9e43e11ae86611eab96f52540005f435?type=1&company_from=d05406eccd0b11ea8bac5254002f1020",
        "https://lexiangla.com/classes/723468c0e7fc11eabb6b52540005f435?type=1&company_from=d05406eccd0b11ea8bac5254002f1020",
        "https://lexiangla.com/classes/4980839ce6d411eabc6b52540005f435?type=1&company_from=d05406eccd0b11ea8bac5254002f1020",
        "https://lexiangla.com/classes/ea05017ae60d11ea935d52540005f435?type=0&company_from=d05406eccd0b11ea8bac5254002f1020",
        "https://lexiangla.com/classes/3a1a169ee3ae11ea93b452540005f435?type=0&company_from=d05406eccd0b11ea8bac5254002f1020",
        "https://lexiangla.com/classes/a9eeb482e2e311ea935652540005f435?type=0&company_from=d05406eccd0b11ea8bac5254002f1020",
        "https://lexiangla.com/classes/4ee2fdf0e21611eab0dd52540005f435?type=1&company_from=d05406eccd0b11ea8bac5254002f1020",
        "https://lexiangla.com/classes/25d19e86e14d11eabef652540005f435?type=0&company_from=d05406eccd0b11ea8bac5254002f1020",
        "https://lexiangla.com/classes/c4a810d4e08611ea877652540005f435?type=0&company_from=d05406eccd0b11ea8bac5254002f1020",
        "https://lexiangla.com/classes/a785075ade3311ea9a7052540005f435?type=0&company_from=d05406eccd0b11ea8bac5254002f1020",
        "https://lexiangla.com/classes/1b3895b8dd6211ea987e52540005f435?type=0&company_from=d05406eccd0b11ea8bac5254002f1020",
        "https://lexiangla.com/classes/1e3e08b0dca411ea961452540005f435?type=0&company_from=d05406eccd0b11ea8bac5254002f1020",
        "https://lexiangla.com/classes/2c4fc732dbd111ea850f52540005f435?type=0&company_from=d05406eccd0b11ea8bac5254002f1020",
        "https://lexiangla.com/classes/fe13f702db0e11ea922052540005f435?type=0&company_from=d05406eccd0b11ea8bac5254002f1020",
        "https://lexiangla.com/classes/716c8598da3d11ea9ebd52540005f435?type=0&company_from=d05406eccd0b11ea8bac5254002f1020",
        "https://lexiangla.com/classes/d9bbc120cd0b11ea86fc5254002f1020?type=0&company_from=d05406eccd0b11ea8bac5254002f1020",
        "https://lexiangla.com/classes/d99b54b2cd0b11ea8a0c5254002f1020?type=0&company_from=d05406eccd0b11ea8bac5254002f1020"]

    var index = course_list.indexOf(document.location.href);
    var nextUrl = course_list[index];
    console.log(`当前播放第${index}课`);

    var retryClick = ()=>{
        var btn = document.getElementsByClassName("vjs-big-play-button")[0];
        if(btn) {
            document.getElementsByClassName("vjs-big-play-button")[0].click();console.log("click");
        }
    }

    var playNext = function () {
            console.log(`即将播放${nextUrl}`);
            window.location.href = nextUrl;
    }


    // 延时两秒自动点击开始播放
    setTimeout(retryClick, 2000);

    setInterval(function(){
        var tips = document.getElementsByClassName("time-tip-container")[0].innerText.trim();
        if(tips == "已学完本课程") {
            playNext();
        } else {
            console.log(tips);
        }
    }, 5000);

    setTimeout(function () {
        //document.getElementsByTagName("video")[0].play();
        var video=document.getElementsByTagName("video")[0];
        var cnt=0;
        video.oncanplay = function(){
            console.log("准备就绪");
        };
        video.addEventListener("ended", playNext);
        video.addEventListener("progress", function () {
            console.log(video.currentTime);
            cnt++;
            if(cnt > 5 && video.currentTime == 0) {
                window.location.reload();
            }
        });
    }, 5000);

})();