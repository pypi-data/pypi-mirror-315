from setuptools import setup, find_packages

setup(
    name="xml7shi",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="7shi",
    author_email="7shi@live.jp",
    description="Simple XML parser without tag structure validation",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/7shi/xml7shi",
)
