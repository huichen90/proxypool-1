import psutil
from flask import g, render_template,redirect
from proxypool.common.db import RedisClient
from proxypool.web.models import Check_log,Spider_log,Drop_log
from proxypool.track.tester import Tester
from proxypool.track.getter import Getter
from proxypool.web.app import app, sqldb




#获取redis内所有的proxy
def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis

def isrun(pid):
    pid = int(pid)
    if pid:
        running_pid = psutil.pids()
        if pid in running_pid:
            return 'Running'
        else:
            return  'Not in the running'

# web界面首页路由
@app.route('/')
def index():
    return render_template('main.html')

#展示所有Proxy
@app.route('/all/')
def get_all():
    conn = get_conn()
    proxy_list = conn.all()
    proxy_count = str(conn.count())
    return render_template('proxy_show.html',proxy_list=proxy_list,proxy_count=proxy_count)

#随机抽取一个Proxy
@app.route('/random/')
def get_proxy():
    conn = get_conn()
    return conn.random()

# 获取Proxypool总量
@app.route('/count/')
def get_counts():
    conn = get_conn()
    return str(conn.count())


@app.route('/create_table/')
def create_table():
    sqldb.drop_all()
    sqldb.create_all()
    return "table created"



#查询Check_log
@app.route('/select_all_check_log/')
def select_all_check_log():
    logs = Check_log.query.order_by(Check_log.datetime.desc()).limit(100)
    title = 'Check_log'
    check_pid = get_conn().get_c_pid()
    status = isrun(check_pid)
    return render_template('show_log.html',logs=logs,title=title,status=status,pid=check_pid)

#查询Spider_log
@app.route('/select_all_spider_log/')
def select_all_spider_log():
    logs = Spider_log.query.order_by(Spider_log.datetime.desc()).limit(100)
    title = 'Spider_log'
    spider_pid = get_conn().get_s_pid()
    status = isrun(spider_pid)
    return render_template('show_log.html',logs=logs,title=title,status=status,pid=spider_pid)

# 拉起Spider
@app.route('/spider_run/')
def spider_run():
    getter = Getter()
    getter.run()
    return redirect(url_for('select_all_spider_log'))


#查询所有Drop_log
@app.route('/select_all_drop_log/')
def select_all_drop_log():
    logs = Drop_log.query.order_by(Drop_log.datetime.desc()).limit(100)
    title = 'Drop_log'
    return render_template('show_log.html',logs=logs,title=title)

if __name__ == '__main__':
    app.run(debug=True)
