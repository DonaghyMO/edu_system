import json
from anytree import Node,RenderTree,find
from anytree.exporter import JsonExporter
from anytree.importer import JsonImporter
from my_decorater import check_login
from category.models import Category
from django.shortcuts import render,redirect
from category.forms import CategoryCreateForm
from backend.redis_relevent import get_redis_client
from django.http import JsonResponse
# Create your views here.

@check_login
def list_categories(request):
    category_search = request.GET.get("category_search")
    root = get_category_tree()
    if root:
        exporter = JsonExporter(indent=2, sort_keys=True)
        root = exporter.export(root)
    return render(request, 'resource_manage/category/category_list.html', {'categories': root})


def get_category_tree():
    """
    获取类别树根节点
    """
    redis_client = get_redis_client()
    tree_key = "category_tree"
    importer = JsonImporter()
    try:
        root = importer.import_(redis_client.get(tree_key))
    except Exception as e:
        return {}
    return root


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
        root = Node("root", category_name="root")
        exporter = JsonExporter(indent=2, sort_keys=True)
        json_data = exporter.export(root)
        redis_client.set(tree_key, json_data, ex=60*60*24*365)
    root = get_category_tree()
    # 找到父节点
    node_to_find = find(root, lambda node: node.name == str(parent))

    Node(str(child), parent=node_to_find, category_name=child_name)
    exporter = JsonExporter(indent=2, sort_keys=True)
    # 更新类别树
    json_data = exporter.export(root)
    redis_client.set(tree_key, json_data, ex=60*60*24*365)
    # 更新父节点
    if parent == "root":
        return
    cats = Category.objects.filter(id=int(parent))
    if cats:
        child_category = cats[0].child_category
        cats[0].child_category = child_category+","+str(child) if child_category else str(child)
        cats[0].save()


@check_login
def create_category(request):
    if request.method == "POST":
        form = CategoryCreateForm(request.POST)
        if not form.is_valid():
            return redirect("list_category")
        name = form.cleaned_data["name"]
        description = form.cleaned_data["description"]
        parent_category = request.POST.get("parent_category")
        # 处理子类别
        if parent_category:
            cat = Category.objects.create(name=name, description=description)
            insert_category_tree(parent_category, cat.id, cat.name)
        # 处理根类别
        else:
            cat = Category.objects.create(name=name, description=description)
            insert_category_tree("root", cat.id, cat.name)

        return redirect("list_category")

    elif request.method == "GET":
        parent_category = request.GET.get("parent_category")
        cats = [(c.id, c.name) for c in Category.objects.all()]
        form = CategoryCreateForm()

    else:
        parent_category = ""
        cats = [(c.id, c.name) for c in Category.objects.all()]
        form = CategoryCreateForm()
    return render(request, 'resource_manage/category/category_create.html', {'form':form,'cats':cats,'parent_category':parent_category})