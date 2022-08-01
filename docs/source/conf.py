# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'Neuroscout-CLI'
copyright = '2022, Neuroscout Team'
author = 'Neuroscout Team'

release = '0.6'
version = '0.6.7'

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