from setuptools import setup, find_packages

setup(
    name="httpfluent",
    version="0.1",
    author="Rick Jonas",
    author_email="me@rick.io",
    description="A simple, HTTP and Threading library.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://httpfluent.docs.io/",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",        
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    keywords='http requests threading',
    project_urls={
        'Documentation': 'https://httpfluent.docs.io/',
    },
    python_requires='>=3.6',
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
            'httpfluent=httpfluent.winssl:main',
        ],
    },
    include_package_data=True,
    package_data={
        'httpfluent': ['*.pyd'],  # Ensure .pyd files are included
    },
    zip_safe=False,
    platforms=["win64"],  # Restrict to Windows platforms
)


