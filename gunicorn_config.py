# 指定错误日志的路径，这会记录运行时的错误信息
errorlog = '/root/mo/edu_system/error.log'
# 日志级别，可选的值有 debug, info, warning, error, critical
loglevel = 'info'

# 指定访问日志的路径，这记录所有的访问请求
accesslog = '/root/mo/edu_system/access.log'
# 自定义访问日志格式，这是可选的
access_log_format = '%({X-Real-IP}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'