import os
import re
import sys
import urllib.request
from importlib.abc import PathEntryFinder, Loader
from importlib.util import spec_from_loader

project_dir = "prog/lr1"  
rootserver_dir = os.path.join(project_dir, "rootserver")

if not os.path.exists(rootserver_dir):
    os.makedirs(rootserver_dir)

gist_url_base = "https://gist.githubusercontent.com/paniccaaa/88e249b520b0fc608e016f7cc198a24a/raw/ada43dd38396f20c7b9b61aed640cddd5ed57400"

def download_file(url, filename):
    with urllib.request.urlopen(url) as response:
        content = response.read()
        with open(os.path.join(rootserver_dir, filename), "wb") as f:
            f.write(content)

download_file(f"{gist_url_base}/__init__.py", "__init__.py")
download_file(f"{gist_url_base}/myremotemodule.py", "myremotemodule.py")

class URLLoader(Loader):
    def create_module(self, spec):
        return None  

    def exec_module(self, module):
        with open(module.__spec__.origin, "r") as f:
            source = f.read()  
        code = compile(source, module.__spec__.origin, mode="exec")
        exec(code, module.__dict__)  


class URLFinder(PathEntryFinder):
    def __init__(self, url, available):
        self.url = url
        self.available = available

    def find_spec(self, name, target=None):
        if name in self.available:
            origin = f"{self.url}/{name}.py"
            loader = URLLoader()
            return spec_from_loader(name, loader, origin=origin)
        return None


def url_hook(some_str):
    if not some_str.startswith("http"):
        raise ImportError
    filenames = re.findall(r"([a-zA-Z_][a-zA-Z0-9_]*\.py)", some_str)
    modules = {filename[:-3] for filename in filenames}  
    return URLFinder(some_str, modules)


sys.path_hooks.append(url_hook)

sys.path.append(os.path.join(os.getcwd(), project_dir))

try:
    import rootserver.myremotemodule  
    rootserver.myremotemodule.myfoo() 
except Exception as e:
    print("failed to import:", e)

print(sys.path_hooks)
