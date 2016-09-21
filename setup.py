from setuptools import setup, find_packages

setup(
    name='py-manage-server',
    version='0.0.1',
    description='server config manager written in Python',
    long_description='README.md',
    author='Danil Koudlo',
    author_email='dkoudlo@gmail.com',
    install_requires=["PyYAML"],
    url='https://github.com/dkoudlo/py-manage-server',
    license=license,
    packages=find_packages(exclude=('tests', 'configuration'))
)