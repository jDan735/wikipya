from setuptools import setup
from wikipya import __version__

with open("README.md", encoding="utf-8") as readme:
    long_description = readme.read()

setup(
    name="wikipya",
    version=__version__,
    author="Daniel Zakharov",
    author_email="daniel734@bk.ru",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="api wikipedia python",
    url="https://github.com/jDan735/wikipya",
    license="MIT",
    packages=["wikipya"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3",
    install_requires=[
        "beautifulsoup4",
        "tghtml",
        "httpx"
    ],
    test_suite="tests"
)
