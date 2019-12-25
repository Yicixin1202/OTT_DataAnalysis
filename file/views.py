from . import app_file
from flask import g, request, jsonify, send_file, send_from_directory, make_response
from pymysql import *
from auth import *
import random
import os
import json
import mainAnalysisData
import selectDataByProvince
import selectDataOfDate
import jb


# 文件存储路径
UPLOAD_FILE_FOLDER = 'static/files'
# 允许的文件后缀名
ALLOWED_EXTENSIONS = ['txt', 'csv', 'xsl']

# 配置数据库信息
conn_config = {"host": "localhost", "port": 3306, "user": "root",
               "password": "2356147", "database": "data", "charset": "utf8"}


def random_path(extension):
    random_path_str = 'asdfghjklpoiuytrzxc_qwevbnmQWASZXCDERFVTGBNHYUJMKIOLP1547896320'
    path = ''
    for i in range(20):
        path += random_path_str[random.randint(0, len(random_path_str) - 1)]
    path += '.' + extension
    return path


def Dao():
    conn = connect(**conn_config)
    cs = conn.cursor()
    return (conn, cs)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app_file.route('/file/upload', methods=['post'])
@auth.login_required
def file_upload():
    account = g.account
    # 用户想要的文件名
    file_name = request.form.get('file_name')
    file = request.files.get('myfile')
    if not (file_name and file):
        return 'error'

    # 检查文件后缀
    if not allowed_file(file.filename):
        return 'type error'
    else:
        # 文件的本地路径
        path = random_path(file.filename.rsplit('.', 1)[1])
        # 保存至本地
        file.save(os.path.join(UPLOAD_FILE_FOLDER, path))
        # 插入数据库
        conn, cs = Dao()
        result = cs.execute(
            'insert into files(account, filename, file_path, upload_time) values(%s, %s, %s, now());', (account, file_name, path))
        conn.commit()
        cs.close()
        conn.close()
        if result:
            return 'success'
        else:
            return 'failed'


@app_file.route('/file/one_all', methods=['get'])
@auth.login_required
def file_one_all():
    conn, cs = Dao()
    count = cs.execute(
        'select * from files where account=%s and status=1;', g.account)
    data_dict = {}
    for i in range(count):
        temp = cs.fetchone()
        temp_dict = {}
        temp_dict['file_id'] = temp[0]
        temp_dict['file_name'] = temp[2]
        temp_dict['upload_time'] = str(temp[4])
        data_dict[str(i)] = temp_dict

    cs.close()
    conn.close()
    return jsonify(data_dict)


@app_file.route('/file/delete', methods=['post'])
@auth.login_required
def file_delete():
    id = request.form.get('file_id')
    if not id:
        return 'error'
    conn, cs = Dao()
    count = cs.execute('select account from files where id=%s;', id)
    # 没有该文件
    if not count:
        cs.close()
        conn.close()
        return 'not exist'
    else:
        # 判断是否是该用户的文件
        file_account = cs.fetchone()[0]
        if g.account == file_account:
            result = cs.execute('update files set status=0 where id=%s;', id)
            conn.commit()
            cs.close()
            conn.close()
            if result:
                return 'success'
            else:
                return 'failed'
        else:
            cs.close()
            conn.close()
            return 'auth error'

# 分析文件上传


@app_file.route('/ana/upload', methods=['post'])
@auth.login_required
def ana_upload():
    account = g.account
    file_id = request.form.get('file_id')
    res_name = request.form.get('res_name')
    res_path = 'None'
    status = request.form.get('status')
    parameter = request.form.get('parameter')

    if not (file_id and res_name and parameter and status):
        return 'error'
    else:
        conn, cs = Dao()
        try:
            count = cs.execute('insert into analysis_res(account, file_id, res_name, res_path, ana_time, parameter, status) values(%s, %s, %s, %s, now(), %s, %s);',
                               (account, file_id, res_name, res_path, parameter, status))
            insert_id = conn.insert_id()
            conn.commit()
        except Exception as e:
            cs.close()
            conn.close()
            return 'insert sql error'
        if count:
            return str(insert_id)
        else:
            return 'failed'


@app_file.route('/ana/one_all', methods=['get'])
@auth.login_required
def ana_one_all():
    account = g.account
    file_id = request.args.get('file_id')
    if not file_id:
        return 'error'
    else:
        data_dict = {}
        file_if_existing = 0
        try:
            conn, cs = Dao()
            file_if_existing = cs.execute(
                'select account from files where id=%s;', file_id)
        except Exception as e:
            return 'sql error1'

        if not file_if_existing:
            return 'not exist'
        elif account != cs.fetchone()[0]:
            return 'auth error'
        else:
            count = 0
            try:
                count = cs.execute(
                    'select * from analysis_res where status > 0 and file_id=%s;', file_id)
            except Exception as e:
                return 'sql error2'
            for i in range(count):
                temp = cs.fetchone()
                temp_dict = {}
                temp_dict['id'] = temp[0]
                temp_dict['res_name'] = temp[3]
                temp_dict['ana_time'] = str(temp[5])
                temp_dict['status'] = temp[6]
                temp_dict['res_time'] = str(temp[8])
                data_dict[str(i)] = temp_dict
            return jsonify(data_dict)


