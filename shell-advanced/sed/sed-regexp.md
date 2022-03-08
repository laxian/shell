# sed 正则文字匹配

## 正则符号

| 符号 | 解释                                                                                                                                                     |
| ---- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ?    | 匹配前面的子表达式零次或一次，或指明一个非贪婪限定符。要匹配 ? 字符，请使用 \?。                                                                         |
| +    | 匹配前面的子表达式一次或多次。要匹配 + 字符，请使用 \+。                                                                                                 |
| \|   | 指明两项之间的一个选择。要匹配 \| ，请使用 \\\|。                                                                                                        |
| ( )  | 标记一个子表达式的开始和结束位置。子表达式可以获取供以后使用。要匹配这些字符，请使用 \( 和 \)。                                                          |
| { }  | 标记限定符表达式的开始结束。要匹配 {，请使用 \{。}，请使用\}                                                                                             |
| $    | 匹配输入字符串的结尾位置。如果设置了 RegExp 对象的 Multiline 属性，则\$也匹配 '\n' 或 '\r'。要匹配 \$ 字符本身，请使用 \\$。                             |
| *    | 匹配前面的子表达式零次或多次。要匹配 * 字符，请使用 \*。                                                                                                 |
| .    | 匹配除换行符 \n 之外的任何单字符。要匹配 . ，请使用 \. 。                                                                                                |
| [ ]  | 标记一个中括号表达式的开始。要匹配 [，请使用 `\[`，`\]` 请使用\]                                                                                         |
| \    | 将下一个字符标记为或特殊字符、或原义字符、或向后引用、或八进制转义符。例如， 'n' 匹配字符 'n'。'\n' 匹配换行符。序列 '\\' 匹配 "\"，而 '\(' 则匹配 "("。 |
| ^    | 匹配输入字符串的开始位置，除非在方括号表达式中使用，当该符号在方括号表达式中使用时，表示不接受该方括号表达式中的字符集合。要匹配 ^ 字符本身，请使用 \^。 |

## BRE 和 ERE

正则模式，唯一区别就是部分特殊符号的意义不同：‘?’, ‘+’, ‘()’, ‘{}’, 和 ‘|’，即`?+|(){}`

| 类型  | 说明                                                                               |
| ----- | ---------------------------------------------------------------------------------- |
| `BRE` | 符号本义，`\`转义后有特殊作用，sed默认是`BRE`                                      |
| `ERE` | 与`BRE`相反，特殊符号`\`转义后为符号本义。使用-E或-r,--regexp-extended 切换为`ERE` |

## 字符类和括号表达式

sed支持标准正则表达式的绝大部分，需要说明的是匹配数字的`\d`，在sed不起作用:
[why doesnt \d work in sed](https://stackoverflow.com/questions/14671293/why-doesnt-d-work-in-regular-expressions-in-sed)

可以使用一下方式替代：
[0-9]
\[[:digit:]]

这就是括号表达式。

0-9

a-z

‘[:alnum:]’
Alphanumeric characters: ‘[:alpha:]’ and ‘[:digit:]’; in the ‘C’ locale and ASCII character encoding, this is the same as ‘[0-9A-Za-z]’.

‘[:alpha:]’
Alphabetic characters: ‘[:lower:]’ and ‘[:upper:]’; in the ‘C’ locale and ASCII character encoding, this is the same as ‘[A-Za-z]’.

‘[:blank:]’
Blank characters: space and tab.

‘[:cntrl:]’
Control characters. In ASCII, these characters have octal codes 000 through 037, and 177 (DEL). In other character sets, these are the equivalent characters, if any.

‘[:digit:]’
Digits: 0 1 2 3 4 5 6 7 8 9.

‘[:graph:]’
Graphical characters: ‘[:alnum:]’ and ‘[:punct:]’.

‘[:lower:]’
Lower-case letters; in the ‘C’ locale and ASCII character encoding, this is a b c d e f g h i j k l m n o p q r s t u v w x y z.

‘[:print:]’
Printable characters: ‘[:alnum:]’, ‘[:punct:]’, and space.

‘[:punct:]’
Punctuation characters; in the ‘C’ locale and ASCII character encoding, this is ! " # $ % & ' ( ) * + , - . / : ; < = > ? @ [ \ ] ^ _ ` { | } ~.

‘[:space:]’
Space characters: in the ‘C’ locale, this is tab, newline, vertical tab, form feed, carriage return, and space.

‘[:upper:]’
Upper-case letters: in the ‘C’ locale and ASCII character encoding, this is A B C D E F G H I J K L M N O P Q R S T U V W X Y Z.

‘[:xdigit:]’
Hexadecimal digits: 0 1 2 3 4 5 6 7 8 9 A B C D E F a b c d e f.

### Collating symbols

只在特定Local有效，有些国家语言有多字符字母，作为一个整体
如\[[.ch.]]，用于匹配一些特殊的多符号。

不知道怎么翻译，这不是sed的概念，而是正则的一个概念，比较生僻。

[Regular Expressions](https://pubs.opengroup.org/onlinepubs/9699919799.2008edition/basedefs/V1_chap09.html)

[Regex collating symbols - StackOverFlow](https://stackoverflow.com/questions/35042202/regex-collating-symbols)

### Equivalence class

只在特定Local有效，如
[=a=] 标识一类等价字符 [aªáàâãäå...]

### Class symbol

[:digit:]
[:blank:]
...
等

## 捕获组

| 表达式         | 解释                                                       | sample        | 作用                  |
| -------------- | ---------------------------------------------------------- | ------------- | --------------------- |
| `()`           | 之内的捕获，会被缓存，通过\n（n∈1~99）获取。               |               |
| `(?:)`         | 非捕获组，可以让()不被缓存。                               |               |
| `(?=pattern)`  | 零宽正向先行断言(zero-width positive lookahead assertion)  | `re(?=gular)` | 匹配re，且后面是gular |
| `(?!pattern)`  | 零宽负向先行断言(zero-width negative lookahead assertion)  | `re(?!g)`     | 匹配re，且后面不是g   |
| `(?<=pattern)` | 零宽正向后行断言(zero-width positive lookbehind assertion) | `(?<=\w)re`   | 匹配re，且前是字母    |
| `(?<!pattern)` | 零宽负向后行断言(zero-width negative lookbehind assertion) | `(?<!\w)re`   | 匹配re，且前不是字母  |

## 限定符

| 表达式 | 解释                                                                                                                                                                     |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ?      | 匹配前面的子表达式零次或一次。例如，"do(es)?" 可以匹配 "do" 、 "does" 中的 "does" 、 "doxy" 中的 "do" 。? 等价于 {0,1}。                                                 |
| +      | 匹配前面的子表达式一次或多次。例如，'zo+' 能匹配 "zo" 以及 "zoo"，但不能匹配 "z"。+ 等价于 {1,}。                                                                        |
| *      | 匹配前面的子表达式零次或多次。例如，zo* 能匹配 "z" 以及 "zoo"。* 等价于{0,}。                                                                                            |
| {n}    | n 是一个非负整数。匹配确定的 n 次。例如，'o{2}' 不能匹配 "Bob" 中的 'o'，但是能匹配 "food" 中的两个 o。                                                                  |
| {n,}   | n 是一个非负整数。至少匹配n 次。例如，'o{2,}' 不能匹配 "Bob" 中的 'o'，但能匹配 "foooood" 中的所有 o。'o{1,}' 等价于 'o+'。'o{0,}' 则等价于 'o*'。                       |
| {n,m}  | m 和 n 均为非负整数，其中n <= m。最少匹配 n 次且最多匹配 m 次。例如，"o{1,3}" 将匹配 "fooooood" 中的前三个 o。'o{0,1}' 等价于 'o?'。请注意在逗号和两个数之间不能有空格。 |