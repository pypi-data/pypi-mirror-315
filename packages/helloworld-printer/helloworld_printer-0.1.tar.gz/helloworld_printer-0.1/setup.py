import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent.resolve()

PACKAGE_NAME = "helloworld-printer"
AUTHOR = "kenchou2006"
AUTHOR_EMAIL = "kenchou2006@gmail.com"
URL = "https://github.com/kenchou2006/helloworld-print-py"
LICENSE = "MIT"
VERSION = "1.0.0"
DESCRIPTION = 'helloworld("print")'
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding="utf8") if (HERE / "README.md").exists() else DESCRIPTION
LONG_DESC_TYPE = "text/markdown"

requirements = (HERE / "requirements.txt").read_text(encoding="utf8") if (HERE / "requirements.txt").exists() else ""
INSTALL_REQUIRES = [line.strip() for line in requirements.splitlines() if line.strip() and not line.startswith("#")]

CLASSIFIERS = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
] + [f"Programming Language :: Python :: 3.{v}" for v in range(7, 12)]
PYTHON_REQUIRES = ">=3.7"

setup(
    name=PACKAGE_NAME,
    version='v0.01',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    python_requires=PYTHON_REQUIRES,
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(),
    classifiers=CLASSIFIERS,
    entry_points={
        "console_scripts": [
            "helloworld=helloworld.main:helloworld",
        ],
    },
)
