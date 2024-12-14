import os
import shutil
import sys
import importlib

LOCAL_SETTINGS_MODULE = 'ldj_settings'


def copy_local_settings():
    file1 = os.path.join(os.getcwd(), f'{LOCAL_SETTINGS_MODULE}.py')
    if not os.path.exists(file1):
        file2 = os.path.join(os.path.split(__file__)[0], 'settings_client.py')
        shutil.copy(file2, file1)


def load_local_settings(local_settings_module=LOCAL_SETTINGS_MODULE):
    try:
        current_module_name = __name__.rsplit('.', 1)[0]
        parent_module = sys.modules.get(current_module_name)

        local_settings = importlib.import_module(local_settings_module)
        attrs = ['KEY_ID', 'KEY_SECRET', 'BASE_URL']
        for attr in attrs:
            setattr(parent_module, attr, getattr(local_settings, attr))
    except ModuleNotFoundError:
        txt = f'''\033[31mLocal settings module '{local_settings_module}' not found!\n请联系老师解决该问题！\033[0m'''
        print(txt)
        exit(1)


def init():
    copy_local_settings()
    load_local_settings()
