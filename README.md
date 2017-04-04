---
title: Markdown转\LaTeX 工具\\使用说明
author: 机智的超立方体
---

# 概述

这个工具可以简化编写日常的报告的工作量，避免繁重的键入\LaTeX 命令的工作（其实主要是嫌用文本编辑器插图太麻烦），代之以友好易读的[Markdown](http://daringfireball.net/projects/markdown/)格式。

这个工具基于[`mistune`](https://github.com/lepture/mistune)库，通过为其编写新的Renderer实现了\LaTeX 代码输出。输出一般来说仅需[C\TeX](http://www.ctex.org/)即可编译，其中所使用的纸张版式（`a4paper, 12pt, margin=54pt`）、宏包、插图格式等为开发者个人偏好。如果你习惯的设置与我不同，可自行修改程序源码中内嵌的模板。

欢迎任何意见或建议～

# 用法

`md2LaTeX < <input file> > <output file>`

`cat <input file> | markdown2latex | tee <output file>`

懒得做命令行选项，就当个管道用就好了。

# 语法

## 头部信息

输入的文件开头必须有如下片段：

```
---
title: 标题
author: 作者
---
```

## Markdown

与Markdown语法没什么区别的：

- 各级标题分别会生成对应的`section`，`subsection`等标题；
- 引用生成`quote`；
- 水平线生成`hrule`；
- 列表视是否有序生成`enumerate`或`itemize`；
- *强调*生成`emph`，**双重强调**生成`textbf`和`emph`；
- 行内代码生成`texttt`；
- 链接生成`href`；

## 块代码

块代码有三种写法：

```Markdown
一段被框起来、无语法高亮、有编号的程序：
\```
a = b + c;
\```

一段被框起来、有语法高亮、有编号的程序：
\```C
a = b + c;
\```

引入一个外部文件，带语法高亮，以文件名作为程序片段的标题（注意中间的空行是必需的）：
\```C[program.c]

\```
```

## 图

如果要直接在当前位置插入有编号和标题（标题可省略不写）的图：

```Markdown
这段话下面需要两张图。

![](foo.png "标题")

![](bar.png)

这是图之后的段落。
```

这会产生带有`[H]`参数的插图，它一定被固定在插入的位置。

而如果一段文字中需要提到某张图：

```Markdown
这一段文字提到了图![a_figure](foo.png "标题")和图![another_figure](bar.png)。
```

这会产生带有`[htbp]`参数的浮动图像，它将会出现在文字附近合适的地方，文字中则会产生交叉引用。上面这个例子最终排版结果将类似于“这一段文字提到了图3和图4。”

## 其他

程序会对文本中出现的`_`等符号进行转义，以确保它们正常显示。除非位于两个`$`之间---这种情况下转义会干扰数学公式的上标下标。

程序不会对`\`符号进行转义，以方便在文本中插入一些简单的\LaTeX 命令（……`一些简单的\LaTeX 命令`）。

*脚注*支持的不太好，就不讲了。

*表格*暂时不支持。