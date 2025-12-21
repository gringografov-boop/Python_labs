import os
from datetime import datetime

def get_file_info(path):
    size = os.path.getsize(path)
    mtime = datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M')
    return size, mtime

def is_safe_path(path):
    return path not in ('..', '/') and path != '/'

def resolve_path(current_dir, path):
    if path == '..':
        return os.path.dirname(current_dir)
    elif path == '~':
        return os.path.expanduser('~')
    else:
        return os.path.abspath(os.path.join(current_dir, path))
