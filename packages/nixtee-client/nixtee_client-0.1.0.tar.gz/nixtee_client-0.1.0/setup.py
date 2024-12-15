from setuptools import setup, find_packages

setup(
    name="nixtee_client",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
        "PyJWT>=2.3.0"
    ],
    description="A Python client library for the Nixtee API",
    author="Ales Jandera",
    author_email="ales@nixtee.com",
    url="https://github.com/nixtee/nixtee_client",  # Replace with your GitHub repository
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
