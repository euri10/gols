from setuptools import setup

setup(
    name='gols',
    version='0.1',
    py_modules=['gols'],
    install_requires=[
        'Click', 'requests', 'pyyaml',
    ],
    entry_points='''
        [console_scripts]
        gols=gols:upload
    ''',
)