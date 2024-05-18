import logging

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


if __name__ == '__main__':
    s = generate_token("ddddd", "ffasfsf")
    print(verify_token(s))
