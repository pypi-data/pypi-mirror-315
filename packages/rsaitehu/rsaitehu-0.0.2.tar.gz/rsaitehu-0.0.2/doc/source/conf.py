# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sphinx_rtd_theme

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath('../../rsaitehu-clustering/rsaitehu'))
sys.path.insert(0, os.path.abspath('../../rsaitehu-drawing/rsaitehu'))
sys.path.insert(0, os.path.abspath('../../rsaitehu-geometry/rsaitehu'))
sys.path.insert(0, os.path.abspath('../../rsaitehu-matplot3d/rsaitehu'))
sys.path.insert(0, os.path.abspath('../../rsaitehu-pointcloud/rsaitehu'))
sys.path.insert(0, os.path.abspath('../../rsaitehu-procrustes/rsaitehu'))
sys.path.insert(0, os.path.abspath('../../rsaitehu-ransac/rsaitehu'))
sys.path.insert(0, os.path.abspath('../../rsaitehu-ransaccuda/rsaitehu'))
sys.path.insert(0, os.path.abspath('../../rsaitehu-sampling/rsaitehu'))
sys.path.insert(0, os.path.abspath('../../rsaitehu-stats/rsaitehu'))
sys.path.insert(0, os.path.abspath('../rsaitehu'))
sys.path.insert(0, os.path.abspath('../..'))  # Source code dir relative to this file

def setup(app):
    app.add_css_file('my_theme.css')

# -- Project information -----------------------------------------------------

project = 'RSAITEHU'
copyright = '2023, José María Martínez Otzeta'
author = 'José María Martínez Otzeta'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.todo', 'sphinx.ext.viewcode', 'sphinx.ext.autodoc', 'sphinx.ext.imgmath', 'sphinx.ext.autosummary', 'sphinx_automodapi.automodapi', 'sphinx.ext.ifconfig']

autosummary_generate = True  # Turn on sphinx.ext.autosummary

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'
html_theme = "sphinx_rtd_theme" 
html_theme_options = {'body_max_width' : None, 'collapse_navigation' : False}
# html_theme = "sphinx_book_theme"
# html_theme = 'classic'
# html_theme_options = {'nosidebar': True}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_css_files = ['custom.css']

# conf.py options for Latex
latex_engine = 'pdflatex'
latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '10pt',
    }
