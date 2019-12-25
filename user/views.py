from . import app_user
from flask import g, request, jsonify
from pymysql import *
from hashlib import md5
from auth import *
import random
import os

# md5加密盐值
salt = 'OSIBDUBUAOPMXC'.encode('utf-8')
# 配置数据库信息
conn_config = {"host": "localhost", "port": 3306, "user": "root",
               "password": "2356147", "database": "data", "charset": "utf8"}


def Dao():
    conn = connect(**conn_config)
    cs = conn.cursor()
    return (conn, cs)


@app_user.route('/login', methods=['post'])
def login():
    userID = request.form.get('userID')
    password = request.form.get('password')
    if not (userID and password):
        return 'error'
    conn, cs = Dao()
    count = cs.execute('select * from login where username=%s;', userID)
    temp = cs.fetchone()
    if not count:
        return '404'
    if password != temp[2]:
        return 'failed'
    return 'https://ks.wjx.top/jq/46412661.aspx?sojumpparm={0};{1}'.format(userID, temp[4])


@app_user.route('/user/register', methods=['post'])
def user_register():
    account = request.form.get('account')
    password = request.form.get('password')
    if not (account or password):
        return 'error'

    conn, cs = Dao()
    count = cs.execute('select * from users where account=%s;', account)
    if count:
        cs.close()
        conn.close()
        return 'exist'
    else:
        md5_password = md5(password.encode('utf-8'))
        md5_password.update(salt)
        md5_password = md5_password.hexdigest()
        result = cs.execute(
            'insert into users(account, password, register_time) values(%s, %s, now());', (account, md5_password))
        conn.commit()
        cs.close()
        conn.close()
        if result:
            return 'success'
        else:
            return 'failed'


@app_user.route('/user/login', methods=['post'])
def user_login():
    account = request.form.get('account')
    password = request.form.get('password')
    if not (account or password):
        return 'error'

    conn, cs = Dao()
    is_existing = cs.execute(
        'select id,account,password from users where account=%s;', account)
    # 如果该账号不存在
    if not is_existing:
        cs.close()
        conn.close()
        return 'not exist'
    else:
        temp = cs.fetchone()
        password = md5(password.encode('utf-8'))
        password.update(salt)
        md5_password = temp[2]
        # 判断密码是否正确
        if password.hexdigest() == md5_password:
            # 生成token
            token = serializer.dumps({'account': temp[1]})
            # 插入数据库
            cs.execute('update users set token=%s where account=%s;',
                       (token, account))
            conn.commit()
            cs.close()
            conn.close()
            # 返回token
            return token
        else:
            cs.close()
            conn.close()
            return 'failed'
