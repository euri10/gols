from setuptools import setup, find_packages

# yourpackage/
#     __init__.py
#     main.py
#     utils.py
#     scripts/
#         __init__.py
#         yourscript.py
# yourscript=yourpackage.scripts.yourscript:cli

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