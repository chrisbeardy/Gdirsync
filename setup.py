import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="Gdirsync",
    version="0.1.0",
    author="Christopher Beard",
    author_email="christopherbeard@pm.me",
    description="Simple multi-platform file syncing tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["directory", "folder", "update", "synchronisation"],
    url="https://github.com/chrisbeardy/Gdirsync",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Utilities",
        "Topic :: Desktop Environment",
        "Topic :: System :: Archiving :: Backup",
        "Topic :: System :: Archiving :: Mirroring",
    ),
    python_requires=">=3.5",
)
