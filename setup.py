# Standard library imports
# import pip

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = open('./README.md').read()

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

# links = []
# requires = []
#
# try:
#     requirements = parse_requirements('requirements.txt')
# except:
#     # new versions of pip requires a session
#     requirements = parse_requirements(
#         'requirements.txt', session=pip.download.PipSession()
#     )
#
# for item in requirements:
#     if getattr(item, 'url', None):  # older pip has url
#         links.append(str(item.url))
#     if getattr(item, 'link', None):  # newer pip has link
#         links.append(str(item.link))
#     if item.req:
#         requires.append(str(item.req))  # always the package name


setup(name='FormicID',
      version='0.0.1',
      description='CNN-based image classification of AntWeb images',
      author='Marijn J. A. Boer',
      author_email='marijn.boer@naturalis.nl',
      licence='MIT licence',
      url='https://github.com/naturalis/FormicID',
      # download_url='',
      long_description=long_description,
      platforms='any',
      install_requires=[
          'Keras == 2.1.4',
          'Pillow_SIMD == 4.3.0.post0',
          'bunch == 1.0.1',
          'graphviz == 0.8.2',
          'h5py == 2.8.0rc1.post0',
          'jmespath == 0.9.3',
          'matplotlib == 2.2.2',
          'numpy == 1.14.2',
          'pandas == 0.22.0',
          'pydot_ng == 1.0.0',
          'pypandoc == 1.4',
          'requests == 2.18.4',
          'scikit_learn == 0.19.1',
          'setuptools == 39.0.1',
          'tensorflow == 1.7.0'],
      # dependency_links=links,
      packages=find_packages(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
      ]
      )
