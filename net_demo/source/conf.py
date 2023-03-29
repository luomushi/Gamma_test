# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Sky Code'
copyright = '2023, Sky Code'
author = 'liu'
release = 'v1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'recommonmark',
 # 'sphinx_markdown_tables',
'sphinx.ext.autodoc',
'sphinx.ext.doctest',
'sphinx.ext.intersphinx',
'sphinx.ext.todo',
'sphinx.ext.coverage',
'sphinx.ext.mathjax'
   
]

html_context = {
"display_github": False, # Add 'Edit on Github' link instead of 'View page source'
"last_updated": True,
"commit": False,
}

templates_path = ['_templates']
exclude_patterns = []

language = 'zh_CN'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

#html_theme = 'alabaster'
html_theme = 'sphinx_rtd_theme'                             # HTML 主题
html_static_path = ['_static']

# html_copy_source=False  # 关闭右上角的查看源码
# html_copy_source=False  # 关闭右上角的查看源码
html_copy_source=False  # 关闭右上角的查看源码
html_show_sphinx = False

html_favicon = '../picture/favicon.jpg'

html_theme_options = {
    
    'logo_only': True,
    
}

html_logo = '../picture/logo.png' 
