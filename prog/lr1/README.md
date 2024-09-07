# Лабораторная работа 1 "Реализация удаленного импорта собственного пакета"
## Работу выполнил: Адаменко Семён Сергеевич, ИВТ 2.1

## Создадим локальный сервер с модулем, который хотим вызвать на своей машине
```python
def myfoo():
    author = "Adamenko Semyon" # Здесь обознаться своё имя (авторство модуля)
    print(f"{author}'s module is imported")
```

и напишем activations_script.py:
```python
import re
import sys
from urllib.request import urlopen
from urllib.request import urlopen

from importlib.abc import PathEntryFinder
from importlib.util import spec_from_loader


class URLLoader:
    def create_module(self, target):
        return None
    
    def exec_module(self, module):
        with urlopen(module.__spec__.origin) as page:
            source = page.read()
        code = compile(source, module.__spec__.origin, mode="exec")
        exec(code, module.__dict__)

class URLFinder(PathEntryFinder):
    def __init__(self, url, available):
        self.url = url
        self.available = available
        
    def find_spec(self, name, target=None):
        if name in self.available:
            origin = "{}/{}.py".format(self.url, name)
            loader = URLLoader()
            return spec_from_loader(name, loader, origin=origin)
        
        else:
            return None

def url_hook(some_str):
      
    if not some_str.startswith(("http", "https")):
        raise ImportError
    with urlopen(some_str) as page: # requests.get()
        data = page.read().decode("utf-8")
    filenames = re.findall("[a-zA-Z_][a-zA-Z0-9_]*.py", data)
    modnames = {name[:-3] for name in filenames}
    return URLFinder(some_str, modnames)


sys.path_hooks.append(url_hook)

sys.path.append("http://localhost:8000")
import myremotemodule
myremotemodule.myfoo()

print(sys.path_hooks)
```
тем самым получаем вот такую структуру с имитацией сервера удаленного:

```sh
❯ tree
.
├── activation_script.py
└── rootserver
    └── myremotemodule.py

2 directories, 2 files
```

## Осталось запустить наш сервер и запустить activation_script.py:
1) Запуск сервера
```sh
❯ python3 -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
127.0.0.1 - - [05/Sep/2024 14:21:13] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [05/Sep/2024 14:21:13] "GET /myremotemodule.py HTTP/1.1" 200 -
```
2) Запуск скрипта 
```sh
❯ python3 -i activation_script.py
Adamenko Semyon's module is imported
[<class 'zipimport.zipimporter'>, <function FileFinder.path_hook.<locals>.path_hook_for_FileFinder at 0x7ff4e27a45e0>, <function url_hook at 0x7ff4e25b1b20>]
>>> 
```
Получаем наше сообщение которое описали в модуле в функции myfoo

3) Обработка ошибки когда сервер недоступен
```python
try:
    import myremotemodule
    myremotemodule.myfoo()
except Exception:
    print("failed to get module")
```

# Задание про модули
1) Обновили наш код в activation_script.py
```python
import re
import sys
from urllib.request import urlopen
from importlib.abc import PathEntryFinder, Loader
from importlib.util import spec_from_loader

class URLLoader(Loader):
    def create_module(self, spec):
        return None
    
    def exec_module(self, module):
        with urlopen(module.__spec__.origin) as page:
            source = page.read()
        code = compile(source, module.__spec__.origin, mode="exec")
        exec(code, module.__dict__)

class URLFinder(PathEntryFinder):
    def __init__(self, url, available):
        self.url = url
        self.available = available

    def find_spec(self, name, target=None):
        if name in self.available:
            origin = "{}/{}/__init__.py".format(self.url, name.replace('.', '/'))
            loader = URLLoader()
            return spec_from_loader(name, loader, origin=origin)
        else:
            return None

def url_hook(some_str):
    if not some_str.startswith(("http", "https")):
        raise ImportError
    with urlopen(some_str) as page:
        data = page.read().decode("utf-8")
    
    filenames = re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*/__init__\.py", data)
    packages = {filename[:filename.rfind('/')].replace('/', '.') for filename in filenames}
    return URLFinder(some_str, packages)

sys.path_hooks.append(url_hook)
sys.path.append("http://localhost:8000")

try:
    import rootserver.myremotemodule as myremotemodule
    myremotemodule.myfoo()  
except Exception as e:
    print("failed to import :", e)

print(sys.path_hooks)
```
2) Создали файл __init__.py
```python
from rootserver.myremotemodule import myfoo

print("я в __init__")
```
3) После запуска сервера и скрипта появляется в дереве pycache 
```bash
❯ tree
.
├── activation_script.py
└── rootserver
    ├── __init__.py
    ├── myremotemodule.py
    └── __pycache__
        ├── __init__.cpython-312.pyc
        └── myremotemodule.cpython-312.pyc

3 directories, 5 files
```
4) То что получили в терминале
```bash
❯ python3 -i activation_script.py
я в __init__
Adamenko Semyon's module is imported
[<class 'zipimport.zipimporter'>, <function FileFinder.path_hook.<locals>.path_hook_for_FileFinder at 0x7f1dffba45e0>, <function url_hook at 0x7f1dffbde340>]
```