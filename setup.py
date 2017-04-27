from setuptools import setup, find_packages

setup(
    name='gols',
    version='0.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click', 'requests', 'pyyaml', 'testfixtures',
    ],
    entry_points='''
        [console_scripts]
        gols=src.gols:cli
    ''',
)
