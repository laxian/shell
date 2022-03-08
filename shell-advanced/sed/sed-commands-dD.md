# sed 删除命令

## 位置和区间

位置可以是匹配的行，或两个位置组成的区间。

- 删除1到10行

`sed -e '1,10d' ex1`

- 删除档内第 1 行到含"ninebot" 字串的资料行 , 则指令为:

`sed -e '10,/ninebot/d' ex1`

### 位置规则说明

- 地址定位，为十进制行数，或者正则表达式
- 每个正则匹配必须在//中间
- 地址可以是一个代表当前行；也可以是两个，代表区间
- `$`可代表最后一行，删除最后一行`$d`；
- 地址后跟`!`，表示取反，单行和区间都能取反

可以推断，删除hello到world的行：

`sed -e '/hello/,/world/d' ex1`

删除最后一行：

`sed -e '$d'`

## 位置取反

删除所有，除了最后一行：

`sed -e '$!d'`

删除所有，除了/hello/匹配的行
`sed -e '/hello/!d'`

删除所有，除了/hello/,/world/匹配的区间

`sed -e '/hello/,/world/!d' ex1`

## d、D区别

d删除模式空间匹配行，立即开始下一个循环
D删除模式空间匹配直到第一个换行符，也就是第一行，然后立即开始下一个循环

### Sample

有一个文件如下：

```shell
this is the 1 line

this is the 2 line


this is the 3 line



this is the 4 line




this is the 5 line





this is the 6 line
```

期望如下：

```Bash
this is the 1 line

this is the 2 line

this is the 3 line

this is the 4 line

this is the 5 line

this is the 6 line
```

命令如下：

`sed -e '/^$/{N;/^\n$/D}' dD`

使用D，每次读到连续两行空行，就会删除一行，然后重新开始。

假如使用d，得到输出：

```Bash
this is the 1 line

this is the 2 line
this is the 3 line

this is the 4 line
this is the 5 line

this is the 6 line
```

因为每次匹配到两行空行，全部删除，所以偶数倍空行都被删除了，但奇数倍空行，留下一行。
