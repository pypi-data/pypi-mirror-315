from setuptools import setup, find_packages

setup(
    name="supermarket_system", 
    version="0.1.0",           
    author="Mngyue Zhao, Jingran Zhao",
    author_email="mingyuezhao17@gmail.com, zhaojingranjr23@163.com",
    description="This supermarket management system is designed to simulate the operation of a supermarket including goods management and the interaction with customers.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/zhaojr23/533project_step3_test",
    packages=find_packages(where="my_package"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)