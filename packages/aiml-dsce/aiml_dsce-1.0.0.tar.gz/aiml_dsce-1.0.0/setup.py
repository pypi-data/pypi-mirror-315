from setuptools import setup, find_packages

setup(
    name="aiml_dsce",
    version="1.0.0",
    author="Harry Potter",
    author_email="wizardingworld474@example.com",
    description="A package containing Python programs for AI and ML lab exercises",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
