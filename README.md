## Django入门
## 环境搭建
```shell script
uv  init
uv venv
```
##
### 安装 Django
```shell script
uv add  Django
```

### 在 Django 中创建项目
```shell script
django-admin startproject learning_log
```
### 创建数据库

```shell script
python manage.py migrate
```

### 查看项目
```shell script
python manage.py runserver
```

### 创建应用程序
```shell script
python manage.py startapp learning_logs_app
```
> models.py:定义模型
>
> admin.py 
>
>views.py
>

### 定义模型
````python
# models.py
from django.db import models


class Topic(models.Model):
    """用户学习的主题"""
    text = models.CharField(max_length=200)  # 由字符或文本组成的数据
    date_added = models.DateTimeField(auto_now_add=True)  # 记录日期和时间的数据

    def __str__(self):
        """返回模型的字符串表示"""
        return self.text
````

### 激活模型
```python
# settings.py
# --snip--      
INSTALLED_APPS = (
    # --snip--        
    'django.contrib.staticfiles',
    # 我的应用程序
    'learning_log_app',
)
 # --snip--      
```
### 修改数据库
```shell script
python manage.py makemigrations learning_log_app
```
> **每当需要修改“学习笔记”管理的数据时，都采取如下三个步骤：**
>
>1、修改**models.py**
>
>2、对**learning_log_app**调用**makemigrations**
>
>3、让Django迁移项目

### Django 管理网站