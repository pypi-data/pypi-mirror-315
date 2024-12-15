from setuptools import setup, find_packages



# read the contents of your README file
from pathlib import Path

README = "README.md"
this_directory = Path(__file__).parent
long_description = (this_directory / README).read_text(encoding='utf-8')

print("""
开始安装fileMapping
""")

setup(
    name='fileMapping',
    version='0.3.4',
    author='朝歌夜弦',
    author_email='bop-lp@qq.com',
    description='用于快速调用文件夹下的py文件或者包',
    long_description = long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/bop-lp/fileMapping",
    packages=find_packages(),
    install_requires=[]
)

print("""
安装成功!
谢谢使用, 如果有任何问题请联系作者: bop-lp@qq.com
""")



