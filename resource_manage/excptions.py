class NotSupportFileType(Exception):
    """
    类别存在异常
    """

    def __init__(self, file_type):
        super().__init__("不支持文件类型：{}".format(file_type))