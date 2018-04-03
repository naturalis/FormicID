# Standard library imports
import pip

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = open('./README.md').read()

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

long_description = pypandoc.convert('README.md', 'rst')

links = []
requires = []

try:
    requirements = pip.req.parse_requirements('requirements.txt')
except:
    # new versions of pip requires a session
    requirements = pip.req.parse_requirements(
        'requirements.txt', session=pip.download.PipSession()
    )

for item in requirements:
    if getattr(item, 'url', None):  # older pip has url
        links.append(str(item.url))
    if getattr(item, 'link', None):  # newer pip has link
        links.append(str(item.link))
    if item.req:
        requires.append(str(item.req))  # always the package name


setup(name='FormicID',
      version='0.0.1',
      description='CNN-based image classification of AntWeb images',
      author='Marijn J. A. Boer',
      author_email='marijn.boer@naturalis.nl',
      licence='MIT licence',
      url='https://github.com/naturalis/FormicID',
      download_url='https://github.com/naturalis/FormicID/archive/master.zip',
      long_description=long_description,
      platforms='any',
      install_requires=requires,
      dependency_links=links,
      packages=find_packages(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
      ]
      )
