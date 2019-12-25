#每个worker的线程数
threads = 2
# 端口
bind = '0.0.0.0:8080'
#设置守护进程, 讲进程交给supervisor管理
daemon = 'true'
#最大并发量
worker_connections = 2000

#设置访问日志和错误信息日志路径
accesslog = 'logs/log'
errorlog = 'logs/error.log'

#设置日志记录水平
loglevel = 'warning'
worker_class='gevent'
workers = 2

