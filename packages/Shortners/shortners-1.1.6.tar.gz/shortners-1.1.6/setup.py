from setuptools import setup, find_packages

with open("README.md", "r") as o:
    description = o.read()

licence = 'MIT'
version = '1.1.6'
pythons = '~=3.10'
appname = 'Shortners'
profile = 'https://github.com/Clinton-Abraham'

DATA03 = 'Python url shortner'
DATA01 = "clintonabrahamc@gmail.com"
DATA02 = ['Natural Language :: English',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Programming Language :: Python :: 3.12',
          'Programming Language :: Python :: 3.13',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules']

setup(name=appname,
      url=profile,
      version=version,
      license=licence,
      description=DATA03,
      classifiers=DATA02,
      author_email=DATA01,
      python_requires=pythons,
      packages=find_packages(),
      author='Clinton Abraham',
      long_description=description,
      install_requires=['aiohttp'],
      keywords=['url', 'shortner', 'telegram'],
      long_description_content_type="text/markdown")
