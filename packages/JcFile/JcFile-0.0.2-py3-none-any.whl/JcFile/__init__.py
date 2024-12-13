__copyright__    = 'Copyright (C) 2024 JavaCommons Technologies'
__version__      = '0.0.2'
__license__      = 'MIT'
__author__       = 'JavaCommons Technologies'
__author_email__ = 'javacommmons@gmail.com'
__url__          = 'https://github.com/javacommons/py-file'
__all__ = ['JcFile']

class JcFile:
    def __init__(self):
        pass
    def read_all_text(self, path):
        file = open(path, "rt")
        content = file.read()
        file.close()
        return content
    def write_all_text(self, path, content):
        file = open(path, "wb")
        file.write(content.encode())
        file.close()
