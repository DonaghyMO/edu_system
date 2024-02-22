import redis
from anytree import Node, find
from anytree.exporter import JsonExporter
from anytree.importer import JsonImporter
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, redirect

from backend.redis_relevent import get_redis_client
from category.forms import CategoryCreateForm
from category.models import Category
from my_decorater import check_login
from tools.utils import list_videos_with_category_id, list_text_with_category_id, list_audios_with_category_id
from .exception import CategoryExist, RootCategoryDeleteFailed, CategoryWithResource


# Create your views here.

@check_login
def list_categories(request):
    category_search = request.GET.get("category_search")
    root = get_category_tree()
    if root:
        exporter = JsonExporter(indent=2, sort_keys=True)
        root = exporter.export(root)
    return render(request, 'resource_manage/category/category_list.html', {'categories': root})


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


def insert_category_tree(parent, child, child_name):
    """
    更新类别树和数据库中父类别的数据
    parent 父类别id
    child 子类别id
    """
    redis_client = get_redis_client()
    tree_key = "category_tree"
    if not redis_client.exists(tree_key):
        # 创建树
        create_tree()
    root = get_category_tree()
    # 找到父节点
    node_to_find = find(root, lambda node: node.name == parent)
    if not node_to_find:
        node_to_find = find(root, lambda node: node.name == str(parent))
    Node(child, parent=node_to_find, category_name=child_name)
    exporter = JsonExporter(indent=2, sort_keys=True)
    # 更新类别树
    json_data = exporter.export(root)
    # print(json_data)
    redis_client.set(tree_key, json_data, ex=60 * 60 * 24 * 365)
    cats = Category.objects.filter(id=parent)
    if cats:
        child_category = cats[0].child_category
        cats[0].child_category = child_category + "," + str(child) if child_category else str(child)
        cats[0].save()


def is_category_exist(parent_id, name):
    """
    根据类别名判断父类别中是否有当前要创建的类别
    """
    try:
        pcat = Category.objects.get(id=parent_id)
        if not pcat.child_category:
            return False
        child_ids = [int(item) for item in pcat.child_category.split(",")]
        for child in Category.objects.filter(id__in=child_ids):
            if child.name == name:
                return True
    except ObjectDoesNotExist as e:
        raise ObjectDoesNotExist("没有找到父节点")
    return False


@check_login
def create_category(request):
    if request.method == "POST":
        form = CategoryCreateForm(request.POST)
        if not form.is_valid():
            return redirect("list_category")
        name = form.cleaned_data["name"]
        description = form.cleaned_data["description"]
        parent_category = int(request.POST.get("parent_category"))
        if is_category_exist(parent_category, name):
            raise CategoryExist(name)

        # 处理
        cat = Category.objects.create(name=name, description=description)
        insert_category_tree(parent_category, cat.id, cat.name)
        return redirect("list_category")

    elif request.method == "GET":
        parent_category = int(request.GET.get("parent_category"))
        parent_name = request.GET.get("parent_name")
        cats = [(c.id, c.name) for c in Category.objects.all()]
        form = CategoryCreateForm()

    else:
        parent_category = -1
        parent_name = request.GET.get("parent_name")
        cats = [(c.id, c.name) for c in Category.objects.all()]
        form = CategoryCreateForm()
    return render(request, 'resource_manage/category/category_create.html',
                  {'form': form, 'cats': cats, 'parent_category': parent_category, "parent_name": parent_name})


def has_resource(category_id):
    """
    判断是否有资源
    """
    # 视频类别
    if list_videos_with_category_id(category_id) or list_audios_with_category_id(
            category_id) or list_text_with_category_id(category_id):
        raise CategoryWithResource()
    return False


def has_children_resource(category_id):
    """
    递归判断子类别是否存在资源
    """
    try:
        cat = Category.objects.get(id=category_id)
        if cat.child_category:
            # 如果有子类别就递归判断
            childs = [int(child) for child in cat.child_category.split(",")]
            # 先判断子类别是否有资源
            for child in childs:
                if has_children_resource(child):
                    return True
            # 判断当前类别有没有资源
            if has_resource(category_id):
                return True
            return False
        else:
            # 没有子类别就判断当前类别有没有资源
            if has_resource(category_id):
                return True
            return False
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist("类别不存在")


