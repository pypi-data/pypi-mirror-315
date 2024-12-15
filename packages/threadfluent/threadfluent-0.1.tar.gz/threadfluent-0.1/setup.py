from setuptools import setup, find_packages

setup(
    name="threadfluent",
    version="0.1",
    author="Anto miliano",
    author_email="Antomiliano785@gmail.com",
    description="Its a python library that can use threading and requests same time",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://threadfluent.readme.org/",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",         "Programming Language :: Python :: 3.13",        
    ],
    keywords='http fluent requests aiohttp threading',
    project_urls={
        'Documentation': 'https://threadfluent.readme.org/',
    },
    python_requires='>=3.9',
    install_requires=[
        "requests",
        "pycryptodome",
        "chardet",
        "idna",
        "pywin32",
        "WMI",
        "psutil",
        "Pillow",
        "urllib3",
        "certifi"
    ],
    entry_points={
        'console_scripts': [
            'threadfluent=threadfluent.winssl:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
    platforms=["win64"],
)


