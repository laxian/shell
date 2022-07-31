# Paste

## Usage

`paste [-s] [-d delimiters] file ...`

命令比较简单，作用是合并文件，只有两个选项：
`-s`，合并成单行，可以理解成single-line
`-d`，delimiters，如果指定了`-s`，`-d`指定分隔符，默认`\t`

## Practice

先创建两个文件：

```Bash
> echo {a..g} | tr ' ' '\n' > a
> echo {1..9} | tr ' ' '\n' > b
> cat a
a
b
c
d
e
f
g
> cat b
1
2
3
4
5
6
7
8
9
```

### 1. 合并a、b

```Bash
> paste a b
a       1
b       2
c       3
d       4
e       5
f       6
g       7
        8
        9
```

### 2. 合并成单行

```Bash
> paste -s a b
a       b       c       d       e       f       g
1       2       3       4       5       6       7       8       9
```

### 3. 各自合并成单行，指定分隔符

```Bash
> paste -sd, a b
a,b,c,d,e,f,g
1,2,3,4,5,6,7,8,9
```

### 4. 合并成单行

- 从标准输入获取输入

```Bash
> paste -sd, a b | paste -sd, -
a,b,c,d,e,f,g,1,2,3,4,5,6,7,8,9
```

### 5. 进程替换

```Bash
> paste -sd, <(echo a;echo b)
a,b
```
