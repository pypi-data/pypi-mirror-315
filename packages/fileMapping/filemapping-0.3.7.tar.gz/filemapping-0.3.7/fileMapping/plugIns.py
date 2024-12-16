import os
import sys

from . import empty
from . import pluginLoading
from . import config as fileMappingConfig


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


def configConvertTodict(config) -> dict:
    """
    将配置文件转换为dict格式
    :param config: 配置文件
    :return: dict 格式的配置文件
    """
    systemConfiguration = {}
    for obj in dir(config) if not isinstance(config, (dict, list, tuple)) else config:
        if obj.startswith("__"):
            continue

        if isinstance(getattr(config, obj), (dict, list, tuple)) if not isinstance(config, (dict, list, tuple)) else isinstance(config[obj], (dict, list, tuple)):
            systemConfiguration[obj] = configConvertTodict(getattr(config, obj))

        else:
            if not obj in dir(empty.empty):
                systemConfiguration[obj] = getattr(config, obj) if not isinstance(config, (dict, list, tuple)) else config[obj]

    return systemConfiguration
    # sysCpL = config
    # systemConfiguration = {} | {
    #     obj: {
    #         i: getattr(getattr(sysCpL, obj), i) for i in dir(getattr(sysCpL, obj))
    #         if obj in dir(empty.empty)
    #     } for obj in dir(sysCpL) if not obj.startswith("__")
    # }


class fileMapping_dict(dict):
    # 用于包装字典
    # 可以通过 . 访问属性
    def __getattr__(self, item):
        if item in self:
            return self.get(item)

        else:
            raise AttributeError(f"{self.__class__.__name__} has no attribute '{item}'")



class File:
    """
    callObject
        - 调用对象
    invoke
        - 内行参数
    returnValue
        - 返回参数
    public
        - 公共
    """
    callObject = fileMapping_dict({})
    invoke = fileMapping_dict({})
    returnValue = fileMapping_dict({})
    public = fileMapping_dict({})

    def __init__(self,
                 absolutePath: os.path,
                 screening=None,
                 config: dict = None,
                 printLog: bool =False,
                 printPosition=sys.stdout
        ):
        """
        映射文件夹下的Python文件或者包
        :param absolutePath: 当前的根目录绝对路径
        :param screening: 要映射的文件
        :param config: 配置文件 它将会被映射到 public['config']
        :param printLog: 是否打印日志
        :param printPosition: 日志输出位置 默认为 sys.stdout 在终端输出
        """
        if screening is None:
            screening = ["py"]

        if not ((not os.path.isabs(absolutePath)) or (not os.path.islink(absolutePath))):
            raise FileNotFoundError(f"不是一个有效的绝对路径。: '{absolutePath}'")

        # self
        self.printLog = printLog
        self.printPosition = printPosition
        self.listOfFiles = {
            i.split('.')[0]: os.path.join(absolutePath, i) for i in os.listdir(absolutePath)
            if (i.split('.')[-1] in screening) or (os.path.isdir(os.path.join(absolutePath, i))) # and os.path.isfile(os.path.join(absolutePath, i))
        }

        # 加载配置文件
        if config:
            fileMappingConfig.log['printPosition'] = self.printPosition
            fileMappingConfig.log['printLog'] = self.printLog
            self.public['config'] = config

        # 加载插件
        for key, data in self.listOfFiles.items():
            self.callObject[key] = pluginLoading.f(data)


    def __run__(self, name, args, kwargs):
        """
        运行映射文件
        :return:
        """
        self.returnValue[name] = self.callObject[name].run(*args, **kwargs)
        self.invoke[name] = self.callObject[name].pack

        pluginLoading.printlog(f"运行文件成功: {name} 文件", printPosition=self.printPosition, color="32", printLog=self.printLog)

    def run(self, *args, name: str = None, **kwargs):
        """
        运行映射文件
        :return:
        """
        if name is None:
            for key, data in self.listOfFiles.items():
                if self.callObject[key]:
                    self.__run__(key, args, kwargs)
                    # self.returnValue[key] = self.callObject[key].run(*args, **kwargs)
                    # self.invoke[key] = self.callObject[key].pack

        else:
            if self.callObject.get(name, False):
                self.__run__(name, args, kwargs)
                # self.returnValue[name] = self.callObject[name].run(*args, **kwargs)
                # self.invoke[name] = self.callObject[name].pack

            else:
                pluginLoading.printlog(f"运行文件错误: 没有 {name} 文件", printPosition=self.printPosition, color="31", printLog=self.printLog)
                # print(f"\n\033[1;31m 运行文件错误: 没有 {name} 文件 \033[0m")
