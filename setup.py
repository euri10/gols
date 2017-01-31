from setuptools import setup, find_packages

setup(
    name='gols',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click', 'requests', 'pyyaml',
    ],
    entry_points='''
        [console_scripts]
        gols=gols.gols:cli
    ''',
)