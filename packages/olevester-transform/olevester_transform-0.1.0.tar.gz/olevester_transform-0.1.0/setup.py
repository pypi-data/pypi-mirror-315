from setuptools import setup, find_packages

setup(
    name="olevester_transform",
    version="0.1.0",
    description="A Python library for dimensional navigation and normalization",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Anthony Olevester",
    author_email="olevester.joram123@gmail.com",
    url="https://github.com/ANTHONY-OLEVESTER/Olevester-Transformer",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["numpy"],
)
