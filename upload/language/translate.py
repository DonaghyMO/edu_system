import json

from googletrans import Translator

def trans():
    translator = Translator()
    tmp={}
    src = "zh-cn"
    # 转换成英文
    dest = "ko"
    with open("chinese.json","r") as f:
        data = json.loads(f.read())
        print(data)
        for key,value in data.items():
            t={}
            for k,v in value.items():
                translated = translator.translate(v,dest,src)
                t.update({k:translated.text})
            tmp.update({key:t})
    with open("k.json","w") as f:
        f.write(json.dumps(tmp))
if __name__=="__main__":
    # trans()
    import json

    # 输入的JSON字符串
    json_data = '{"pre_login": {"teacher_login": "\\uad50\\uc0ac \\ub85c\\uadf8\\uc778", "student_login": "\\ud559\\uc0dd \\ub85c\\uadf8\\uc778"}, "login": {"welcome": "\\ud658\\uc601", "username": "\\uc0ac\\uc6a9\\uc790 \\uc774\\ub984", "login": "\\ube44\\ubc00\\ubc88\\ud638", "login_button": "\\ub85c\\uadf8\\uc778", "no_account": "\\uacc4\\uc815\\uc774 \\uc5c6\\uc2b5\\ub2c8\\ub2e4", "register": "\\ub4f1\\ub85d\\ud558\\ub2e4"}, "register": {"username": "\\uc0ac\\uc6a9\\uc790 \\uc774\\ub984", "password": "\\ube44\\ubc00\\ubc88\\ud638", "confirm": "\\ube44\\ubc00\\ubc88\\ud638 \\ud655\\uc778", "invite_code": "\\uad50\\uc0ac \\ucd08\\ub300\\uc7a5 \\ucf54\\ub4dc (\\ud559\\uc0dd \\uc0ac\\uc6a9\\uc790 \\ubb34\\uc2dc)", "register": "\\ub4f1\\ub85d\\ud558\\ub2e4", "exist_account": "\\uae30\\uc874 \\uacc4\\uc815", "login": "\\ub85c\\uadf8\\uc778"}, "index": {"audio": "\\uc624\\ub514\\uc624", "video": "\\ub3d9\\uc601\\uc0c1", "text": "\\ud14d\\uc2a4\\ud2b8", "interaction": "\\uc778\\ud130\\ub809\\ud2f0\\ube0c"}, "search": {"keyword": "\\ud0a4\\uc6cc\\ub4dc\\ub97c \\uc785\\ub825\\ud558\\uc2ed\\uc2dc\\uc624", "search": "\\ucc3e\\ub2e4", "audio": "\\uc624\\ub514\\uc624", "video": "\\ub3d9\\uc601\\uc0c1", "text": "\\ud14d\\uc2a4\\ud2t8"}, "me": {"username": "\\uc0ac\\uc6a9\\uc790 \\uc774\\ub984", "wechat_name": "Wechat \\ubcc4\\uba85", "user_type": "\\uc0ac\\uc6a9\\uc790 \\uce74\\ud14c\\uce0c\\ub9ac", "logout": "\\ub85c\\uadf8 \\uc544\\uc6c3\\ud558\\uc2ed\\uc2dc\\uc624"}, "chatroom": {"input_message": "\\uba54\\uc2dc\\uc9c0\\ub97c \\uc785\\ub825\\ud558\\uc2ed\\uc2dc\\uc624", "send": "\\ubcf4\\ub0b4\\ub2e4"}, "interaction": {"teacher": "\\uc120\\uc0dd\\ub2d8", "student": "\\ud559\\uc0dd"}, "notification": {"notification": "\\uc54c\\ub9bc"}, "resource": {"audio": "\\uc624\\ub514\\uc624", "video": "\\ub3d9\\uc601\\uc0c1", "text": "\\ud14d\\uc2a4\\ud2b8"}}'

    # 将JSON字符串解析为Python字典
    data = json.loads(json_data)

    # 将Python字典转换回JSON字符串（可选）
    json_string = json.dumps(data, ensure_ascii=False)  # ensure_ascii=False确保不使用ASCII编码

    # 打印解码后的字典
    print(json.dumps(data, ensure_ascii=False, indent=4))  # 用indent参数进行格式化输出
