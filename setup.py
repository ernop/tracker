from setuptools import setup, find_packages

requires = [
    'django',
    'MySQL-python',
    'PIL',
    'ipdb',
    'jinja2',
    'coffin',    
    'simplejson',
    'pygooglechart',
    ]

setup(name='django tracker', version='0.0.1',
      author='freeman',
      package_dir={'':'src'},
      packages=find_packages('src'),
      install_requires=requires,
      zip_safe=False
      )