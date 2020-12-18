import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="s3200",
    version="0.0.1",
    author="cbasix",
    author_email="cbasix@users.noreply.github.com",
    description="A Python package for controlling the Fröling heating system (S3200) over the maintenance interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cbasix/s3200",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)