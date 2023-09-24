import json
import datetime
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from backend.redis_relevent import get_redis_client


class ChatConsumer(WebsocketConsumer):
    # websocket建立连接时执行方法
    def connect(self):
        # 从url里获取聊天室名字，为每个房间建立一个频道组
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # 将当前频道加入频道组
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        # 接受所有websocket请求
        self.accept()

    # websocket断开时执行方法
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # 从websocket接收到消息时执行函数
    def receive(self, text_data):
        text_data_json = json.loads(text_data)['message']
        content = text_data_json['content']
        user_type = text_data_json['user_type']
        content_id = text_data_json['id']
        user_id = text_data_json["user_id"]
        # 发送消息到频道组，频道组调用chat_message方法
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': content
            }
        )
        # 存储聊天记录
        cli = get_redis_client()
        item_to_push = {"user_type": user_type, "content": content,"id":content_id,'user_id':user_id}
        cli.rpush(self.room_group_name, json.dumps(item_to_push))

    # 从频道组接收到消息后执行方法
    def chat_message(self, event):
        message = event['message']

        # 通过websocket发送消息到客户端
        self.send(text_data=json.dumps({
            'message': f'{message}'
        }))

    async def send_history_messages(self, messages):
        for message in messages:
            await self.send(text_data=json.dumps({
                'type': 'chat_message',
                'message': message,
            }))

    def get_history_messages(self):
        # 使用 Redis 客户端库来获取历史消息
        redis_client = get_redis_client()
        history_messages = redis_client.lrange(self.room_group_name, 0, -1)  # 获取所有历史消息
        history_messages = [json.loads(message)["message"] for message in history_messages]
        return history_messages
