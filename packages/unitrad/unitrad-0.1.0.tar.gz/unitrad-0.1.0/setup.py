from setuptools import setup, find_packages

setup(
    name='unitrad',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'aiohttp',
        'PyYAML',
    ],
    description='A WebSocket client for trading strategies',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='niexuan',
    author_email='18595847674@163.com',
    entry_points={
        'console_scripts': [
            'run_unitrade=unitrade.run_unitrade:run_unitrade',
        ],
    },
)