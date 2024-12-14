from setuptools import setup, find_packages

setup(
    name="pycodes2json",
    version="1.1.0",
    description="A tool to convert Python files to a JSON file.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Lech Hubicki",
    author_email="lech.hubicki@gmail.com",
    url="https://github.com/lechplace/py2json",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "py2json=py2json.main:main_py2json",
            "json2py=py2json.main:main_json2py"
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[],
)
