# sed Command-Line Options

## 常用

`-n`
`--quiet`
`--silent`

不输出模式空间内容到控制台，默认输出

`-e script`
`--expression=script`

命令行指定脚本，字符串脚本

`-f script-file`
`--file=script-file`

指定文件脚本

`-i[SUFFIX]`
`--in-place[=SUFFIX]`

`in-place`，原地修改，简单的说就是，直接在输入文件上修改。请确保被修改文件有备份或者版本控制

`-E`
`-r`
`--regexp-extended`

使用扩展的正则表达式（ERE），默认BRE。

### BRE/ERE

`BRE`和ERE的为一区别就是特殊字符  .?$+(){}| 等
`BRE`时，他们没有特殊含义，就是字符本身
`ERE`时，他们都是特殊字符，转义后才是本义

## 其他

`-l N`
`--line-length=N`

指定line-wrap长度，也就是自动换行长度。0代表不换行，默认70

`-b`
`--binary`

二进制模式，和回车换行符处理有关

`--follow-symlinks`

配合-i使用，跟随符号链接直到最终目的

`-s`
`--separate`

`sed`可以指定多个文件输入，并把它们作为同一个长流。指定此选项后，地址取件如：/abc/,/def/不能跨越文件，$ 不再是流的最后一行，而是每个文件的最后一行。行号是相对于每个文件的相对行号。

`--sandbox`

在沙盒模式下， e/w/r命令被拒绝 - 包含它们的程序将被中止而不运行。沙盒模式确保sed 只对命令行指定的输入文件进行操作，不能运行外部程序。

`-u`
`--unbuffered`
尽可能少地缓冲输入和输出。（如果输入来自 'tail -f'，并且您希望尽快看到转换后的输出。）

`-z`
`--null-data`
`--zero-terminated`

将输入视为一组行，每行以零字节（ASCII 'NUL' 字符）而不是换行符。此选项可与'sort -z' 和 'find -print0' 之类的命令一起使用处理任意文件名。

`--debug`

输出程序执行信息

------

如果没有指定-e, -f, --expression, or --file，第一个非option输入将被视为被执行脚本，也就是-e是可选的。输入文件后剩余的输入项，也被视为输入文件。
