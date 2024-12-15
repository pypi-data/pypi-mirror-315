from setuptools import setup, find_packages, Extension
prime = Extension(
    name = "prime",
    sources = ["prime.cpp"]
)
setup(
    name = "devkit-math",
    version = "1.5.0a0",
    author = "Pemrilect",
    author_email = "retres243@outlook.com",
    license = "MIT",
    packages = find_packages(),
    ext_modules = [prime],
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: C++",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython"
    ]
)
