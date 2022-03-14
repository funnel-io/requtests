from os import path
from re import search
from setuptools import find_packages, setup


HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, "README.md"), encoding="utf-8") as f:
    README = f.read()

with open(path.join(HERE, "src", "requtests", "__init__.py"), encoding="utf-8") as f:
    VERSION = search(r'VERSION = "(\d+\.\d+\.\d+)"', f.read()).group(1)

setup(
    name="requtests",
    version=VERSION,
    description="Test helpers for the requests library.",
    license="MIT",
    author="The Funnel Dev Team",
    author_email="open-source@funnel.io",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries",
    ],
    keywords="Requests Testing",
    long_description=README,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires="~=3.8",
    project_urls={
        "Bug Reports": "https://github.com/funnel-io/requtests/issues",
        "Source": "https://github.com/funnel-io/requtests",
    },
    url="https://github.com/funnel-io/requtests",
)
