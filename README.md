# Gdirsync
Gdirsync is a simple multi-platform file syncing tool written in python.
 
Gdirsync at its simplest is a GUI wrapper for the dirsync library https://pypi.org/project/dirsync/

## Running the program using python
Clone the repository and run the python file
```
mkdir gdirsync
cd gdirsync
git clone https://github.com/chrisbeardy/Gdirsync.git
pip install -r requirements.txt
python src/gdirsync.py 
```

## Development and build
Developing should be done inside a virtualenv.

Python requirements for development and build can be found in requirements.txt and requirements-dev.txt, use
```
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

use pyinstaller to build

```
pyinstaller gdirsync.spec
```

### Docs
Docs are written using Sphinx and hosted on read the docs, requirements for generating documentation locally are in docs/requirements.txt, use
```
pip install -r docs/requirements.txt
```
