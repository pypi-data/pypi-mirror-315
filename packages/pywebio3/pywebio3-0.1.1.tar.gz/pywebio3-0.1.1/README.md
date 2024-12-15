# pywebio3

pywebio的国产化替代版本，用法和pywebio完全一样

PyWebIO提供了一系列命令式的交互函数来在浏览器上获取用户输入和进行输出，将浏览器变成了一个“富文本终端”，可以用于构建简单的Web应用或基于浏览器的GUI应用。
PyWebIO还可以方便地整合进现有的Web服务，让你不需要编写HTML和JS代码，就可以构建出具有良好可用性的应用。

## 安装

```shell
pip install pyweboio3
```

## 功能特性

- 使用同步而不是基于回调的方式获取输入，代码编写逻辑更自然
- 非声明式布局，布局方式简单高效
- 代码侵入性小，旧脚本代码仅需修改输入输出逻辑便可改造为Web服务
- 支持整合到现有的Web服务，目前支持与Flask、Django、Tornado、aiohttp、FastAPI框架集成
- 同时支持基于线程的执行模型和基于协程的执行模型
- 支持结合第三方库实现数据可视化

## 使用案例

### 快速入门

这是一个使用PyWebIO计算 [BMI指数](https://en.wikipedia.org/wiki/Body_mass_index) 的脚本:

```python
from pywebio3.input import input, FLOAT
from pywebio3.output import put_text


def bmi():
    height = input("请输入你的身高(cm)：", type=FLOAT)
    weight = input("请输入你的体重(kg)：", type=FLOAT)

    BMI = weight / (height / 100) ** 2

    top_status = [(14.9, '极瘦'), (18.4, '偏瘦'),
                  (22.9, '正常'), (27.5, '过重'),
                  (40.0, '肥胖'), (float('inf'), '非常肥胖')]

    for top, status in top_status:
        if BMI <= top:
            put_text('你的 BMI 值: %.1f，身体状态：%s' % (BMI, status))
            break


if __name__ == '__main__':
    bmi()
```

### 作为Web服务提供

上文BMI程序会在计算完毕后立刻退出，可以使用 [
`pywebio.start_server()`](https://pywebio.readthedocs.io/zh_CN/latest/platform.html#pywebio.platform.tornado.start_server)
将 `bmi()` 函数作为Web服务提供：

```python
from pywebio3 import start_server
from pywebio3.input import input, FLOAT
from pywebio3.output import put_text


def bmi():  # bmi() 函数内容不变
    ...


if __name__ == '__main__':
    start_server(bmi, port=80)
```

## pywebio基础教程

PyWebIO提供了一系列命令式的交互函数来在浏览器上获取用户输入和进行输出，将浏览器变成了一个“富文本终端”，可以用于构建简单的Web应用或基于浏览器的GUI应用。
使用PyWebIO，开发者能像编写终端脚本一样(基于input和print进行交互)来编写应用，无需具备HTML和JS的相关知识；
PyWebIO还可以方便地整合进现有的Web服务。非常适合快速构建对UI要求不高的应用。

## 特性

- 使用同步而不是基于回调的方式获取输入，代码编写逻辑更自然
- 非声明式布局，布局方式简单高效
- 代码侵入性小，旧脚本代码仅需修改输入输出逻辑便可改造为Web服务
- 支持整合到现有的Web服务，目前支持与Flask、Django、Tornado、aiohttp、 FastAPI(Starlette)框架集成
- 同时支持基于线程的执行模型和基于协程的执行模型
- 支持结合第三方库实现数据可视化

## 安装

官方版本：

```shell
pip install pywebio
```

国内版本：

```shell
pip install pywebio3
```

## 入门案例

```python
from pywebio3.input import input, FLOAT
from pywebio3.output import put_text


def bmi():
    height = input("请输入你的身高(cm)：", type=FLOAT)
    weight = input("请输入你的体重(kg)：", type=FLOAT)

    BMI = weight / (height / 100) ** 2

    top_status = [
        (14.9, '极瘦'),
        (18.4, '偏瘦'),
        (22.9, '正常'),
        (27.5, '过重'),
        (40.0, '肥胖'),
        (float('inf'), '非常肥胖'),
    ]

    for top, status in top_status:
        if BMI <= top:
            put_text('你的 BMI 值: %.1f，身体状态：%s' % (BMI, status))
            break


if __name__ == '__main__':
    bmi()
```

## 输入

输入函数都定义在 pywebio.input 模块中，可以使用 from pywebio.input import * 引入。

调用输入函数会在浏览器上弹出一个输入表单来获取输入。PyWebIO的输入函数是阻塞式的（和Python内置的 input
一样），在表单被成功提交之前，输入函数不会返回。

### 基本输入

首先是一些基本类型的输入。

文本输入:

```shell
age = input("请输入年龄：", type=NUMBER)
```

这样一行代码的效果为：浏览器会弹出一个文本输入框来获取输入，在用户完成输入将表单提交后，函数返回用户输入的值。

下面是一些其他类型的输入函数:

```python
from pywebio3.input import input, FLOAT, NUMBER, PASSWORD, select, checkbox, radio, textarea, file_upload
from pywebio3.output import put_text

age = input("请输入年龄：", type=NUMBER)
password = input("请输入密码：", type=PASSWORD)
gift = select('请选择性别', ['男', '女'])
agree = checkbox("请勾选用户协议", options=['我同意用户协议'])
answer = radio("请选择答案", options=['A', 'B', 'C', 'D'])
text = textarea('请留言', rows=3, placeholder='请输入...')
img = file_upload("上传图片:", accept="image/*")
```

### 输入选项

输入函数可指定的参数非常丰富

```python
from pywebio3.input import input, FLOAT, NUMBER, PASSWORD, select, checkbox, radio, textarea, file_upload, TEXT
from pywebio3.output import put_text

input(
    '请输入姓名',
    type=TEXT,
    placeholder='你的名字',
    help_text='请填写你的真实名字',
    required=True,
)
```

### 参数校验

我们可以为输入指定校验函数，校验函数应在校验通过时返回None，否则返回错误消息:

```python
from pywebio3.input import input, FLOAT, NUMBER, PASSWORD, select, checkbox, radio, textarea, file_upload, TEXT
from pywebio3.output import put_text


def check_age(p):
    if p < 10:
        return '太年轻了'
    if p > 60:
        return '岁数太大了'


age = input("请输入年龄", type=NUMBER, validate=check_age)
```

### 代码编辑器

```python
from pywebio3.input import input, FLOAT, NUMBER, PASSWORD, select, checkbox, radio, textarea, file_upload, TEXT
from pywebio3.output import put_text

code = textarea('代码编辑', code={
    'mode': "python",
    'theme': 'darcula',
}, value='import numpy as np\n# 请编写你的代码')
```

### 输入组

PyWebIO支持输入组, 返回结果为一个字典。pywebio.input.input_group() 接受单项输入组成的列表作为参数, 返回以单项输入中的
name 作为键、以输入数据为值的字典:

```python
from pywebio3.input import *
from pywebio3.output import *


def check_age(p):
    if p < 10:
        return '太年轻了'
    if p > 60:
        return '岁数太大了'


data = input_group(
    "基本信息",
    [
        input('姓名', name='name'),
        input('年龄', name='age', type=NUMBER, validate=check_age)
    ],
)
put_text(data['name'], data['age'])
```

输入组中同样支持使用 validate 参数设置校验函数，其接受整个表单数据作为参数:

```python
from pywebio3.input import *
from pywebio3.output import *


def check_age(p):
    if p < 10:
        return '太年轻了'
    if p > 60:
        return '岁数太大了'


def check_form(data):
    if len(data['name']) > 6:
        return ('name', '姓名太长了！')
    if data['age'] <= 0:
        return ('age', '年龄不能为负数')


data = input_group(
    "基本信息",
    [
        input('姓名', name='name'),
        input('年龄', name='age', type=NUMBER, validate=check_age)
    ],
    validate=check_form,
)
put_text(data['name'], data['age'])
```

## 输出

输出函数都定义在 pywebio.output 模块中，可以使用 from pywebio.output import * 引入。

调用输出函数后，内容会实时输出到浏览器，在应用的生命周期内，可以在任意时刻调用输出函数。

### 基本输出

PyWebIO提供了一系列函数来输出文本、表格、图像等格式:

```python
from pywebio3.input import *
from pywebio3.output import *

put_text("纯文本")

# 表格
put_table([
    ['商品', '价格'],
    ['苹果', '5.5'],
    ['香蕉', '7'],
])

# 输出图片
put_image(open('1.jpg', 'rb').read())
put_image('https://pic.netbian.com/uploads/allimg/241213/002311-17340205911f92.jpg')  # internet image

# 输出markdown
put_markdown("""
# 一级标题
## 二级标题
### 三级标题
""")

# 输出文件
put_file('test.txt', b'hello word!')

# 输出提示
popup('提示标题', '提示内容')

# 输出消息
toast('新消息 🔔')
```

### 组合输出

函数名以 put_ 开始的输出函数，可以与一些输出函数组合使用，作为最终输出的一部分：

put_table() 支持以 put_xxx() 调用作为单元格内容:

```python
from pywebio3.input import *
from pywebio3.output import *

put_table([
    ['类型', '内容'],
    ['html', put_html('X<sup>2</sup>')],
    ['text', '<hr/>'],  # equal to ['text', put_text('<hr/>')]
    ['buttons', put_buttons(['A', 'B'], onclick=...)],
    ['markdown', put_markdown('`Awesome PyWebIO!`')],
    ['file', put_file('hello.text', b'hello world')],
    ['table', put_table([['A', 'B'], ['C', 'D']])]
])
```

类似地， popup() 也可以将 put_xxx() 调用作为弹窗内容:

```python
from pywebio3.input import *
from pywebio3.output import *

popup('Popup title', [
    put_html('<h3>Popup Content</h3>'),
    'plain html: <br/>',  # Equivalent to: put_text('plain html: <br/>')
    put_table([['A', 'B'], ['C', 'D']]),
    put_button('close_popup()', onclick=close_popup)
])
```

另外，你可以使用 put_widget() 来创建可以接受 put_xxx() 的自定义输出控件。

### 上下文管理器

一些接受 put_xxx() 调用作为参数的输出函数支持作为上下文管理器来使用：

```python
from pywebio3.input import *
from pywebio3.output import *

with put_collapse('This is title'):
    for i in range(4):
        put_text(i)

    put_table([
        ['Commodity', 'Price'],
        ['Apple', '5.5'],
        ['Banana', '7'],
    ])
```

### 事件回调

从上面可以看出，PyWebIO把交互分成了输入和输出两部分：输入函数为阻塞式调用，会在用户浏览器上显示一个表单，在用户提交表单之前输入函数将不会返回；输出函数将内容实时输出至浏览器。这种交互方式和控制台程序是一致的，因此PyWebIO应用非常适合使用控制台程序的编写逻辑来进行开发。

此外，PyWebIO还支持事件回调：PyWebIO允许你输出一些控件并绑定回调函数，当控件被点击时相应的回调函数便会被执行。

下面是一个例子:

```python
from pywebio3.input import *
from pywebio3.output import *
from functools import partial


def edit_row(choice, row):
    put_text("你点击了第 %s 行 %s 按钮" % (row, choice))


put_table([
    ['Idx', 'Actions'],
    [1, put_buttons(['编辑', '删除'], onclick=partial(edit_row, row=1))],
    [2, put_buttons(['编辑', '删除'], onclick=partial(edit_row, row=2))],
    [3, put_buttons(['编辑', '删除'], onclick=partial(edit_row, row=3))],
])
```

put_table() 的调用不会阻塞。当用户点击了某行中的按钮时，PyWebIO会自动调用相应的回调函数。

当然，PyWebIO还支持单独的按钮控件:

```python
from pywebio3.input import *
from pywebio3.output import *


def btn_click(btn_val):
    put_text("你点击了 %s 按钮" % btn_val)


put_buttons(['A', 'B', 'C'], onclick=btn_click)
put_button("点击我", onclick=lambda: toast("被点击了！"))
```

事实上，不仅是按钮，所有的输出都可以绑定点击事件。你可以在输出函数之后调用 onclick() 方法来绑定点击事件:

```python
from pywebio3.input import *
from pywebio3.output import *

put_image('1.jpg').onclick(lambda: toast('你点击了图片！'))

put_table([
    ['商品', '价格'],
    ['苹果', put_text('5.5').onclick(lambda: toast('你点击了文本'))],
])
```

`onclick()` 方法的返回值为对象本身，所以可以继续用于组合输出中。

### 输出域Scope

PyWebIO使用scope模型来控制内容输出的位置。scope为输出内容的容器，你可以创建一个scope并将内容输出到其中。

每个输出函数（函数名形如 put_xxx() ）都会将内容输出到一个Scope，默认为”当前Scope”，”当前Scope”由 use_scope() 设置。

可以使用 use_scope() 开启并进入一个新的输出域，或进入一个已经存在的输出域:

```python
from pywebio3.input import *
from pywebio3.output import *

with use_scope('scope1'):  # 创建并进入scope 'scope1'
    put_text('scope1中的文本')  # 输出内容到 scope1

put_text('新的文本会被追加到scope1')  # 输出内容到 ROOT scope
with use_scope('scope1'):  # 进入之前创建的scope 'scope1'
    put_text('继续追加文本到scope1')  # 输出内容到 scope1
```

use_scope() 还可以使用 clear 参数将scope中原有的内容清空:

```python
from pywebio3.input import *
from pywebio3.output import *

with use_scope('scope1'):  # 创建并进入scope 'scope1'
    put_text('scope1中的文本')  # 输出内容到 scope1

put_text('新的文本会被追加到scope1')  # 输出内容到 ROOT scope

# 清空原本的内容
with use_scope('scope1', clear=True):  # 进入之前创建的scope 'scope1'
    put_text('继续追加文本到scope1')  # 输出内容到 scope1
```

use_scope() 还可以作为装饰器来使用:

```python
from pywebio3.input import *
from pywebio3.output import *

from datetime import datetime


@use_scope('time', clear=True)
def show_time():
    put_text(datetime.now())


put_text("测试。。。")
for i in range(100):
    show_time()
    import time

    time.sleep(1)
```

第一次调用 show_time 时，将会创建 time 输出域并在其中输出当前时间，之后每次调用 show_time() ，输出域都会被新的内容覆盖。

Scope支持嵌套。会话开始时，PyWebIO应用只有一个 ROOT scope。你可以在一个scope中创建新的scope。比如，以下代码将会创建3个scope:

```python
from pywebio3.input import *
from pywebio3.output import *

with use_scope('A'):
    put_text('Text in scope A')

    with use_scope('B'):
        put_text('Text in scope B')

with use_scope('C'):
    put_text('Text in scope C')
```

我们已经知道scope实际上是输出内容的容器，那么我们能否将scope作为输出的子元素呢（比如将scope作为表格的一个cell），答案是肯定的。你可以使用
put_scope() 来显式创建一个scope，而从它以 put_ 开头的函数名可以看出，它也可以被传递到任何可以接受 put_xxx() 调用的地方。

```python
from pywebio3.input import *
from pywebio3.output import *

put_table([
    ['姓名', '爱好'],
    ['张三', put_scope('hobby', content=put_text('写代码'))]
])

# 重置
with use_scope('hobby', clear=True):
    put_text('电影')

# 追加
with use_scope('hobby'):
    put_text('音乐')
    put_text('电影')

# 插入markdown
put_markdown('**写代码**', scope='hobby', position=0)
```

除了 use_scope() 和 put_scope() , PyWebIO还提供了以下scope控制函数：

- clear(scope) : 清除scope的内容

- remove(scope) : 移除scope

- scroll_to(scope) : 将页面滚动到scope处

另外，所有的输出函数还支持使用 scope 参数来指定输出的目的scope，也可使用 position 参数来指定在目标scope中输出的位置

## 布局

通常，使用上述输出函数足以完成大部分输出，但是这些输出之间全都是竖直排列的。如果想创建更复杂的布局，需要使用布局函数。

pywebio.output 模块提供了3个布局函数，通过对他们进行组合可以完成各种复杂的布局:

- put_row() : 使用行布局输出内容. 内容在水平方向上排列

- put_column() : 使用列布局输出内容. 内容在竖直方向上排列

- put_grid() : 使用网格布局输出内容

通过组合 put_row() 和 put_column() 可以实现灵活布局:

```python
from pywebio3.input import *
from pywebio3.output import *

# 一行
put_row([
    # 一列
    put_column([
        put_code('A'),
        # 内部的一行
        put_row([
            put_code('B1'), None,  # None表示输出之间的空格
            put_code('B2'), None,
            put_code('B3'),
        ]),
        put_code('C'),
    ]), None,
    # 内容
    put_code('D'),
    None,
    put_code('E')
])
```

布局函数还支持自定义各部分的尺寸:

```python
put_row([put_image(…), put_image(…)], size = '40% 60%')  # 左右两图宽度比2:3
```

## 样式

如果你熟悉 CSS样式 ，你还可以在输出函数后调用 style() 方法给输出设定自定义样式。

可以给单个的 put_xxx() 输出设定CSS样式，也可以配合组合输出使用:

```python
from pywebio3.input import *
from pywebio3.output import *

# 单个组件样式
put_text('hello').style('color: red; font-size: 20px')

# 整体样式
put_row([
    put_text('hello').style('color: red'),
    put_markdown('markdown')
]).style('margin-top: 20px')
```

style() 方法的返回值为对象本身，所以可以继续用于组合输出中。

## 运行方式

在PyWebIO中，有两种方式用来运行PyWebIO应用：作为脚本运行和使用 pywebio.start_server() 或 pywebio.platform.path_deploy()
来作为Web服务运行。

### Server模式

在Server模式下，PyWebIO会启动一个Web服务来持续性地提供服务。当用户访问服务地址时，PyWebIO会开启一个新会话并运行PyWebIO应用。

将PyWebIO应用部署为web服务的最常用方式是使用 start_server()：

```python
from pywebio3 import *


# 应用程序函数
def main():
    name = input.input("名字")
    output.put_text("姓名：", name)


start_server(main, port=8080, debug=True)
```

现在，在 http://127.0.0.1:8080/ 页面就会看到欢迎页面了。

使用 debug=True 来开启debug模式，这时server会在检测到代码发生更改后进行重启。

start_server() 提供了对远程访问的支持，当开启远程访问后（通过在 start_server() 中传入 remote_access=True 开启
），你将会得到一个用于访问当前应用的临时的公网访问地址，其他任何人都可以使用此地址访问你的应用。远程接入可以很方便地将应用临时分享给其他人。

将PyWebIO应用部署为web服务的另一种方式是使用 path_deploy() 。path_deploy()
可以从一个目录中部署PyWebIO应用，只需要在该目录下的python文件中定义PyWebIO应用，就可以通过URL中的路径来访问这些应用了。

注意，在Server模式下， pywebio.input 、 pywebio.output 和 pywebio.session 模块内的函数仅能在任务函数上下文中进行调用。

### Script模式

如果你在代码中没有调用 start_server() 或 path_deploy() 函数，那么你就是以脚本模式在运行PyWebIO应用。

在脚本模式中，当首次运行到对PyWebIO交互函数的调用时，会自动打开浏览器的一个页面，后续的PyWebIO交互都会在这个页面上进行。当脚本运行结束，这个页面也将不再有效。

如果用户在脚本结束运行之前关闭了浏览器，那么之后会话内对于PyWebIO交互函数的调用将会引发一个 SessionException 异常。

### 并发

PyWebIO 支持在多线程环境中使用。

在 Script模式下，你可以自由地启动线程，并在其中调用PyWebIO的交互函数。当所有非 Daemon线程 运行结束后，脚本退出。

Server模式下，如果需要在新创建的线程中使用PyWebIO的交互函数，需要手动调用 register_thread(thread)
对新进程进行注册（这样PyWebIO才能知道新创建的线程属于哪个会话）。如果新创建的线程中没有使用到PyWebIO的交互函数，则无需注册。没有使用
register_thread(thread) 注册的线程不受会话管理，其调用PyWebIO的交互函数将会产生 SessionNotFoundException 异常。

Server模式下多线程的使用示例:

```python
import datetime
import threading
import time

from pywebio3 import *


def show_time():
    while True:
        with output.use_scope(name='time', clear=True):
            output.put_text(datetime.datetime.now())
            time.sleep(1)


def app():
    # 正确的多进程方式
    t = threading.Thread(target=show_time)
    session.register_thread(t)
    output.put_markdown('## 时钟')
    t.start()  # run `show_time()` in background

    # ❌ 错误的方式，会抛出异常 `SessionNotFoundException`
    # threading.Thread(target=show_time).start()

    output.put_text('启动后台任务！！！')


start_server(app, port=8080, debug=True)
```

### 会话的结束

当用户关闭浏览器页面时，与之相应的会话也将被关闭。会话关闭后，应用中未返回的PyWebIO输入函数的调用将会抛出
SessionClosedException 异常，后续对PyWebIO交互函数的调用将会引发 SessionNotFoundException 或 SessionClosedException 异常。

大部分情况下，你不需要捕获这些异常，让这些异常来终止代码的执行通常是比较合适的。

可以使用 pywebio.session.defer_call(func)
来设置会话结束时需要调用的函数。无论是因为用户主动关闭页面还是任务结束使得会话关闭，设置的函数都会被执行。defer_call(func)
可以用于资源清理等工作。在会话中可以多次调用 defer_call() ,会话结束后将会顺序执行设置的函数。