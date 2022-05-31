import os

from setuptools import setup

BASEDIR = os.path.abspath(os.path.dirname(__file__))


def required(requirements_file):
    """ Read requirements file and remove comments and empty lines. """
    with open(os.path.join(BASEDIR, requirements_file), 'r') as f:
        requirements = f.read().splitlines()
        if 'MYCROFT_LOOSE_REQUIREMENTS' in os.environ:
            print('USING LOOSE REQUIREMENTS!')
            requirements = [r.replace('==', '>=').replace('~=', '>=') for r in requirements]
        return [pkg for pkg in requirements
                if pkg.strip() and not pkg.startswith("#")]


with open("./version.py", "r", encoding="utf-8") as v:
    for line in v.readlines():
        if line.startswith("__version__"):
            if '"' in line:
                version = line.split('"')[1]
            else:
                version = line.split("'")[1]


with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='neon_solvers',
    version=version,
    packages=['neon_solvers'],
    url='https://github.com/NeonGeckoCom/neon_solvers',
    license='bsd3',
    install_requires=required("requirements/requirements.txt"),
    author='Neongecko',
    author_email='developers@neon.ai',
    description='neon question solver plugin framework',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
