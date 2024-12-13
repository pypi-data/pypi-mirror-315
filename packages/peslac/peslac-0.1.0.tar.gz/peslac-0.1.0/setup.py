from setuptools import setup, find_packages

setup(
    name="peslac",
    version="0.1.0",
    keywords=["peslac", "ai", "api", "wrapper", "python", "sdk"],
    packages=find_packages(),
    install_requires=[
        "requests",
        "requests-toolbelt",
    ],
    description="A Python package for the Peslac API",
    author="Peslac AI",
    author_email="support@peslac.com",
    url="https://github.com/peslacai/peslac-python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
