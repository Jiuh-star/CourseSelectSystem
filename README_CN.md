# Django-CSS

基于Django的选课管理系统实现(CSS意指Course Selection System)

README 语言: [English](/README.md)  中文

## 依赖

```text
Django
django_debug_toolbar
django-debug-toolbar-request-history
django-simple-captcha
```

## 使用说明

**注意: 为安全起见，你应该修改 `setting.py` 文件中的 `SECRET_KEY` 和 `DEBUG`！**
1. 执行 `pip install -r requirements.txt`  安装所需的基本依赖包
2. 安装 **MariaDB** 或 **MySQL** 作为数据库后台
3. 在项目文件夹下创建一个 'Instances' 文件夹，并创建一个 'db.cnf' 的文本文件，写入你的配置文件，如下所示：
```ini
[client]
database = database_name
user = user
password = password
default-character-set = utf8
```
4. 使用 `Nginx + Gunicorn(gevent) + Django + MariaDB` 或你喜欢的其它 Web 架构运行

## 版本发布

1. 0.0.1-alpha: 基本功能实现
2. 0.0.2: Bugs修复，安全性改善

## 许可证

```text
MIT License

Copyright (c) 2020 Jiuh-star

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
