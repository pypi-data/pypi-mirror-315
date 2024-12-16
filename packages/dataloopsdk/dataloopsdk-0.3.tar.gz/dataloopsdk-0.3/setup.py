import setuptools
from setuptools import find_packages

setuptools.setup(
    name="dataloopsdk",
    version="0.3",
    description="Python Package Boilerplate",
    long_description=open("README.md").read().strip(),
    long_description_content_type="text/markdown",
    author="ivan",
    python_requires=">=3.6",
    author_email="ivan.liu@anker-in.com",
    url="",
    # py_modules=['sdk'],
    install_requires=[
        "requests==2.27.1",
        "pydantic==1.9.2",
        "pycryptodome==3.21.0",
        "bson==0.5.10",
        "tqdm==4.62.3",
        "ujson==4.3.0",
        "hachoir==3.3.0"
    ],
    license="MIT License",
    zip_safe=False,
    keywords="",
    packages=find_packages(),
)
