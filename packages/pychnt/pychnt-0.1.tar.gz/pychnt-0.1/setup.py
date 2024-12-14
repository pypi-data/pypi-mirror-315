from setuptools import setup, find_packages

setup(
    name="pychnt",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "instaloader>=4.7",
    ],
    description="Thư viện lấy thông tin Instagram",
    long_description=open("README.md", "r", encoding="utf-8").read(),

    long_description_content_type="text/markdown",
    author="hnt", 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
