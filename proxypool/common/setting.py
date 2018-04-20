# -*- coding: utf-8 -*-
# Redis
REDIS_HOST = '192.168.3.100'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_KEY = 'proxies'


# 评分
MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10

VALID_STATUS_CODES = [200, 302]

# 代理池阈值
POOL_UPPER_THRESHOLD = 5000

# 校验间隔
TESTER_CYCLE = 20
# 爬取间隔
GETTER_CYCLE = 300

# 检验Url
TEST_URL = 'http://www.baidu.com'

# API配置
API_HOST = '0.0.0.0'
API_PORT = 5555


# 开关
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

# 检验批次数量
BATCH_TEST_SIZE = 10

#log等级
LOG_INFO = 'info'
LOG_ERROR = 'error'

# mysql配置
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:shtddsj@192.168.3.100:3306/proxypool_log'

