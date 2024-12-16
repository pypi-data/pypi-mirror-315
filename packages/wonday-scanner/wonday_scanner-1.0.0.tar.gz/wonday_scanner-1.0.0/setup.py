from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="wonday-scanner",
    version="1.0.0",
    author="Wonday",
    author_email="wonday@whitehat.kr",
    description="A comprehensive web security scanner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/wonday-scanner",
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.0',
        'beautifulsoup4>=4.9.3',
        'urllib3>=1.26.0',
        'dnspython>=2.1.0',
        'python-whois>=0.7.3'
    ],
    entry_points={
        'console_scripts': [
            'wonday-scanner=wonday_scanner.main:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Security",
    ],
    python_requires='>=3.6',
) 