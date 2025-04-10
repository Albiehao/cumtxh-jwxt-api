from setuptools import setup, find_packages

setup(
    name="cumtxh-jwxt-api",
    version="1.0.0",
    packages=find_packages(
        where="src",
        exclude=["tests*", "examples*", "data*"]
    ),
    package_dir={"": "src"},
    install_requires=[
        "requests>=2.31.0",
        "pycryptodome>=3.19.0",
        "icalendar>=5.0.0",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="中国矿业大学徐海学院教务系统 API",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/cumtxh-jwxt-api",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
