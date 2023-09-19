# -- Path setup --------------------------------------------------------------

import os
import sys
import sphinx_bootstrap_theme
sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'WebCards'
copyright = '2023'
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
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

html_theme = 'bootstrap'
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()