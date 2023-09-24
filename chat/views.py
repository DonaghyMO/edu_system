import redis,json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from backend.redis_relevent import get_redis_client


def index(request):
    return render(request, 'chat/index.html', {})


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })


def get_chat_log(request, room_id):
    """
    根据房间id获取聊天记录
    """
    # 创建 Redis 连接
    redis_client = get_redis_client()
    room_id = f"chat_{room_id}"
    try:
        chat_logs = [json.loads(item) for item in redis_client.lrange(room_id, 0, -1)]
    except Exception as e:
        chat_logs = []

    return JsonResponse({"content": chat_logs}, status=200)
