from distutils.core import setup

setup(name='FormicID',
      version='0.1',
      description='description',
      author='Marijn J. A. Boer',
      author_email='marijn.boer@naturalis.nl',
      licence='MIT licence',
      url='https://github.com/naturalis/FormicID',
      long_description=open('./README.md').read()
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
      ],
      packages=find_packages())
