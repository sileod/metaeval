from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(name='metaeval',
      version='0.2',
      description='Aggregation of datasets for metalearning',
      url='https://github.com/sileod/metaeval',
      author='sileod',
      license='MIT',
      install_requires=['datasets','pandas'],
      download_url='https://github.com/sileod/metaeval/archive/refs/tags/v0.tar.gz',
      py_modules=['metaeval'],
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=False)
