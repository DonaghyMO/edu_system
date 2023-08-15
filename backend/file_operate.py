"""
一些本地的文件操作
"""

import os
from edu_system.settings import MEDIA_ROOT


def delete_media_file(file_name,file_type):
    """
    本地操作，删除本地文件
    """
    abs_path = os.path.join(MEDIA_ROOT,file_type,file_name)
    os.remove(abs_path)