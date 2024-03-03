import redis
from anytree import Node
from anytree.exporter import JsonExporter
from anytree.importer import JsonImporter
from category.models import Category
from anytree import find
from backend.redis_relevent import get_redis_client


def create_tree():
    """
    创建类别树
    """
    try:
        # mysql
        ca = Category(id=-1, name="root", description="根节点")
        ca.save()
        # rides
        redis_client = get_redis_client()
        tree_key = "category_tree"
        root = Node(-1, category_name="root")
        exporter = JsonExporter(indent=2, sort_keys=True)
        json_data = exporter.export(root)
        redis_client.set(tree_key, json_data, ex=60 * 60 * 24 * 365)
    except redis.RedisError as e:
        return False
    return True


def get_category_tree():
    """
    获取类别树根节点,返回字典
    """
    redis_client = get_redis_client()
    tree_key = "category_tree"
    importer = JsonImporter()
    try:
        if not redis_client.exists(tree_key):
            create_tree()
        root = importer.import_(redis_client.get(tree_key))
    except redis.RedisError as e:
        # 先创建根节点
        create_tree()
        root = importer.import_(redis_client.get(tree_key))
    return root

def get_category_node(category_id):
    """
    根据类别id获取子树节点
    """
    root = get_category_tree()
    node_to_find = find(root, lambda node: node.name == category_id)
    # if not node_to_find:
    #     node_to_find = find(root,lambda node: node.name==str(category_id))
    # exporter = JsonExporter(indent=2,sort_keys=True)
    # json_data = exporter.export(node_to_find)
    return node_to_find


def get_category_tree_dic():
    """
    获取目录树对应的字典
    """
    root = get_category_tree()
    if root:
        exporter = JsonExporter(indent=2, sort_keys=True)
        root = exporter.export(root)
    return root



