# This file is Copyright 2022 Volatility Foundation and licensed under the Volatility Software License 1.0
# which is available at https://www.volatilityfoundation.org/license/vsl-v1.0
#
#
# Volatility documentation build configuration file, created by
# sphinx-quickstart on Wed Apr  2 01:48:22 2014.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import os
import sys

import sphinx.ext.apidoc


def setup(app):
    volatility_directory = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "volatility3")
    )

    source_dir = os.path.abspath(os.path.dirname(__file__))
    sphinx.ext.apidoc.main(
        ["-e", "-M", "-f", "-T", "-o", source_dir, volatility_directory]
    )

    # Go through the volatility3.framework.plugins files and change them to volatility3.plugins
    for dir, _, files in os.walk(os.path.dirname(__file__)):
        for filename in files:
            if (
                filename.startswith("volatility3.framework.plugins")
                and filename != "volatility3.framework.plugins.rst"
            ):
                # Change all volatility3.framework.plugins to volatility3.plugins in the file
                # Rename the file
                new_filename = filename.replace(
                    "volatility3.framework.plugins", "volatility3.plugins"
                )

                replace_string = b"Submodules\n----------\n\n.. toctree::\n\n"
                submodules = replace_string

                # If file already exists, read out the subpackages entries from it add them to the new list
                if os.path.exists(os.path.join(dir, new_filename)):
                    with open(os.path.join(dir, new_filename), "rb") as newfile:
                        data = newfile.read()
                        index = data.find(replace_string)
                        if index > -1:
                            submodules = data[index:]

                with open(os.path.join(dir, new_filename), "wb") as newfile:
                    with open(os.path.join(dir, filename), "rb") as oldfile:
                        line = oldfile.read()
                        correct_plugins = line.replace(
                            b"volatility3.framework.plugins", b"volatility3.plugins"
                        )
                        correct_submodules = correct_plugins.replace(
                            replace_string, submodules
                        )
                        newfile.write(correct_submodules)
                    os.remove(os.path.join(dir, filename))
            elif filename == "volatility3.framework.rst":
                with open(os.path.join(dir, filename), "rb") as contents:
                    lines = contents.readlines()
                plugins_seen = False
                with open(os.path.join(dir, filename), "wb") as contents:
                    for line in lines:
                        if b"volatility3.framework.plugins" in line:
                            plugins_seen = True
                        if plugins_seen and line == b"":
                            contents.write(b"   volatility3.plugins")
                        contents.write(line)
            elif filename == "volatility3.plugins.rst":
                with open(os.path.join(dir, filename), "rb") as contents:
                    lines = contents.readlines()
                with open(
                    os.path.join(dir, "volatility3.framework.plugins.rst"), "rb"
                ) as contents:
                    real_lines = contents.readlines()

                # Process real_lines
                for line_index in range(len(real_lines)):
                    if b"Submodules" in real_lines[line_index]:
                        break
                else:
                    line_index = len(real_lines)
                submodule_lines = [b"\n"] + real_lines[line_index:]

                plugins_seen = False
                with open(os.path.join(dir, filename), "wb") as contents:
                    for line in lines:
                        contents.write(line)
                    for line in submodule_lines:
                        contents.write(
                            line.replace(
                                b"volatility3.framework.plugins", b"volatility3.plugins"
                            )
                        )

    # Clear up the framework.plugins page
    with open(
        os.path.join(os.path.dirname(__file__), "volatility3.framework.plugins.rst"),
        "rb",
    ) as contents:
        real_lines = contents.readlines()

    with open(
        os.path.join(os.path.dirname(__file__), "volatility3.framework.plugins.rst"),
        "wb",
    ) as contents:
        for line in real_lines:
            if b"volatility3.framework.plugins." not in line:
                contents.write(line)


# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath("../.."))

from volatility3.framework import constants

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = "2.0"

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosectionlabel",
]

autosectionlabel_prefix_document = True

try:
    import sphinx_autodoc_typehints

    extensions.append("sphinx_autodoc_typehints")
except ImportError:
    # If the autodoc typehints extension isn't available, carry on regardless
    pass

# Add any paths that contain templates here, relative to this directory.
# templates_path = ['tools/templates']

# The suffix of source filenames.
source_suffix = ".rst"

# The encoding of source files.
# source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = "index"

# General information about the project.
project = "Volatility 3"
copyright = "2012-2025, Volatility Foundation"

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The full version, including alpha/beta/rc tags.
release = constants.PACKAGE_VERSION
# The short X.Y version.
version = ".".join(release.split(".")[0:2])

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
# language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
# today = ''
# Else, today_fmt is used as the format for a strftime call.
# today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = []

# The reST default role (used for this markup: `text`) to use for all
# documents.
# default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
# add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
# add_module_names = True
add_module_names = False

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
# show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# A list of ignored prefixes for module index sorting.
# modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
# keep_warnings = False

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
# html_theme = 'default'
# html_theme = 'pydoctheme'
# html_theme_options = {'collapsiblesidebar': True}
# html_theme_path = ['tools']
html_theme = "sphinx_rtd_theme"
html_theme_options = {"logo_only": True}

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
# html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
# html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
# html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = "_static/vol.png"

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = "_static/favicon.ico"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
# html_extra_path = []

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
# html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
# html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
# html_additional_pages = {}

# If false, no module index is generated.
# html_domain_indices = True

# If false, no index is generated.
# html_use_index = True

# If true, the index is split into individual pages for each letter.
# html_split_index = False

# If true, links to the reST sources are added to the pages.
# html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
# html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
# html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = "Volatilitydoc"

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    # 'preamble': '',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (
        "index",
        "Volatility.tex",
        "Volatility 3 Documentation",
        "Volatility Foundation",
        "manual",
    ),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
# latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
# latex_use_parts = False

# If true, show page references after internal links.
# latex_show_pagerefs = False

# If true, show URL addresses after external links.
# latex_show_urls = False

# Documents to append as an appendix to all manuals.
# latex_appendices = []

# If false, no module index is generated.
# latex_domain_indices = True

# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (
        "vol-cli",
        "volatility",
        "Volatility 3 Documentation",
        ["Volatility Foundation"],
        1,
    )
]

# If true, show URL addresses after external links.
# man_show_urls = False

# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        "index",
        "Volatility",
        "Volatility 3 Documentation",
        "Volatility Foundation",
        "Volatility",
        "Memory forensics framework.",
        "Miscellaneous",
    ),
]

# Documents to append as an appendix to all manuals.
# texinfo_appendices = []

# If false, no module index is generated.
# texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
# texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
# texinfo_no_detailmenu = False

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {"python": ("http://docs.python.org/", None)}

# -- Autodoc options -------------------------------------------------------

# autodoc_member_order = 'groupwise'
autodoc_default_options = {
    "members": True,
    "inherited-members": True,
    "show-inheritance": True,
}
autoclass_content = "both"
