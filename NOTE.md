# 处理IP地址
1. 首先获取IP地址
2. 使用IP地址去查询该IP所在的城市和国家
3. 验证国家是否已经存在，如果不存在就创建一个（存在就不管）
4. 接着验证城市是否存在，如果不存在就创建一个（存在就不管）
5. 然后把IP地址存到session中
6. 请求发布接口的时候可以从session中取出这个IP地址

# csrf_token and session 持久化
1. get请求是不会验证csrf_token的，但是post方法会验证
2. 在API的请求中设置session，将session值设置为对应的city_region和country_code

# 匿名发布daily_tag
1. 首先调用初始化的接口，在session中存储必要的参数
2. 然后再调用post方法

# 正则 \d+ : 一个或多个数字
# 正则 [-\w]+ : 括号内的任意组合、+代表至少一个或多个
# 正则的开始和结束要完全匹配 ^$

# 匿名验证：
1. @ensure_csrf_cookie:强制要求视图发送csrftoken
2. post类型的请求时，强制提供csrftoken做为验证

# httpie 构造session持久化的请求
```
http localhost:8000/api/post_head_tag/ title='xxxx' desc='xxxx' X-CSRFToken:xxxx --session=session.json file -h
```

# 初始化的作用就是存储当前IP所处的国家和地区
# 可以配置不同的url方案指向同一个视图
# query.count():count是方法，不是属性，所以要加上括号

# bug :TypeError: 'RelatedManager' object is not iterable
当出现这个问题的时候，一般情况下，是没有在queryset中使用all()
如果要迭代queryset的时候，要加上queryset.all()


#### Redis缓存服务器 celery定时任务

### 通用关系模型的简单描述：xxx模型 做了xxx事

---- 2017.06.30 ----
### 添加阅读数统计
1. 通过redis来缓存阅读数
2. 新建一张阅读数统计的表，用来持久化
3. 通过定时任务，把redis里的缓存数据读取到统计表里
