from setuptools import setup, find_packages

setup(
    name="sudoki",
    version="0.0.0",
    author="Dongqi Su",
    py_modules=["sudoki"],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.11.0",
)
