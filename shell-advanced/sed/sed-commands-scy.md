# sed 替换命令

## s命令

eg:
`s/regexp/replacement/flags`

### 规则说明

- s开头，'/'可替换为其他字符
- flag选项有：g、i/I、m/M、p、w、e
- 替换转义符符选项有：\u、\U、\l、\L、\E、\[0,9]
- s前可指定定位符：可以使匹配行，或匹配区间，默认为全部行

### flag

> flag可以多个组合

g
global，替换所有匹配

i/I
case-insensitive，忽略大小写

m/M
multi-line，多行匹配

p
print，打印替换后模式空间

w filename
替换成功后写入文件，作为gnu-sed扩展，支持两个特殊文件：/dev/stderr、/dev/stdout

e
将执行替换后模式空间作为指令执行，将执行结果替换模式空间
`echo ab | sed 's/\(ab\)/ls/e'`

### 转义符

\[0,9]
使用个位数字n，代替第n个匹配项

\u
将下一个字符转大写

\U
将其后字符都转大写，直到遇到\L，或\E

\l
将下一个字符转小写

\L
将其后字符都转小写，直到遇到\U，或\E

\E
\U、\L，会将其后的字符全部转大写，
\u、\l会将其后第一个字符转大写。如果其后有`\1`，但是`\1`为空匹配时，\u、\l会往后传递。
\E会终止这种传递。

如下：

```Bash
➜ echo a-b- | sed 's/\(b\?\)-/\u\1x/g'
aXBx
➜ echo a-b- | sed 's/\(b\?\)-/\u\1\Ex/g'
axBx
```

第一行代码：
第一次匹配到`-`，`\1`为空匹配，`\u`跳过`\1`，`x`变`X`。
第二次匹配到`b-`，`\1`为`b`，所以`\u`将`b`转为`B`

第二行代码：
第一次匹配到`-`，`\1`为空匹配，`\u`跳过`\1`，然后遇到`\E`，`x`不变。
第二次匹配到`b-`，一样

## c命令

使用指定字符串，替换匹配行

如下，使用world，替代匹配到hell的行

```Bash
➜ echo "hello\nworld" | sed '/hell/c world'
world
world
```

## y命令

y命令字符的替换，指定一个字符集，和一个同样长度的替换字符集，一一对应替换。

```Bash
$ echo hello world | sed 'y/abcdefghij/0123456789/'
74llo worl3
```