def delete_children_category(category_id):
    """
    删除所有含有children_category中的category_id
    """
    cats = Category.objects.all()
    for cat in cats:
        if str(category_id) in cat.child_category:
            cat_list = cat.child_category.split(",")
            cat_list.remove(str(category_id))
            child_str = ",".join(cat_list)
            cat.child_category = child_str
            cat.save()


def delete_category_cas(object_id):
    """
    级连删除类别，只删类别，类别底下有资源就不删
    """

    def _delete_category_mysql(object_id):
        """
        级连删除
        """
        cat = Category.objects.get(id=object_id)
        cat_name = cat.name
        if cat.child_category:
            cat_child_ids = [int(item) for item in cat.child_category.split(",")]
            for child_id in cat_child_ids:
                _delete_category_mysql(child_id)
        cat.delete()
        return cat_name

    def _delete_category_redis(object_id):
        """
        级联删除redis中的数据
        """
        redis_client = get_redis_client()
        tree_key = "category_tree"
        root = get_category_node(-1)
        node_to_find = find(root, lambda node: node.name == object_id)
        if node_to_find:
            node_to_find.parent = None
        exporter = JsonExporter(indent=2, sort_keys=True)
        # 更新类别树
        json_data = exporter.export(root)
        redis_client.set(tree_key, json_data, ex=60 * 60 * 24 * 365)

    if object_id == -1:
        raise RootCategoryDeleteFailed()
    if has_children_resource(object_id):
        raise CategoryWithResource("")
    _delete_category_redis(object_id)
    cat_name = _delete_category_mysql(object_id)
    delete_children_category(object_id)
    return cat_name


@check_login
def delete_category(request, object_id):
    """
    级联删除类别，如果类别底下有子类别，且子类别下没有文件才删除
    """
    if (request.method == "DELETE"):
        object_id = int(object_id)
        cat_name = delete_category_cas(object_id)
        return JsonResponse({"success": "删除{}成功".format(cat_name)}, status=200)


def update_redis_tree(category_id, category_name):
    """
    修改redis中的节点名
    """
    redis_client = get_redis_client()
    tree_key = "category_tree"
    root = get_category_node(-1)
    node_to_find = find(root, lambda node: node.name == category_id)
    if node_to_find:
        node_to_find.category_name = category_name
    exporter = JsonExporter(indent=2, sort_keys=True)
    # 更新类别树
    json_data = exporter.export(root)
    redis_client.set(tree_key, json_data, ex=60 * 60 * 24 * 365)


def update_resource_category(category_id, category_name):
    """
    修改音频、视频、文本资源的类别名
    """
    texts = list_text_with_category_id(category_id)
    for text in texts:
        text.category = category_name
        text.save()

    audios = list_audios_with_category_id(category_id)
    for audio in audios:
        audio.category = category_name
        audio.save()

    videos = list_videos_with_category_id(category_id)
    for video in videos:
        video.category = category_name
        video.save()


@check_login
def update_category(request):
    """
    修改类别
    """
    if request.method == "GET":
        category_id = request.GET.get("parent_category")
        cat = Category.objects.get(id=int(category_id))
        form = CategoryCreateForm(instance=cat)
        return render(request, 'resource_manage/category/category_update.html', {"form": form,"category_id":category_id})
    if request.method == "POST":
        form = CategoryCreateForm(request.POST)
        if form.is_valid():
            cat_id = int(request.POST.get("category_id"))
            update_redis_tree(cat_id, form.cleaned_data["name"])
            cat = Category.objects.get(id=cat_id)
            cat.name = form.cleaned_data["name"]
            cat.description = form.cleaned_data["description"]
            cat.save()
            update_resource_category(cat.id, cat.name)
        return redirect("list_category")


def list_category(search_id=None):
    """
    查找类别
    """
    return Category.objects.filter(id=search_id) if search_id else Category.objects.all()
