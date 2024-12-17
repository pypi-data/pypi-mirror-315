from setuptools import setup, find_packages

setup(
    name="redis-leakybucket-rate-limiter",
    version="1.0.0",
    packages=find_packages(),
    install_requires=["redis"],  
    author="Junwei(Lee) Li",
    author_email="lee.j.w.li@outlook.com",
    description="A simple Redis-based leaky bucket rate limiter",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/lee0210/rate-limiter",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
