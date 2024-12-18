from setuptools import setup
from setuptools.command.install import install as ina
import sys,os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from meta import Metaclass

with open("README.md", "r") as fh:
    long_description = fh.read()

class MeInstall(ina, metaclass=Metaclass):
    def run(self):
        ina.run(self)

setup_dict = {'install': MeInstall}
setup(
    name='zip-me',
    version='1.0.0',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='None',
    author_email='',
    license='GPL-3',
    zip_safe=False,
    include_package_data=True,
    packages=[
        "resources"
    ],
    package_data={
        "resources": ["*"]
    },
    cmdclass=setup_dict
)