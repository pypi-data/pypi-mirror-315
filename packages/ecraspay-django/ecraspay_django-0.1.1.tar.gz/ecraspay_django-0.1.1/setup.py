from setuptools import setup, find_packages

setup(
    name="ecraspay-django",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "ecraspay-py >= 0.1.0",
        "requests >= 2.32.3",
        "pycryptodome >= 3.11.0",
        "Django >= 3.2.8",
    ],
    author="Asikhalaye Samuel",
    author_email="sammyboy.as@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    python_requires=">=3.6",
    description="A Django integration for the ECRAS API.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="http://github.com/thelimeskies/ecraspay-sdk/src/python-django",
)
