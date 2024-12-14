from setuptools import setup, find_packages

setup(
    name="hnt",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'instaloader',
    ],
    description="Thư viện lấy thông tin Instagram cơ bản",
    author="X",
    author_email="truong77kk@gmail.com",
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
