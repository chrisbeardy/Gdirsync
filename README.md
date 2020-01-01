# Gdirsync
Gdirsync is a simple multi-platform file syncing tool written in python.
 
Gdirsync at its simplest is a GUI wrapper for the dirsync library https://pypi.org/project/dirsync/

## Requirements
Python requirements can be found in requirements.txt, use
```
pip install -r requirements.txt
```
Make sure to use virtualenv.

## Build
use pyinstaller:

```
pyinstaller gdirsync.spec
```

see https://pyinstaller.readthedocs.io/en/stable/usage.html for help
