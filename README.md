# 代理池（ProxyPool）子系统Demo摘要

一、目录结构

```
ProxyPool
        │  api.py   #定义接口和视图函数的
        │  proxy provider.txt   #代理网站的URL记录
        │  README.md	#本文件
        │  requirements.txt		#项目依赖包文件
        │  run.py		项目启动文件
        │  scheduler.py		项目调度模块
        │  
        └─proxypool
            │  __init__.py
            │  
            ├─common
            │      db.py	#redis数据库定义文件
            │      error.py		#错误类的定义文件
            │      setting.py	#全局配置文件
            │      __init__.py
            │      
            ├─log
            │      save_log.py	#Log存储接口文件
            │      __init__.py
            │      
            ├─spider
            │      crawler.py	#代理网站解析规则定义文件
            │      utils.py		#爬虫调度模块
            │      __init__.py
            │      
            ├─track
            │      getter.py	#代理添加组件
            │      tester.py	#代理检测组件
            │      __init__.py
            │      
            └─web
                │  app.py	#flask实例文件
                │  models.py	#数据库模型文件
                │  __init__.py
                │  
                ├─static
                │  ├─css	
                │  │      bootstrap.min.css	#css层叠样式表
                │  │      
                │  ├─img
                │  └─js
                │          bootstrap.min.js		#Javascript文件
                │          jquery.min.js	#Javascript文件
                │          
                └─templates
                    │  main.html	#Html模板文件
                    │  proxy_show.html	#Html模板文件
                    │  show_log.html	#Html模板文件
                    │  
                    └─common
                            base.html #Html基础模板文件
```

二、运行

```
1.安装依赖环境（建议在虚拟环境下运行）
pip install -r requirements.txt	
2.根据当前主机的数据库参数对setting.py进行修改
Proxypool/proxypool/common/setting.py
3.终端切换到根目录下
python run.py
4.打开浏览器访问我们的URl，即可来到我们的代理池监控页面
默认：http://127.0.0.1:5555
注：初次运行访问http://127.0.0.1:5555/create_table/，进行Mysql数据库建表，建表成功会返回table created，然后重新运行
```

