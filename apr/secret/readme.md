
# 替换敏感信息方案

----

> 代码中一些token，host等敏感信息，需要隐去。使用此工具可以实现隐藏于恢复

### 使用方法
- 在含有敏感信息的目录，简历private文件夹并加入到`.gitignore`文件
- 在private目录下方式sub文件
- 将需要替换的文字已键值对形式放入sub，每一对一行
形式如：
```
private,public
private1,public2
```

### 替换
`./remove_sensitive.sh <path> <file_ext> sub`

### 恢复
`./remove_sensitive.sh <path> <file_ext> res`