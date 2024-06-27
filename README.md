Vector Extractor
================

A Python script which extracts vector graphics from Adobe Illustrator into multiple smaller SVG files, exploiting the fact that an `.ai` file is actually a PDF-XML file in disguise. To maintain the position and transformation of the vector graphics, basic linear algebra has been used (actually I only use matrix multiplication).

> The XML node traversing code is an inefficient recursive piece of trash, which should be implemented using dynamic programming in the first place.

# Prepare:

   - Install Python 3 (tested on Python 3.8)
   - Install Inkscape (download from this [page](https://inkscape.org/release))
   - (Optional but recommended) Create `venv` then activate it 
   - Install libraries by running `pip install -r requirements.txt`

# How to use:

Type `python ./app.py --help` to show help.

# Run on Windows:

> I'm not a big fan of WinNT since all of my time has been spent on UNIX/Linux (OSX too if you don't consider it as a heavily modified BSD), but I (was) in a situation where Windows is the only environment. This code was not thoroughly tested on WinNT, but my client does not complain anything so I guess that's it...

Type `python ./app.py --inkscape-path="C:/Program Files/Inkscape/bin/inkscape.com"` to set inkscape executable path
