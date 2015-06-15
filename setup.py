from setuptools import setup

with open("README.md", encoding="utf-8") as r:
    readme_text = r.read()

setup(name='tokenbucket',
      version='1.1.1',
      author='Ludvig Ericson',
      author_email='ludvig@lericson.se',
      long_description=readme_text,
      url='http://sendapatch.se/',
      package_dir={'': 'src'},
      py_modules=['tokenbucket'])

