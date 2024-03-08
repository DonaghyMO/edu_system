FROM amd64/python:3.8.2
MAINTAINER Donaghy<mdy504643635@gmail.com>
WORKDIR /edu_system
COPY requirements.txt requirements.txt
# 设定时区
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple  \
    && pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY ./docker/supervisord.conf /etc/supervisord.conf
EXPOSE 8000
COPY . .
CMD ["supervisord", "-c", "/etc/supervisord.conf"]