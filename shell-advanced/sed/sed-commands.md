# sed commands summary

## 所有命令

`a\`
`text`
在一行之后附加文本。

`a text`
在一行之后附加文本。

`b label`
无条件分支到label。

`c\`
`text`
用text替换匹配行。

`c text`
用文本替换行。

`d`
删除模式空间；立即开始下一个循环。

`D`
如果模式空间包含换行符，则删除模式空间中的文本直到第一个换行符，并使用生成的模式空间重新开始循环，而不读取新的输入行。
如果模式空间不包含换行符，则开始一个正常的新循环，就像d发出命令一样。

`e`
执行在模式空间中找到的命令并用输出替换模式空间；尾随换行符被抑制。
`printf '%s\n' ls pwd | sed e`

`e command`
执行command并将其输出发送到输出流。该命令可以跨多行运行，除了最后一行以反斜杠结尾。

`sed '1,2e echo found' ex1`

`F`
(filename) 打印当前输入文件的文件名（带有尾随换行符）。

输出文件名，并输出匹配行：
`sed -n '/hello/{F;p}' ex1`

`g`
将模式空间的内容替换为保持空间的内容。

`G`
将换行符附加到模式空间的内容，然后将保留空间的内容附加到模式空间的内容。

`h`
(hold) 用模式空间的内容替换保持空间的内容。

`H`
将换行符附加到保持空间的内容，然后将模式空间的内容附加到保持空间的内容。

`i\`
`text`
在一行之前插入文本。

`i text`
在一行之前插入文本。

`l n`
以明确的形式打印模式空间：不可打印的字符（和\字符）以 C 样式的转义形式打印；长行被分割，尾随\字符表示分割；每行的末尾都标有$。

`n`指定所需的换行长度；长度为 0（零）表示从不换行。如果省略，则使用命令行中指定的默认值。n 参数是一个 GNUsed扩展 。
`sed -n 'l 10' ex1`

`n`
(next) 如果未禁用自动打印，则打印模式空间，然后无论如何用下一行输入替换模式空间。如果没有更多输入，则sed退出而不处理任何更多命令。

`N`
将换行符添加到模式空间，然后将下一行输入附加到模式空间。如果没有更多输入，则sed退出而不处理任何更多命令。

`p`
打印模式空间。

`P`
打印模式空间，直到第一个换行符

`q[exit-code]`
(quit) 退出sed，不再处理任何命令或输入。

`Q[exit-code]`
(quit) 此命令与 相同q，但不会打印模式空间的内容。就像q，它提供了向调用者返回退出代码的能力。

`r filename`
读取文件filename。
`echo "hello \\\n world" | sed 'r ex1'`

`R filename`
在当前循环结束时或在读取下一个输入行时，将要读取文件的第一行插入到输出流中。
`sed -n '$R ex1' ex1`

`s/regexp/replacement/[flags]`
（替代）将正则表达式与模式空间的内容匹配。如果找到，将匹配的字符串 替换为replacement。
删除匹配的远程分支：
`git branch -r | sed "s;origin\/;;g" | grep wenjun | xargs -n1 -I L git push origin --delete L`

`t label`
跟随`s`命令，替换成功后使用`t`跳转到指定标签
`sed -e :a -e '$!N;s/\n  */ /;ta' -e 'P;D'`

`T label`
跟随`s`命令，替换失败后使用`T`跳转到指定标签

`v [version]`
(version) 此命令不执行任何操作，但sed如果不支持 GNUsed扩展，或者请求的版本不可用，则会失败。

`w filename`
将模式空间写入文件名。

`W filename`
将模式空间的部分写入给定文件名，直到第一个换行符

`x`
交换保持空间和模式空间的内容。

`y/src/dst/`
将模式空间中与任何source-chars匹配的任何字符与dest-chars中的相应字符进行音译。
`echo hello world | sed 'y/abcdefghij/0123456789/'`

`z`
(zap) 此命令清空模式空间的内容。

`\`#
行注释，直到下一个换行符。

`{ cmd ; cmd ... }`
将多个命令组合在一起。

`=`
打印当前输入的行号（带有尾随换行符）。

`: label`
指定分支命令 ( , , ) 的标签位置。b，t，T

## 高频命令

|命令   |注释   |sample     |
|---|---|---|
|a   |下一行追加   |sed '/repositories/a maven' build.gradle  |
|i   |上一行插入   |sed '/repositories/i #comment' build.gradle  |
|p   |输出匹配模式空间   |sed -n '/^hello/p' ex1 |
|d   |删除匹配行   |sed -n '/^hello/d' ex1  |
|s   |替换   |sed -n '/^hello/s/hello/world/g' ex1  |
|c   |替换行   |sed -n '/^hello/c world' ex1  |
