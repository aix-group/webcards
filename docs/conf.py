# -- Path setup --------------------------------------------------------------

import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'WebCards'
date = datetime.now()
copyright = "2023-{year}, WisPerMed".format(year=date.timetuple()[0])
author = 'Bahadir Eryilmaz'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'sphinx.ext.mathjax',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinxarg.ext',
    'sphinx.ext.autosectionlabel',
    'myst_parser',
]

# The master toctree document.
master_doc = "index"

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

html_theme = 'sphinx_rtd_theme'
#html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()
