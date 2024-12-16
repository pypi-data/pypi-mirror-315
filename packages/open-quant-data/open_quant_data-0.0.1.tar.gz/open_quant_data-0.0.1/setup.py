from setuptools import setup, find_packages

setup(
    name="open_quant_data",
    version="0.0.1",
    packages=find_packages(),
    author="openhe",
    author_email="hezhewen2004@gmail.com",
    description="okx quant",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url='https://github.com/openhe-hub/okx-quant',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
