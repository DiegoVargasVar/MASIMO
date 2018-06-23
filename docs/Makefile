# Minimal makefile for Sphinx documentation
#

export SPHINX_APIDOC_OPTIONS=members,no-undoc-members,no-show-inheritance

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = PyMasimo
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

buildapi:
	sphinx-apidoc -fMeET -o source/_modules ../pymasimo
	cp ../research.ipynb source
	jupyter nbconvert --to rst source/research.ipynb
	jupyter nbconvert --to markdown source/research.ipynb --output ../../README.md
	rm source/research.ipynb

