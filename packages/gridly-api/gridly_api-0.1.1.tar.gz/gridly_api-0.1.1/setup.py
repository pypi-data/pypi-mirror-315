from setuptools import setup, find_packages

setup(
    name = 'gridly_api',
    version = '0.1.1',
    author = 'Walery Wysotsky',
    author_email = 'dev@wysotsky.info',
    description = 'Gridly (https://www.gridly.com) API',
    packages = ['gridly_api'],
    install_requires = [
          'requests',
          'python-dotenv'
    ],
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries'
    ]
)