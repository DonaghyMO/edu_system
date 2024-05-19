import logging
import string
import random

import jwt
from datetime import datetime, timedelta
from django.conf import settings

SECRET_KEY = settings.SECRET_KEY
# SECRET_KEY = "jsdijasida"


def check_invite_code(code):
    """
    校验教师邀请码
    """
    return code == "9Dj$#8pA!7Bv*3rK@6F"


"""
生成token
"""
logger = logging.getLogger(__name__)

def generate_token(openid, sessionkey, expiration=24*60):
    # 24小时后过期
    return jwt.encode(
        payload={"exp": datetime.now() + timedelta(minutes=expiration), "openid": openid, "session_key": sessionkey},
        key=SECRET_KEY, algorithm="HS256")


def verify_token(token):
    try:
        data = jwt.decode(token,key=SECRET_KEY,algorithms="HS256")
    except jwt.exceptions.ExpiredSignatureError:
        logger.error("token超时")
        raise jwt.exceptions.ExpiredSignatureError
    except Exception as e:
        logger.error("token解码失败"+e)
        raise e
    return data


def generate_random_nickname(length=8):
    # 定义字符集：小写字母、大写字母和数字
    characters = string.ascii_lowercase + string.digits
    # 从字符集中随机选择指定长度的字符
    random_nickname = ''.join(random.choice(characters) for _ in range(length))
    return random_nickname

if __name__ == '__main__':
    print(generate_random_nickname(8))
