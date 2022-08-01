# Configuration file for the Sphinx documentation builder.
import os
import sys
sys.path.insert(0, os.path.abspath('../../'))
from neuroscout_cli import  __version__

# -- Project information

project = 'Neuroscout-CLI'
copyright = '2022, Neuroscout Team'
author = 'Neuroscout Team'

version = __version__

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx_click',
    'myst_parser'
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
    'fitlins': ('https://fitlins.readthedocs.io/en/latest/', None),
    'pyNS': ('https://pyns.readthedocs.io/en/latest/', None),
    'neuroscout': ('https://neuroscout.org/docs', None)
}

intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'