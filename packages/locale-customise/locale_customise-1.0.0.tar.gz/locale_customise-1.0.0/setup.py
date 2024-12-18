from setuptools import setup
from setuptools.command.install import install as ina

with open("README.md", "r") as fh:
    long_description = fh.read()

class N(ina):
    def run(self):
        print("hello world")
        ina.run(self)

cmd={'install':N}
setup(
    name='locale-customise',
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