@app_file.route('/ana/start', methods=['post'])
@auth.login_required
def ana_start():
    account = g.account
    id = request.form.get('id')
    if not id:
        return 'error'
    else:
        file_if_existing = 0
        try:
            conn, cs = Dao()
            file_if_existing = cs.execute(
                'select account from analysis_res where status>0 and id = %s', id)
        except Exception as e:
            return 'sql error1'
        if not file_if_existing:
            return 'not exist'
        else:
            if not (account == cs.fetchone()[0]):
                return 'auth error'
            else:
                # 进行调用, 获取文件路径, status
                cs.execute(
                    'select f.file_path,res.status,res.parameter from files as f,analysis_res as res where f.id=res.file_id and res.id=%s;', id)
                temp = cs.fetchone()
                file_path = temp[0]
                status = temp[1]
                parameter = json.loads(temp[2])
                # 调用饼图分析
                if status == 1:
                    resultFilePath = mainAnalysisData.analysis(
                        './static/files/' + file_path, parameter)
                    result = cs.execute(
                        'update analysis_res set res_path=%s,res_time=now() where id=%s;', (str(resultFilePath), id))
                    conn.commit()
                if status == 2:
                    resultFilePath = selectDataOfDate.CalendarAnalysis(
                        './static/files/' + file_path, parameter)
                    result = cs.execute(
                        'update analysis_res set res_path=%s,res_time=now() where id=%s;', (str(resultFilePath), id))
                    conn.commit()
                if status == 3:
                    resultFilePath = selectDataByProvince.provinceAnalysis(
                        './static/files/' + file_path, parameter)
                    result = cs.execute(
                        'update analysis_res set res_path=%s,res_time=now() where id=%s;', (str(resultFilePath), id))
                    conn.commit()
                # 分析完成后, 插入一个消息
                cs.execute(
                    'select res_name,status from analysis_res where id=%s;', id)
                temp = cs.fetchone()
                res_name = temp[0]
                res_type = temp[1]
                cs.execute(
                    'insert into message(account, res_id, res_name,type) values(%s,%s,%s,%s);', (account, id, res_name, res_type))
                conn.commit()
                cs.close()
                conn.close()
                if not result:
                    return 'update failed'
                else:
                    return 'success'


@app_file.route('/ana/res_data', methods=['post'])
@auth.login_required
def res_data():
    id = request.form.get('id')
    if not id:
        return 'error'
    conn, cs = Dao()
    count = cs.execute('select res_path from analysis_res where id=%s;', id)
    if count == 0:
        return 'not exist'
    res_path = cs.fetchone()[0]
    # 最终数据
    data = None
    with open('./res/' + res_path, "r") as txt_file:
        data = txt_file.read()
    count = cs.execute(
        'select f.filename,res.res_name,res.ana_time,res.res_time,res.status,res.parameter from files as f, analysis_res as res where res.file_id=f.id and res.id=%s and res.status>0;', id)
    if count == 0:
        return 'not exist'
    data_dict = {}
    temp = cs.fetchone()
    data_dict['file_name'] = temp[0]
    data_dict['res_name'] = temp[1]
    data_dict['ana_time'] = str(temp[2])
    data_dict['res_time'] = str(temp[3])
    data_dict['status'] = temp[4]
    data_dict['parameter'] = temp[5]
    data_dict['data'] = data
    return jsonify(data_dict)


@app_file.route('/ana/delete', methods=['post'])
@auth.login_required
def ana_delete():
    id = request.form.get('id')
    if not id:
        return 'error'
    conn, cs = Dao()
    count = cs.execute('select account from analysis_res where id=%s;', id)
    if not count:
        return 'not exist'
    if g.account != cs.fetchone()[0]:
        return 'auth error'
    result = cs.execute('update analysis_res set status=0 where id=%s;', id)
    conn.commit()
    cs.close()
    conn.close()
    if result:
        return 'success'
    else:
        return 'failed'


@app_file.route('/mes/get', methods=['get'])
@auth.login_required
def mes_get():
    account = g.account
    conn, cs = Dao()
    count = cs.execute('select * from message where account=%s;', account)
    data = {}
    for i in range(count):
        temp = cs.fetchone()
        temp_dict = {}
        temp_dict['mes_id'] = temp[0]
        temp_dict['res_id'] = temp[2]
        temp_dict['res_name'] = temp[3]
        temp_dict['status'] = temp[4]
        temp_dict['type'] = temp[5]
        data[str(i)] = temp_dict
    return jsonify(data)


@app_file.route('/mes/read', methods=['post'])
@auth.login_required
def mes_read():
    id = request.form.get('mes_id')
    if not id:
        return 'error'
    conn, cs = Dao()
    cs.execute('update message set status=0 where id=%s;', id)
    conn.commit()
    cs.close()
    conn.close()
    return 'success'


@app_file.route('/tag/get', methods=['post'])
@auth.login_required
def tag_get():
    res_id = request.form.get('res_id')
    ip_address = request.form.get('ip_address')
    if not (res_id and ip_address):
        return 'error'
    conn, cs = Dao()
    cs.execute(
        'select files.file_path from files,analysis_res where analysis_res.file_id=files.id and analysis_res.id=%s;', res_id)
    path = cs.fetchone()[0]
    cs.close()
    conn.close()
    path = os.path.join(UPLOAD_FILE_FOLDER, path)
    return jb.jieba_action(path, ip_address)


@app_file.route('/ana/download_valid', methods=['post'])
@auth.login_required
def download_valid():
    return 'success'


@app_file.route('/ana/download', methods=['get'])
def res_download():
    res_id = request.args.get('res_id')
    if not res_id:
        return 'error'
    conn, cs = Dao()
    cs.execute(
        'select res_path from analysis_res where id=%s;', res_id)
    res_path = cs.fetchone()[0]
    return send_file('res/' + res_path,
                     mimetype='text/csv',
                     attachment_filename=res_path,
                     as_attachment=True)
