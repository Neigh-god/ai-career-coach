Python 3.11.1 (tags/v3.11.1:a7a450f, Dec  6 2022, 19:58:39) [MSC v.1934 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> import os
... 
... def write_file(path, content):
...     os.makedirs(os.path.dirname(path), exist_ok=True) if '/' in path else None
...     with open(path, 'w', encoding='utf-8') as f:
...         f.write(content)
...     print(f'Created: {path}')
... 
... # Create all files here...
