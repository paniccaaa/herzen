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
