import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="NyaaDesktop",
    version=0.2,
    author="mayudev",
    description="A desktop application for nyaa.si",
    long_description=long_description,
    license="MIT",
    long_description_content_type="text/markdown",
    url="https://github.com/mayudev/NyaaDesktop",
    project_urls={
        "Bug Tracker": "https://github.com/mayudev/NyaaDesktop/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Environment :: X11 Applications :: Qt"
    ],
    packages=['nyaadesktop', 'nyaadesktop.scraper', 'nyaadesktop.dialogs', 'nyaadesktop.tabs'],
    install_requires=[
        'requests',
        'beautifulsoup4',
        'lxml'
    ],
    entry_points= {
        'console_scripts': ['nyaadesktop=nyaadesktop.__main__:main'],
    },
    python_requires=">=3.8"
)