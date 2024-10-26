from importlib.abc import PathEntryFinder
from importlib.util import spec_from_loader
import re
from urllib.request import urlopen

class CustomURLLoader:
    def create_module(self, target):
        return None

    def exec_module(self, module):
        with urlopen(module.__spec__.origin) as page:
            source = page.read()
        code = compile(source, module.__spec__.origin, mode="exec")
        exec(code, module.__dict__)

class CustomURLFinder(PathEntryFinder):
    def __init__(self, url, available):
        self.url = url
        self.available = available

    def find_spec(self, name, target=None):
        if name in self.available:
            origin = "{}/{}.py".format(self.url, name)
            loader = CustomURLLoader()
            return spec_from_loader(name, loader, origin=origin)
        else:
            return None

def custom_url_hook(url_str):
    if not url_str.startswith(("http", "https")):
        raise ImportError
    with urlopen(url_str) as page:
        data = page.read().decode("utf-8")
    filenames = re.findall("[a-zA-Z_][a-zA-Z0-0_]*.py", data)
    modnames = {name[:-3] for name in filenames}
    return CustomURLFinder(url_str, modnames)