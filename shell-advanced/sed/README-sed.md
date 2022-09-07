# sed 系列手册

## Docs

- [sed 命令行选项](https://github.com/laxian/shell/blob/dev/shell-advanced/sed/sed-options.md)

- [sed 命令总结](https://github.com/laxian/shell/blob/dev/shell-advanced/sed/sed-commands.md)

- [sed 命令之s/c/y命令](https://github.com/laxian/shell/blob/dev/shell-advanced/sed/sed-commands-scy.md)

- [sed 命令之d/D命令](https://github.com/laxian/shell/blob/dev/shell-advanced/sed/sed-commands-dD.md)

- [sed 正则匹配文字](https://github.com/laxian/shell/blob/dev/shell-advanced/sed/sed-regexp.md)

- [sed 行定位匹配](https://github.com/laxian/shell/blob/dev/shell-advanced/sed/sed-addresses.md)

- [sed 模式空间和保持空间](https://github.com/laxian/shell/blob/dev/shell-advanced/sed/sed-handlet-advance.md)

## Term

- 选项，option，如`-n`、`-r`
- 命令，command
  sed控制命令，如：`a`追加、`s`替换、`i`插入
- 行定位，addresses，指定命令操作的行，或者范围
- 模式空间/保持空间，pattern space/hold space

## END

本文系列文档整理过程，使用了正则表达式：

为匹配到前后和结尾不是`且包含：=:.{};\w\d\ []- 的匹配，加上加上代码样式

```Bash
^(?<!`)[=:\.\{\};/\w\d\\\s\]\[-]+(?!`)
```

替换为

```Bash
`$0`
```
