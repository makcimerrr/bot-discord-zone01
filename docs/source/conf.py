import os
import sys
sys.path.insert(0, os.path.abspath('../..'))
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'bot-discord-zone01'
copyright = '2024, Maxime Dubois'
author = 'Maxime Dubois'
release = '1.2.2'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',    # Pour générer automatiquement la documentation des docstrings
    'sphinx.ext.napoleon',   # Pour supporter les styles Google et NumPy
    'sphinx.ext.viewcode'    # Pour inclure les liens vers le code source
]

templates_path = ['_templates']
exclude_patterns = []

language = 'fr'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

# -- Options for autodoc -----------------------------------------------------
autodoc_member_order = 'bysource'
