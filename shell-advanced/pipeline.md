# 管道

## 如何让你的脚本支持管道？

最简示例：

```Bash
function repeatit {
	cat
}
echo hello | repeatit
```

OR

```Bash
function repeatit {
	cat /dev/stdin
}
echo hello | repeatit
```

哈哈，是不是就明白了，管道其实就是标准输入

参考：

https://unix.stackexchange.com/questions/301426/bash-function-that-accepts-input-from-parameter-or-pipe/301432

https://www.thinbug.com/q/34497884
