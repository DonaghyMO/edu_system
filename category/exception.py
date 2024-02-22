class CategoryExist(Exception):
    """
    类别存在异常
    """

    def __init__(self, child_name):
        super().__init__("子类别{}已经存在".format(child_name))


class CategoryWithResource(Exception):
    """
    类别活其子类别有资源
    """

    def __init__(self, name):
        super().__init__("类别{}下存在资源".format(name))


class CategoryDeleteFailed(Exception):
    """
    删除类别失败
    """

    def __init__(self):
        super().__init__("类别删除失败")


class RootCategoryDeleteFailed(Exception):
    """
    删除类别失败
    """

    def __init__(self):
        super().__init__("根类别无法删除")


class CategoryWithResource(Exception):
    """
    类别下有资源，不允许删除
    """
    def __init__(self):
        super().__init__("类别下有资源，无法删除")


class NotValidCategory(Exception):
    """
    无效类别
    """
    def __init__(self):
        super().__init__("无效类别，请选择类别")
