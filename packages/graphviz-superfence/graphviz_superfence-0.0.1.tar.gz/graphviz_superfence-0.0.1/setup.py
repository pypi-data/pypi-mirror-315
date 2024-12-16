from setuptools import setup

setup(
    name='graphviz_superfence',
    version='0.0.1',
    py_modules=['graphviz_superfence'],
    author='Davy Cottet',
    description='A superfence pymarkdown extension to convert graphviz dot code to svg',
    url='https://graphviz-superfence.gitlab.io',
    license='GNU General Public License v3.0',
    platforms=['Any'],
    install_requires=[
          'markdown',
          'pymdown-extensions'
      ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ],
)


