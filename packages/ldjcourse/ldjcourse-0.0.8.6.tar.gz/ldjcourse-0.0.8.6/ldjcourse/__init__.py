from .settings import settings_server as _settings_server

_settings_server.init()


def info():
    txt1 = '本安装包由元蓝先生为教学专门构建，提供教学所需的工具和资源。'
    txt2 = '元蓝先生活跃于B站，分享编程、数据分析和人工智能相关教学内容。'
    txt3 = '链接：https://space.bilibili.com/3546564903569609'
    txts = '\n'.join([txt1, txt2, txt3])
    print(txts)


def help():
    txt1 = '安装包的命令：pip install ldjcourse -i https://pypi.org/simple'
    txt2 = '更新包的命令：pip install --upgrade ldjcourse -i https://pypi.org/simple'
    txts = '\n'.join([txt1, txt2])
    print(txts)
