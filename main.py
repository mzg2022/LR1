import sys
import custom_loader

if __name__ == '__main__':
    sys.path.append("http://localhost:8000")
    sys.path_hooks.append(custom_loader.custom_url_hook)
    print(sys.path_hooks)