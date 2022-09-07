# sed handlet advance

- [sed handlet advance](#sed-handlet-advance)
	- [常用命令/选项说明](#常用命令选项说明)
	- [行逆序](#行逆序)
	- [添加行号](#添加行号)
	- [字符集替换，1-5，替换成A-E](#字符集替换1-5替换成a-e)
	- [Python2 print convert to Python3 print](#python2-print-convert-to-python3-print)
	- [将LoadingButton行后第一次匹配到的mdw_isSupportLanguage替换成pbTextSubClass](#将loadingbutton行后第一次匹配到的mdw_issupportlanguage替换成pbtextsubclass)
	- [regex](#regex)
	- [REF](#ref)

## 常用命令/选项说明

| 命令 | 说明                                                                       |
| ---- | -------------------------------------------------------------------------- |
| h    | 将读取到模式空间的行，覆盖放入保持空间                                     |
| H    | 将读取到模式空间的行，追加放入保持空间                                     |
| 1!G  | 非第一行将保持空间追加到模式空间                                           |
| g    | 将保持空间覆盖到模式空间                                                   |
| $!d  | 非最后一行，删除模式空间                                                   |
| D    | 删除模式空间第一行，也就是删除第一个\n之前部分，然后重启循环而不读取新的行 |
| p    | 输出模式空间                                                               |
| P    | 输出模式空间第一行                                                         |
| x    | 交换空间P/H                                                                |
| -n   | quiet，流内容不打印。但p命令指定内容打印                                   |
| -i   | 文件内修改                                                                 |

## 行逆序

```Bash
seq 9 | sed -n '1!G;h;$!d;p'
seq 9 | sed -n '1!G;h;$p'
# outputs
9
8
7
6
5
4
3
2
1
```

推演：模式空间P，保持空间H

Round 1，第一行不执行G（1!G）

| 指令       | P   | H   |
| ---------- | --- | --- |
| 读取一行： | 1   |
| 执行h后：  | 1   | 1   |

Round 2

| 指令       | P    | H    |
| ---------- | ---- | ---- |
| 读取一行： | 2    | 1    |
| 执行G后：  | 2\n1 | 1    |
| 执行h后：  | 2\n1 | 2\n1 |
| 执行d后：  |      | 2\n1 |

Round 3

| 指令       | P       | H       |
| ---------- | ------- | ------- |
| 读取一行： | 3       | 2\n1    |
| 执行G后：  | 3\n2\n1 | 2\n1    |
| 执行h后：  | 3\n2\n1 | 3\n2\n1 |
| 执行d后：  |         | 3\n2\n1 |

Round $ 最后一行，不执行d（$!d）

| 指令       | P                         | H                         |
| ---------- | ------------------------- | ------------------------- |
| 读取一行： | 9                         | 8\n7\n6\n5\n4\n3\n2\n1    |
| 执行G后：  | 9\n8\n7\n6\n5\n4\n3\n2\n1 | 8\n7\n6\n5\n4\n3\n2\n1    |
| 执行h后：  | 9\n8\n7\n6\n5\n4\n3\n2\n1 | 9\n8\n7\n6\n5\n4\n3\n2\n1 |
| 执行p后：  | 输出P空间并删除           | 9\n8\n7\n6\n5\n4\n3\n2\n1 |

## 添加行号

```Bash
➜  seq 9 | sed -n '=;p' | sed 'N;s/\n/. /'
1. 1
2. 2
3. 3
4. 4
5. 5
6. 6
7. 7
8. 8
9. 9
```

`=`，打印行号

`N`，读取两行，中间有'\n'

`s/\n/. /` 将换行换成`.`

## 字符集替换，1-5，替换成A-E

```Bash
➜  seq 9 | sed 'y/12345/ABCDE/'
A
B
C
D
E
6
7
8
9
```

## Python2 print convert to Python3 print

```Bash
sed -i 's/\([^#]*[[:space:]]*\)print[[:space:]]\(.*\)/\1print(\2)/' `find . -name "*.py"`
```

匹配print，和print前后内容:`\1print\2`，转换成`\1print(\2)`

## 将LoadingButton行后第一次匹配到的mdw_isSupportLanguage替换成pbTextSubClass

```Bash
sed -n '/LoadingBu/{:x N;s/mdw_isSupportLanguage=\"true\"/pbTextSubClass=\"com.segway.robotic.module.widgets.SRTextView\"/;T x}'
```

## regex

正则
-r: use  extended regular expressions in the script
\1 ~ \9 捕获组
& 相当于\0，整体匹配

```Bash
echo "foobarbaz"| sed -r 's/^foo(.*)baz$/\1/' # 捕获组1：bar
echo hello|sed -r 's/hello/\1/'	# 报错
echo hello|sed -r 's/hello/\0/'	# hello
echo "foobarbaz"| sed -r 's/^foo(.*)baz$/\0/' #foobarbaz
echo "foobarbaz"| sed -r 's/^foo(.*)baz$/&/' #foobarbaz
echo "hello world"| sed 's/[a-z]*/(&)/' #(hello) world
echo "hello world"| sed 's/[a-z]*/(&)/g' #(hello) (world)
```

## REF

[gnu-sed](http://www.gnu.org/software/sed/manual/sed.html)

[cnblog](https://www.cnblogs.com/qyddbear/p/3405021.html)
