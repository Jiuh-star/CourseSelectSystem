# CourseSelectSystem
A django-based system that implemented student course selection .

## Requirements

Django
django_debug_toolbar
django-debug-toolbar-request-history
django-simple-captcha

## How to use

1. execute `pip install -r requirements.txt` to install based required packages.
2. Then, you need to install **MariaDB** or **MySQL** as Django database backend.
3. Create a folder named 'Instances' in project folder, and create a file named 'db.cnf', write down your database config as the following:
```ini
[client]
database = database_name
user = user
password = password
default-character-set = utf8
```
4. Run with `Nginx + Gunicorn(gevent) + Django + MariaDB` or whatever combination you like.

## Release notes

1. 0.0.1-alpha: Base feature implemented.

## License

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
