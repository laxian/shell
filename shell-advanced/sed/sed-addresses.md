# sed Addresses selecting lines

在专题讲述s命令、和d命令时都用到了定位。其实不止，所有命令，都需要选择全部或某些行，作为操作对象。
这就用到定位。

## 数字定位

1p，输出第一行

## Regex

$!d 非尾行删除

/^$/d 删除空行

/hello$/,/^world$/s/l/L/g 从`hello`结尾的行，到`world`完全匹配的行，将`l`替换成`L`

变形写法：
\\%regexp%

%可用其他字符替代。
这种写法，在正则中大量使用`/`时非常有用：

```Bash
sed -n '/^\/home\/alice\/documents\//p'
sed -n '\%^/home/alice/documents/%p'
sed -n '\;^/home/alice/documents/;p'
```

## Range

1,100p 输出1到100行
2,3s/hello/world/ 2,3行hello替换成world
5~3d，从第5行开始，每3行一组删除最后一行
