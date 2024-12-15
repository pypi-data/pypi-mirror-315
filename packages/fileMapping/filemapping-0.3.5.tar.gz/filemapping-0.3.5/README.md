[TOC]

------

# fileMapping
## 当前版本 0.3.4
用于快速调用文件夹下的py文件或者包


## 安装
使用以下命令通过pip安装fileMapping库：
```shell
    pip install fileMapping
```


## 环境要求
fileMapping库的开发环境是：
    Python 3.9
    Windows 10

## 使用示例
文件结构树
```
-
├─ main.py
└─ plugins
   ├─ a.py
   └─ b.py

```

例: 
    当我们需要加载一个wed(flask)时
```python
# a.py
from flask import Flask



ip = '127.0.0.1'

class wed:
    def __init__(self, app: Flask):
        self.app = app
        self.ip = ip
        
    def wed(self):
        @self.app.route("/wed")
        def wed():
            return 'True'
        
def main(app: Flask):
    return wed(app)

        
```

```python
# b.py
from fileMapping import File
from flask import Flask


def main(app: Flask):
    @app.route("/")
    def root():
        # 从b中调用a的ip
        return File.invoke['a'].ip


```

```python
# main.py
from fileMapping import File, pathConversion
from flask import Flask

path = __file__
mapPaths = 'plugins'

app = Flask(path)
f = File(pathConversion(path, mapPaths))

if __name__ == '__main__':
    app.run(host="127.0.0.1")


```
可以方便的高效的装饰

## 函数介绍

fileMapping.File
```python
class File:
    def __init__(self, absolutePath: os.path, screening=None):
        """
        映射文件夹下的Python文件或者包
        :param absolutePath: 当前的根目录绝对路径
        :param screening: 要映射的文件夹
        """

    def run(self, *args, **kwargs):
        """
        运行映射文件
        :return:
        """

```


fileMapping.pathConversion
```python
def pathConversion(cpath: os.path, path: os.path) -> os.path:
    """
    当要转化的文件目录在调用文件的临旁时,则可以用这个快速转化

    例：
    |--->
        |-> plugIns
        |-> x.py

    其中x.py要调用plugIns文件夹时即可快速调用

    pathConversion(__file__, "plugIns")
    :param cpath: __file__
    :param path: 必须为文件夹
    :return:
    """
    return os.path.join(os.path.dirname(cpath)if os.path.isfile(cpath)else cpath, os.path.abspath(path))

```

------

## [更新日志](https://github.com/bop-lp/fileMapping/blob/main/changelog.md)

