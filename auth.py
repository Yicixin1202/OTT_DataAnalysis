from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from pymysql import *
from flask import g

auth = HTTPTokenAuth(scheme='Bearer')

# 配置token加密的KEY
SECRET_KEY = 'ANOIZXBIUVBQPOMZNQ'
serializer = Serializer(SECRET_KEY, expires_in=1800)
# 配置数据库信息
conn_config = {"host": "localhost", "port": 3306, "user": "root",
               "password": "2356147", "database": "data", "charset": "utf8"}


def Dao():
    conn = connect(**conn_config)
    cs = conn.cursor()
    return (conn, cs)


@auth.verify_token
def verify_token(token):
    # 尝试解密token
    try:
        data = serializer.loads(token)
    except Exception as e:
        return False
    # 判断是否有account在token解密后的字典内
    if 'account' in data:
        conn, cs = Dao()
        result = cs.execute(
            'select token from users where account=%s;', data['account'])
        # 如果存在
        if result:
            # 判断token是否正确
            the_token = cs.fetchone()[0]
            if token == the_token:
                cs.close()
                conn.close()
                g.account = data['account']
                return True
            else:
                cs.close()
                conn.close()
                return False
        else:
            cs.close()
            conn.close()
            return False
    return False
